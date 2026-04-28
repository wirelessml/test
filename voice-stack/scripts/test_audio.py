"""Audio device test"""
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

import sounddevice as sd

devs = sd.query_devices()
print(f"Total devices: {len(devs)}")
print()
for d in devs:
    if d["max_input_channels"] > 0:
        print(f"  [INPUT  {d['index']:2d}] {d['name']} (ch={d['max_input_channels']}, sr={int(d['default_samplerate'])})")

print()
default_in = sd.default.device[0]
print(f"Default input device: {default_in}")
