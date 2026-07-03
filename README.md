# Windows Wake-on-LAN

Remotely power on a Windows PC from another device on the same network (or over
the internet with router port-forwarding) by sending a Wake-on-LAN "magic packet".

## 1. One-time setup on the target Windows PC

Wake-on-LAN only works if the PC's hardware and OS are configured to listen for
the magic packet while powered off.

1. **BIOS/UEFI**: enable "Wake on LAN" / "Power On by PCI-E/PCIe" (name varies
   by motherboard vendor).
2. **Disable Fast Startup** (Windows hybrid shutdown can block WoL):
   Control Panel → Power Options → "Choose what the power buttons do" →
   uncheck "Turn on fast startup".
3. **Network adapter settings**: Device Manager → Network adapters → your
   adapter → Properties →
   - Advanced tab: enable "Wake on Magic Packet" (and "Wake on Pattern Match"
     if present).
   - Power Management tab: check "Allow this device to wake the computer" and
     "Only allow a magic packet to wake the computer".
4. Note the PC's **MAC address** (`ipconfig /all` on that PC) — you'll need it
   to send the packet.

## 2. Sending the wake packet

From any machine on the same LAN (or with the router configured to forward
UDP port 9 to the broadcast address, for waking over the internet):

```bash
python3 wol.py AA:BB:CC:DD:EE:FF
```

Optional flags:

```bash
python3 wol.py AA:BB:CC:DD:EE:FF --ip 192.168.1.255 --port 9
```

- `--ip`: broadcast address of the target's subnet (default `255.255.255.255`).
  Use the subnet-specific broadcast (e.g. `192.168.1.255`) if your network
  doesn't forward the global broadcast.
- `--port`: UDP port the packet is sent to (default `9`, `7` also common).

## Limitations

- The PC must be in sleep/hibernate/soft-off (plugged into power) — WoL cannot
  turn on a machine that's fully unplugged or hard-powered-off at the PSU.
- Waking over the internet (not just your LAN) requires router port-forwarding
  and a way to know your home's current public IP (e.g. dynamic DNS).
