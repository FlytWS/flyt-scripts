"""
Basic Configuration Common Use Cases
"""

from cryptoauthlib import *
from cryptoauthlib.device import *
from common import *
import time
import ctypes
import base64
import argparse
import os
import sys


# Maps common name to the specific name used internally
atca_names_map = {'i2c': 'i2c', 'hid': 'kithid', 'sha': 'sha20x', 'ecc': 'eccx08'}

# Configuration for ATECC508A
_atecc508_config = bytearray.fromhex(
    'B0 00 55 00 8F 20 C4 44 87 20 87 20 8F 0F C4 36'
    '9F 0F 82 20 0F 0F C4 44 0F 0F 0F 0F 0F 0F 0F 0F'
    '0F 0F 0F 0F FF FF FF FF 00 00 00 00 FF FF FF FF'
    '00 00 00 00 FF FF FF FF FF FF FF FF FF FF FF FF'
    'FF FF FF FF 00 00 55 55 FF FF 00 00 00 00 00 00'
    '33 00 1C 00 13 00 13 00 7C 00 1C 00 3C 00 33 00'
    '3C 00 3C 00 3C 00 30 00 3C 00 3C 00 3C 00 30 00')

# Configuration for ATECC608A
_atecc608_config = bytearray.fromhex(
    '6A 00 00 01 85 00 82 00  85 20 85 20 85 20 C6 46'
    '8F 0F 9F 8F 0F 0F 8F 0F  0F 0F 0F 0F 0F 0F 0F 0F'
    '0D 1F 0F 0F FF FF FF FF  00 00 00 00 FF FF FF FF'
    '00 00 00 00 00 00 03 F7  00 69 76 00 00 00 00 00'
    '00 00 00 00 00 00 55 55  FF FF 0E 60 00 00 00 00'
    '53 00 53 00 73 00 73 00  73 00 38 00 7C 00 1C 00'
    '3C 00 1A 00 3C 00 30 00  3C 00 30 00 12 00 30 00')

_configs = {'ATECC508A': _atecc508_config,
            'ATECC608': _atecc608_config }





def configure_device(iface='i2c', device='ecc', i2c_addr=None, keygen=True, **kwargs):
    ATCA_SUCCESS = 0x00

    # Loading cryptoauthlib(python specific)
    load_cryptoauthlib()

    # Get the target default config
    cfg = eval('cfg_at{}a_{}_default()'.format(atca_names_map.get(device), atca_names_map.get(iface)))

    # Raspberry Pi I2C
    cfg.cfg.atcai2c.bus = 1

    # Initialize the stack
    assert atcab_init(cfg) == ATCA_SUCCESS
    print('')

    # Check device type
    info = bytearray(4)
    assert atcab_info(info) == ATCA_SUCCESS
    dev_name = get_device_name(info)
    dev_type = get_device_type_id(dev_name)

    # Reinitialize if the device type doesn't match the default
    if dev_type != cfg.devtype:
        cfg.dev_type = dev_type
        assert atcab_release() == ATCA_SUCCESS
        time.sleep(1)
        assert atcab_init(cfg) == ATCA_SUCCESS

    # Request the Serial Number
    serial_number = bytearray(9)
    assert atcab_read_serial_number(serial_number) == ATCA_SUCCESS
    print('\nSerial number: ')
    print(pretty_print_hex(serial_number, indent='    '))

    # Check the zone locks
    print('\nReading the Lock Status')
    is_locked = AtcaReference(False)
    assert ATCA_SUCCESS == atcab_is_locked(0, is_locked)
    config_zone_lock = bool(is_locked.value)

    assert ATCA_SUCCESS == atcab_is_locked(1, is_locked)
    data_zone_lock = bool(is_locked.value)

    print('    Config Zone: {}'.format('Locked' if config_zone_lock else 'Unlocked'))
    print('    Data Zone: {}'.format('Locked' if data_zone_lock else 'Unlocked'))

    # Get Current I2C Address
    print('\nGetting the I2C Address')
    response = bytearray(4)
    assert ATCA_SUCCESS == atcab_read_bytes_zone(0, 0, 16, response, 4)
    print('    Current Address: {:02X}'.format(response[0]))

    # Program the configuration zone
    print('\nProgram Configuration')
    if not config_zone_lock:
        config = _configs.get(dev_name)
        if config is None:
            raise ValueError('Unknown Device Type: {}'.format(dev_type))

        # Update with the target I2C Address
        if i2c_addr is not None:
            config[0] = i2c_addr

        print('\n    New Address: {:02X}'.format(config[0]))
        print('    Programming {} Configuration'.format(dev_name))

        # Write configuration
        assert ATCA_SUCCESS == atcab_write_bytes_zone(0, 0, 16, config, len(config))
        print('        Success')

        # Verify Config Zone
        print('    Verifying Configuration')
        config_qa = bytearray(len(config))
        atcab_read_bytes_zone(0, 0, 16, config_qa, len(config_qa))

        if config_qa != config:
            raise ValueError('Configuration read from the device does not match')
        print('        Success')

        print('    Locking Configuration')
        assert ATCA_SUCCESS == atcab_lock_config_zone()
        print('        Locked')
    else:
        print('    Locked, skipping')
    
    # Check data zone lock
    print('\nActivating Configuration')
    if not data_zone_lock:
        # Generate initial ECC key pairs, if applicable
        key_gen(dev_name)

        # Lock the data zone
        assert ATCA_SUCCESS == atcab_lock_data_zone()
        print('    Activated')
    else:
        print('    Already Active')



    print('\nLoading Public key\n')
    public_key = bytearray(64)
    assert atcab_get_pubkey(0, public_key) == ATCA_SUCCESS
    print(convert_ec_pub_to_pem(public_key))
    publictopem = convert_ec_pub_to_pem(public_key)
    with open("/etc/flyt/publickey", 'w+') as file:
        file.write(publictopem)


    atcab_release()





