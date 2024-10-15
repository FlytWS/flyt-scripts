import socket, subprocess, sys

def listen(ip,port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((ip, port))
    s.listen(1)
    print("Listening on port " + str(port))
    conn, addr = s.accept()
    print('Connection received from ',addr)

    #Receive data
    ans = conn.recv(1024).decode()
    sys.stdout.write(ans)

    if ans == "flyt-wifi-manage":
        print("Running Flyt-WiFi-Manage")
        subprocess.call(['python3', '/etc/flyt/scripts/flyt-wifi-manage.py'])

    if ans == "flyt-wifi-scan":
        print("Running Flyt-WiFi-Scan")
        subprocess.call(['python3', '/etc/flyt/scripts/flyt-wifi-scan.py'])

    if ans == "flyt-wifi-active":
        print("Running Flyt-WiFi-Active")
        subprocess.call(['python3', '/etc/flyt/scripts/flyt-wifi-active.py'])

    s.close()

while True:
    listen("127.0.0.1",65432)