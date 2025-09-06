# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: Copyright 2025 Sam Blenny
#
import displayio
import gc
import usb
import time
from usb.core import USBError, USBTimeoutError


def test_unplug_during_find():
    # This tests how repeated calls to usb.core.find() behave in the
    # context of unplugging a USB device.
    cache = {}
    print("Finding USB devices...")
    while True:
        try:
            for device in usb.core.find(find_all=True):
                # Read 18 byte device descriptor
                desc = bytearray(18)
                device.ctrl_transfer(0x80, 6, 0x01 << 8, 0, desc, 300)
                # Validate descriptor
                key_ = tuple(desc)
                all_zero = all([b==0 for b in desc])
                if all_zero:
                    # Got bad data
                    print("bad data:", key_)
                    continue
                elif key_ in cache:
                    # Descriptor is valid but cached, skip device
                    continue
                # Otherwise, print properties and add to cache
                cache[key_] = True
                print_descriptor_properties(device)
                print(cache)
        except USBTimeoutError as e:
            print("USBTimeoutError: '%s'" % str(e))
        except USBError as e:
            print(f"USBError: '%s'; clear cache, sleep 20ms" % str(e))
            cache.clear()
            # This delay allows TinyUSB to recover from failures
            time.sleep(0.02)

def print_descriptor_properties(device):
    print()
    print(f"idVendor      {device.idVendor:04x}")
    print(f"idProduct     {device.idProduct:04x}")
    print(f"product       {device.product}")
    print(f"manufacturer  {device.manufacturer}")

def run():
    displayio.release_displays()
    gc.collect()
    test_unplug_during_find()
