import argparse
import socket
import time
from concurrent.futures import ThreadPoolExecutor, as_completed


def parse_port_range(port_range):
    """Convert a port range like 1-1000 into two integers."""
    try:
        start_port, end_port = map(int, port_range.split("-"))

        if not 1 <= start_port <= 65535:
            raise ValueError

        if not 1 <= end_port <= 65535:
            raise ValueError

        if start_port > end_port:
            raise ValueError

        return start_port, end_port

    except ValueError:
        raise argparse.ArgumentTypeError(
            "Port range must look like 1-1000 and contain valid ports."
        )


def get_service(port):
    """Return the common TCP service associated with a port."""
    try:
        return socket.getservbyport(port, "tcp").upper()
    except OSError:
        return "UNKNOWN"


def scan_port(target, port, timeout):
    """Check whether a TCP port is open."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)

            result = sock.connect_ex((target, port))

            if result == 0:
                return port, get_service(port)

    except OSError:
        pass

    return None


def scan_target(target, start_port, end_port, timeout, threads):
    """Scan a target across the requested TCP port range."""
    open_ports = []

    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = [
            executor.submit(scan_port, target, port, timeout)
            for port in range(start_port, end_port + 1)
        ]

        for future in as_completed(futures):
            result = future.result()

            if result:
                open_ports.append(result)

    return sorted(open_ports)


def main():
    parser = argparse.ArgumentParser(
        description="Simple multithreaded TCP port scanner."
    )

    parser.add_argument(
        "target",
        help="IP address or hostname to scan"
    )

    parser.add_argument(
        "--ports",
        type=parse_port_range,
        default=(1, 1024),
        metavar="START-END",
        help="Port range to scan (default: 1-1024)"
    )

    parser.add_argument(
        "--timeout",
        type=float,
        default=0.5,
        help="Connection timeout in seconds (default: 0.5)"
    )

    parser.add_argument(
        "--threads",
        type=int,
        default=100,
        help="Number of worker threads (default: 100)"
    )

    args = parser.parse_args()

    try:
        target_ip = socket.gethostbyname(args.target)
    except socket.gaierror:
        print(f"Error: Could not resolve '{args.target}'.")
        return

    start_port, end_port = args.ports

    print(f"\nScanning {args.target} ({target_ip})")
    print(f"Ports: {start_port}-{end_port}\n")

    start_time = time.time()

    open_ports = scan_target(
        target_ip,
        start_port,
        end_port,
        args.timeout,
        args.threads
    )

    if open_ports:
        print(f"{'PORT':<10}{'STATE':<10}{'SERVICE'}")
        print("-" * 30)

        for port, service in open_ports:
            print(f"{port:<10}{'OPEN':<10}{service}")

    else:
        print("No open ports discovered.")

    elapsed_time = time.time() - start_time

    print(f"\nScan completed in {elapsed_time:.2f} seconds")
    print(f"{len(open_ports)} open port(s) discovered")


if __name__ == "__main__":
    main()
