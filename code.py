# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: Copyright 2025 Sam Blenny
#

# Test 1: Connect to gamepad and poll rapidly for input events. Combining this
# with trying to write a file to CIRCUITPY may crash the board.
if False:
    import test_1
    test_1.run()

# Test 2: Repeatedly call usb.core.find() and check for any changes to the
# device descriptor details of the devices it finds.
if True:
    import test_2
    test_2.run()