def key_gen(dev_name):
    """Reviews the configuration of a device and generates new random ECC key pairs for slots that allow it."""
    ATCA_SUCCESS = 0x00

    if 'ECC' not in dev_name:
        return  # SHA device, no keys to generate

    # Read the device configuration
    config_data = bytearray(128)
    assert ATCA_SUCCESS == atcab_read_config_zone(config_data)
    if dev_name == 'ATECC508A':
        config = Atecc508aConfig.from_buffer(config_data)
    elif dev_name == 'ATECC608':
        config = Atecc608Config.from_buffer(config_data)
    else:
        raise ValueError('Unsupported device {}'.format(dev_name))

    # Review all slot configurations and generate keys where possible
    for slot in range(16):
        if not config.KeyConfig[slot].Private:
            continue  # Not a private key
        if config.LockValue != 0x55:
            # Data zone is already locked, additional conditions apply
            skip_msg = '    Skipping key pair generation in slot {}: '.format(slot)
            if not config.SlotConfig[slot].WriteConfig & 0x02:
                print(skip_msg + 'GenKey is disabled')
                continue
            if not config.SlotLocked & (1 << slot):
                print(skip_msg + 'Slot has ben locked')
                continue
            if config.KeyConfig[slot].ReqAuth:
                print(skip_msg + 'Slot requires authorization')
                continue
            if config.KeyConfig[slot].PersistentDisable:
                print(skip_msg + 'Slot requires persistent latch')
                continue

        print('    Generating key pair in slot {}'.format(slot))
        public_key = bytearray(64)
        assert ATCA_SUCCESS == atcab_genkey(slot, public_key)
        print(public_key)
        print(convert_ec_pub_to_pem(public_key))





def parse_interface_params(list):
    """
    Parse a variable list of key=value args into a dictionary suitable for kwarg usage
    """
    return {} if list is None else dict([s.split('=') for s in list])


def pretty_print_hex(a, l=16, indent=''):
    """
    Format a list/bytes/bytearray object into a formatted ascii hex string
    """
    lines = []
    a = bytearray(a)
    for x in range(0, len(a), l):
        lines.append(indent + ' '.join(['{:02X}'.format(y) for y in a[x:x+l]]))
    return '\n'.join(lines)


def convert_ec_pub_to_pem(raw_pub_key):
    """
    Convert to the key to PEM format. Expects bytes
    """
    public_key_der = bytearray.fromhex('3059301306072A8648CE3D020106082A8648CE3D03010703420004') + raw_pub_key
    public_key_b64 = base64.b64encode(public_key_der).decode('ascii')
    public_key_pem = (
        ''.join(public_key_b64[i:i + 64] for i in range(0, len(public_key_b64), 64))
    )
    return public_key_pem





            

if __name__ == '__main__':

    
    print('\nConfiguring the device with base configuration')
    configure_device()
    print('\nDevice Successfully Configured')