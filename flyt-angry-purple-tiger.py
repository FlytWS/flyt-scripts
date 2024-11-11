from angry_purple_tiger import animal_hash

print('Flyt Angry Purple Tiger')

with open('/etc/flyt/publickey') as f:
    print(f.read())
    publickey = f.read()

    name = animal_hash(publickey.encode())

with open("/etc/flyt/wingbits", 'w+') as file:
    file.write(name)