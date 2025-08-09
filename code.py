# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: Copyright 2025 Sam Blenny
#
import displayio
import gc
import usb
from usb.core import USBError, USBTimeoutError


def test_descriptor_parsing_no_config():
    # Check USB device descriptors without activating any configurations
    print("Finding USB devices...")
    try:
        for device in usb.core.find(find_all=True):
            print(f"idVendor      {device.idVendor:04x}")
            print(f"idProduct     {device.idProduct:04x}")
            print(f"serial_number {device.serial_number}")
            print(f"product       {device.product}")
            print(f"manufacturer  {device.manufacturer}")
            print(f"speed         {device.speed}")
    except USBError as e:
        print(f"USBError: .errno={e.errno} string={str(e)}")
        print(e)
    except USBTimeoutError as e:
        print(f"USBError: .errno={e.errno} string={str(e)}")
        print(e)


displayio.release_displays()
gc.collect()

while True:
    print()
    test_descriptor_parsing_no_config()
    print()
    # pause with a prompt to avoid rapidly scrolling serial console output
    input("press Enter to try again: ")
