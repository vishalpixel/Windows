#!/usr/bin/env python3
"""Send a Wake-on-LAN magic packet to power on a sleeping/shutdown PC."""
import argparse
import re
import socket
import sys

MAC_RE = re.compile(r"^([0-9A-Fa-f]{2}[:-]){5}[0-9A-Fa-f]{2}$")


def parse_mac(mac: str) -> bytes:
    if not MAC_RE.match(mac):
        raise ValueError(f"Invalid MAC address: {mac!r}")
    return bytes.fromhex(mac.replace(":", "").replace("-", ""))


def build_magic_packet(mac: str) -> bytes:
    mac_bytes = parse_mac(mac)
    return b"\xff" * 6 + mac_bytes * 16


def send_magic_packet(mac: str, ip: str = "255.255.255.255", port: int = 9) -> None:
    packet = build_magic_packet(mac)
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.sendto(packet, (ip, port))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mac", help="Target PC's MAC address, e.g. AA:BB:CC:DD:EE:FF")
    parser.add_argument(
        "--ip",
        default="255.255.255.255",
        help="Broadcast address to send to (default: 255.255.255.255)",
    )
    parser.add_argument("--port", type=int, default=9, help="UDP port (default: 9)")
    args = parser.parse_args()

    try:
        send_magic_packet(args.mac, args.ip, args.port)
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)

    print(f"Magic packet sent to {args.mac} via {args.ip}:{args.port}")


if __name__ == "__main__":
    main()
