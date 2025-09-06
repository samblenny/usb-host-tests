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
                # If it's already in the cache, skip this device
                key_ = tuple(desc)
                if key_ in cache:
                    continue
                # Otherwise, print properties and cache descriptor
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
