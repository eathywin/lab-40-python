"""Read captured ARM/TAKEOFF; replay original MAVLink bytes only to local SITL."""
import argparse
import hashlib
import socket
import subprocess
import time
from pymavlink.dialects.v20 import common

p = argparse.ArgumentParser(description=__doc__)
p.add_argument('capture')
p.add_argument('--frames', nargs='+', type=int, help='Chosen Wireshark frame numbers')
p.add_argument('--send', action='store_true', help='Send chosen frames to 127.0.0.1 SITL')
a = p.parse_args()
if a.send and not a.frames:
    p.error('--send requires explicit --frames')
cmd = ['tshark', '-r', a.capture, '-Y',
       'udp && !icmp && ip.src == 127.0.0.1 && ip.dst == 127.0.0.1 '
       '&& (udp.dstport == 14580 || udp.dstport == 18570)',
       '-T', 'fields', '-e', 'frame.number', '-e', 'frame.time_epoch',
       '-e', 'udp.dstport', '-e', 'udp.payload']
r = subprocess.run(cmd, capture_output=True, text=True)
if r.returncode:
    raise SystemExit(r.stderr.strip())
found = []
for row in r.stdout.splitlines():
    number, stamp, port, payload = row.split('\t')
    parser = common.MAVLink(None)
    parser.robust_parsing = True
    for message in parser.parse_buffer(bytes.fromhex(payload.replace(':', ''))) or []:
        if message.get_type() not in ('COMMAND_LONG', 'COMMAND_INT'):
            continue
        if message.command != 22 and not (message.command == 400 and message.param1 == 1):
            continue
        raw = bytes(message.get_msgbuf())  # preserves original seq/timestamp/signature
        signed = raw[0] == 0xFD and bool(raw[2] & 1)
        print(f'frame={number} command={message.command} port={port} signed={signed} '
              f'sha256={hashlib.sha256(raw).hexdigest()[:16]}')
        found.append((int(number), float(stamp), int(port), raw))
if not found:
    raise SystemExit('ARM/TAKEOFF not found in this capture. Nothing was sent.')
selected = [x for x in found if a.frames and x[0] in a.frames]
if a.frames and set(a.frames) != {x[0] for x in selected}:
    p.error('Some selected frames are not local captured ARM/TAKEOFF commands')
if not a.send:
    print('Preview only. Signatures were not verified; nothing was sent.')
else:
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        previous = selected[0][1]
        for number, stamp, port, raw in selected:
            time.sleep(max(0, stamp - previous))
            s.sendto(raw, ('127.0.0.1', port))
            previous = stamp
            print(f'Sent original MAVLink bytes from frame {number}; check SITL state/ACK.')
