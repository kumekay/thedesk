import gc

import neopixel
from machine import PWM, Pin
import uasyncio as asyncio
from button import PushButton


gc.collect()

EN_L = Pin(27, Pin.OUT)
EN_R = Pin(25, Pin.OUT)
PWM_L = Pin(32, Pin.OUT)
PWM_R = Pin(26, Pin.OUT)
BUTTON_DOWN = Pin(18, Pin.IN, Pin.PULL_UP)
BUTTON_UP = Pin(19, Pin.IN, Pin.PULL_UP)

PIXEL_PIN = Pin(33, Pin.OUT)
PIXEL = neopixel.NeoPixel(PIXEL_PIN, 1)


def move(up=False, speed=100):
    if up:
        PWM_L.on()
        PWM_R.off()
    else:
        PWM_L.off()
        PWM_R.on()


def stop():
    PWM_L.off()
    PWM_R.off()


async def main():
    # Enable motors
    EN_L.on()
    EN_R.on()

    button_down = PushButton(BUTTON_DOWN)
    button_down.press_func(move, (False,))
    button_down.release_func(stop)

    button_up = PushButton(BUTTON_UP)
    button_up.press_func(move, (True,))
    button_up.release_func(stop)

    # Keep alive
    while True:
        await asyncio.sleep(1)


try:
    asyncio.run(main())
except (KeyboardInterrupt, Exception) as e:
    print("Exception {}".format(e))
finally:
    asyncio.new_event_loop()
