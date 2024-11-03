from angry_purple_tiger import animal_hash

with open('/etc/flyt/publickey') as f:
    print(f.read())
    publickey = f.read()

    name = animal_hash('112CuoXo7WCcp6GGwDNBo6H5nKXGH45UNJ39iEefdv2mwmnwdFt7'.encode())

with open("/etc/flyt/wingbits", 'w+') as file:
    file.write(name)