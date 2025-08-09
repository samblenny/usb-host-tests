# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: Copyright 2025 Sam Blenny
#
import test_1

# Test 1: Connect to gamepad and poll rapidly for input events. Combining this
# with trying to write a file to CIRCUITPY may crash the board.
test_1.run()
