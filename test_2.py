# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: Copyright 2025 Sam Blenny
#
import displayio
import gc
import usb
from usb.core import USBError, USBTimeoutError


def test_unplug_during_find():
    # This tests how repeated calls to usb.core.find() behave in the context of
    # unplugging a USB device. Initially, before a device is plugged in for the
    # first time, the generator produces no iterator items. When you plug in a
    # device, it will produce one item, usually with a valid descriptor. When
    # you unplug that device, find() breaks and starts always yielding one item
    # with an all-zeros descriptor. It keeps doing that if you plug the device
    # back in.
    cache = {}
    print("Finding USB devices...")
    consecutive_all_zeros = 0
    while True:
        try:
            valid_devices = 0
            for device in usb.core.find(find_all=True):
                # 1. Read device descriptor
                desc = get_desc(device, 0x01, length=18)
                # 2. Check if descriptor is all zeros. This happens when I
                #    unplug a device while find() is active. In that case, as
                #    long as no devices are plugged in, find()'s generator will
                #    always provide 1 device with an all-zero descriptor.
                if all((byte_==0 for byte_ in desc)):
                    consecutive_all_zeros += 1
                    if consecutive_all_zeros % 50 == 1:
                        print("Consecutive all zero descriptor count",
                            consecutive_all_zeros)
                    continue
                else:
                    consecutive_all_zeros = 0
                    valid_devices += 1
                # 3. If it's already in the cache, skip device
                key_ = tuple(desc)
                if key_ in cache:
                    continue
                # 3. Otherwise, print properties and cache descriptor
                cache[key_] = True
                print_descriptor_properties()
                print(cache)
            if valid_devices == 0 and len(cache) > 0:
                # find() found no devices, so clear cache
                print("Clearing Cache")
                cache.clear()
        except USBError as e:
            print(f"find USBError: .errno={e.errno} '{str(e)}'")
        except USBTimeoutError as e:
            print(f"find USBError: .errno={e.errno} '{str(e)}'")

def get_desc(device, desc_type, length=256):
    # Read USB descriptor of type specified by desc_type (wIndex always 0).
    data = bytearray(length)
    bmRequestType = 0x80
    wValue = desc_type << 8
    wIndex = 0
    device.ctrl_transfer(bmRequestType, 6, wValue, wIndex, data, 300)
    return data

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
