import socket

services = {
    22: "SSH",
    80: "HTTP",
    443: "HTTPS",
    21: "FTP",
    135: "RPC"
}

def port_scanner():
    target = input("Enter target IP: ")

    print(f"\nScanning {target}...\n")

    for port in range(1, 1025):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)

        result = sock.connect_ex((target, port))

        if result == 0:
            if port in services:
                print(f"Port {port} OPEN → {services[port]}")
            else:
                print(f"Port {port} OPEN")

        sock.close()

port_scanner()