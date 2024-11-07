""" Common helper functions for cryptoauthlib examples """
import argparse
import os
import base64
import sys
from cryptoauthlib import *
from common import *


# Maps common name to the specific name used internally
atca_names_map = {'i2c': 'i2c', 'hid': 'kithid', 'sha': 'sha20x', 'ecc': 'eccx08'}

try:
    FileNotFoundError
except NameError:
    FileNotFoundError = IOError


def setup_example_runner(module):
    """
    Common helper function that sets up the script entry for all examples
    """

    parser = argparse.ArgumentParser(description=details, 
                                 formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument('-i', '--iface', default='hid', choices=['i2c', 'hid'], help='Interface type (default: hid)')
    parser.add_argument('-d', '--device', default='ecc', choices=['ecc', 'sha'], help='Device type (default: ecc)')
    parser.add_argument('-p', '--params', nargs='*', help='Interface Parameters in the form key=value')

    return parser


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
        '-----BEGIN PUBLIC KEY-----\n'
        + '\n'.join(public_key_b64[i:i + 64] for i in range(0, len(public_key_b64), 64)) + '\n'
        + '-----END PUBLIC KEY-----'
    )
    return public_key_pem


def check_if_rpi():
    """
    Does a basic check to see if the script is running on a Raspberry Pi
    """
    is_rpi = False
    try:
        with open('/sys/firmware/devicetree/base/model', 'r') as f:
            if f.readline().startswith('Raspberry'):
                is_rpi = True
    except FileNotFoundError:
        is_rpi = False

    return is_rpi














def info(iface='hid', device='ecc', **kwargs):
    ATCA_SUCCESS = 0x00

    # Get the target default config
    cfg = eval('cfg_at{}a_{}_default()'.format(atca_names_map.get(device), atca_names_map.get(iface)))

    # Set interface parameters
    if kwargs is not None:
        for k, v in kwargs.items():
            icfg = getattr(cfg.cfg, 'atca{}'.format(iface))
            setattr(icfg, k, int(v, 16))

    # Basic Raspberry Pi I2C check
    if 'i2c' == iface and check_if_rpi():
        cfg.cfg.atcai2c.bus = 1

    # Initialize the stack
    assert atcab_init(cfg) == ATCA_SUCCESS
    print('')

    # Request the Revision Number
    info = bytearray(4)
    assert atcab_info(info) == ATCA_SUCCESS
    print('\nDevice Part:')
    print('    ' + get_device_name(info))

    # Request the Serial Number
    serial_number = bytearray(9)
    assert atcab_read_serial_number(serial_number) == ATCA_SUCCESS
    print('\nSerial number: ')
    print(pretty_print_hex(serial_number, indent='    '))

    # Read the configuration zone
    config_zone = bytearray(128)
    assert atcab_read_config_zone(config_zone) == ATCA_SUCCESS

    print('\nConfiguration Zone:')
    print(pretty_print_hex(config_zone, indent='    '))

    # Check the device locks
    print('\nCheck Device Locks')
    is_locked = AtcaReference(False)
    assert atcab_is_locked(0, is_locked) == ATCA_SUCCESS
    config_zone_locked = bool(is_locked.value)
    print('    Config Zone is %s' % ('locked' if config_zone_locked else 'unlocked'))

    assert atcab_is_locked(1, is_locked) == ATCA_SUCCESS
    data_zone_locked = bool(is_locked.value)
    print('    Data Zone is %s' % ('locked' if data_zone_locked else 'unlocked'))

    # Load the public key
    if data_zone_locked:
        print('\nLoading Public key\n')
        public_key = bytearray(64)
        assert atcab_get_pubkey(0, public_key) == ATCA_SUCCESS
        print(convert_ec_pub_to_pem(public_key))

    # Free the library
    atcab_release()



if __name__ == '__main__':
    parser = setup_example_runner(__file__)
    args = parser.parse_args()

    info(args.iface, args.device, **parse_interface_params(args.params))
    print('\nDone')