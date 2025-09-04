# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: Copyright 2025 Sam Blenny
#
import displayio
import gc
import time
import usb
from usb.core import USBError, USBTimeoutError


def test_descriptor_parsing_read_gamepad():
    # Check USB device descriptors, then read from gamepad if found.
    # This one is designed to trigger bugs where an in progress USB transaction
    # fights with other CircuitPython tasks. For me, this reliably triggers a
    # board reset with 10.0.0-beta.2, Fruit Jam rev D, and an 8BitDo SN30 Pro
    # wired gamepad (XInput style) or the Adafruit generic SNES style gamepad.
    # To trigger bug, attempt to write a file to CIRCUITPY once you see the
    # "Reading gamepad input..." message.
    gamepad_vid_pid_map = {
        # ( vid,    pid): (max_packet, sleep_before_read, description)
        (0x081f, 0xe401): (8, True, "Adafruit generic SNES style (HID)"),
        (0x045e, 0x028e): (32, False, "Xbox 360 compatible (XInput)"),
    }
    print("Finding USB devices...")
    try:
        for device in usb.core.find(find_all=True):
            # 1. Print descriptor properties
            vid = device.idVendor
            pid = device.idProduct
            print(f"idVendor      {vid:04x}")
            print(f"idProduct     {pid:04x}")
            print(f"serial_number {device.serial_number}")
            print(f"product       {device.product}")
            print(f"manufacturer  {device.manufacturer}")
            print(f"speed         {device.speed}")
            # 2. Configure interface for known gamepads (skip other devices)
            try:
                if not ((vid, pid) in gamepad_vid_pid_map):
                    print(" skipping this one (not a known gamepad)")
                    continue
                max_packet = gamepad_vid_pid_map[(vid,pid)][0]
                sleep_before_read = gamepad_vid_pid_map[(vid,pid)][1]
                buf = bytearray(max_packet)
                interface = 0
                if device.is_kernel_driver_active(interface):
                    device.detach_kernel_driver(interface)
                device.set_configuration(interface)
            except USBError as e:
                print(f"conf USBError: .errno={e.errno} '{str(e)}'")
            except USBTimeoutError as e:
                print(f"conf USBTimeoutError: .errno={e.errno} '{str(e)}'")
            # 3. Rapidly poll gamepad for input. Goal of this is to trigger
            #    bugs where an in progress USB transaction fights with other
            #    CircuitPython tasks.
            print("Reading gamepad input...")
            print("Writing a file to CIRCUITPY now will probably reset board")
            while True:
                try:
                    if sleep_before_read:
                        # Adafruit generic SNES gamepad (low speed device) gets
                        # mad and raises USBError if you poll it too quickly
                        time.sleep(0.003)
                    n = device.read(0x81, buf, timeout=10)
                except USBError as e:
                    print(f"read USBError: .errno={e.errno} '{str(e)}'")
                except USBTimeoutError as e:
                    print(f"read USBError: .errno={e.errno} '{str(e)}'")
    except USBError as e:
        print(f"find USBError: .errno={e.errno} '{str(e)}'")
    except USBTimeoutError as e:
        print(f"find USBTimeoutError: .errno={e.errno} '{str(e)}'")


def run():
    displayio.release_displays()
    gc.collect()
    while True:
        # pause with a prompt to avoid rapidly scrolling serial console output
        input("press Enter to begin running test: ")
        print()
        test_descriptor_parsing_read_gamepad()
        print()
