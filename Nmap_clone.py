open_ports = [22, 443]

def scan_ports(open_ports):
    for i in range(1, 1025):
        if i in open_ports:
            print(f"Port {i} open")

        else:
            print(f"Port {i} closed")

scan_ports(open_ports)


