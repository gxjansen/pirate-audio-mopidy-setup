#!/usr/bin/env python3
import signal
import RPi.GPIO as GPIO
import requests
import json
import sys
import time

print("Pirate Audio Button Controller with Cleanup")

# Mopidy JSON-RPC endpoint
MOPIDY_URL = 'http://localhost:6680/mopidy/rpc'

# The buttons on Pirate Audio are connected to pins 5, 6, 16 and 24
BUTTONS = [5, 6, 16, 24]
LABELS = ['A', 'B', 'X', 'Y']

def cleanup_gpio():
    """Clean up GPIO before setup"""
    try:
        GPIO.cleanup()
        print("GPIO cleaned up")
    except:
        pass
    time.sleep(0.5)

def setup_gpio():
    """Setup GPIO pins"""
    # Set up RPi.GPIO with the "BCM" numbering scheme
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(BUTTONS, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    print("GPIO setup complete")

def mopidy_call(method, params=None):
    """Send RPC call to Mopidy"""
    payload = {'method': method, 'jsonrpc': '2.0', 'id': 1}
    if params:
        payload['params'] = params
    
    try:
        response = requests.post(MOPIDY_URL, 
                               headers={'Content-Type': 'application/json'}, 
                               data=json.dumps(payload), 
                               timeout=2)
        result = response.json()
        return result.get('result')
    except Exception as e:
        print(f"Mopidy call failed: {e}")
        return None

def handle_button(pin):
    label = LABELS[BUTTONS.index(pin)]
    print(f"Button {label} pressed!")
    
    if label == 'A':  # Play/Pause
        state = mopidy_call('core.playback.get_state')
        if state == 'playing':
            mopidy_call('core.playback.pause')
            print("Paused")
        else:
            mopidy_call('core.playback.play')
            print("Playing")
    
    elif label == "B":  # Previous
        mopidy_call("core.playback.previous")
        print("Previous track")
    
    elif label == "X":  # Next
        mopidy_call("core.playback.next")
        print("Next track")
    
    elif label == 'Y':  # Volume toggle
        volume = mopidy_call('core.mixer.get_volume')
        if volume:
            new_vol = 70 if volume < 60 else 50
            mopidy_call('core.mixer.set_volume', [new_vol])
            print(f"Volume set to {new_vol}%")

def cleanup_and_exit(signum, frame):
    print("\nCleaning up GPIO and exiting...")
    GPIO.cleanup()
    sys.exit(0)

# Set up signal handlers
signal.signal(signal.SIGINT, cleanup_and_exit)
signal.signal(signal.SIGTERM, cleanup_and_exit)

print("A=Play/Pause, B=Previous, X=Next, Y=Volume Toggle")

# Clean up first, then setup
cleanup_gpio()
setup_gpio()

# Attach button event handlers
for pin in BUTTONS:
    GPIO.add_event_detect(pin, GPIO.FALLING, handle_button, bouncetime=200)

print("Button controller ready. Waiting for button presses...")

# Keep the script running
try:
    signal.pause()
except KeyboardInterrupt:
    cleanup_and_exit(None, None)
