# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: Copyright 2025 Sam Blenny

.PHONY: sync tty

# Sync current code to CIRCUITPY drive (macOS only)
sync:
	@cp -X code.py test_*.py /Volumes/CIRCUITPY; sync

# Serial terminal (macOS only): 115200 baud, no flow control (-fn)
tty:
	@if [ -e /dev/tty.usbmodem* ]; then \
		screen -h 9999 -fn /dev/tty.usbmodem* 115200; fi
