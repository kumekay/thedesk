import gc

import neopixel
import uasyncio as asyncio
from machine import PWM, Pin

from button import PushButton

gc.collect()

EN_PINS = (
    Pin(27, Pin.OUT),
    Pin(25, Pin.OUT),
)
PWM_PINS = (
    Pin(32, Pin.OUT),
    Pin(26, Pin.OUT),
)
PWMS = [PWM(pin, freq=20000, duty=0) for pin in PWM_PINS]

BUTTON_PINS = (
    Pin(18, Pin.IN, Pin.PULL_UP),  # Down
    Pin(19, Pin.IN, Pin.PULL_UP),  # Up
)


PIXEL_PIN = Pin(33, Pin.OUT)
PIXEL = neopixel.NeoPixel(PIXEL_PIN, 1)

current_duty = 400


def move(up=False):
    for i, pwm in enumerate(PWMS):
        pwm.duty((int(up) ^ i) * current_duty)


def stop():
    for pwm in PWMS:
        pwm.duty(0)


async def main():
    # Enable motors
    for pin in EN_PINS:
        pin.on()

    for i, button_pin in enumerate(BUTTON_PINS):
        button = PushButton(button_pin)
        button.press_func(move, (i,))
        button.release_func(stop)

    # Keep alive
    while True:
        await asyncio.sleep(1)


try:
    asyncio.run(main())
except (KeyboardInterrupt, Exception) as e:
    print("Exception {}".format(e))
finally:
    asyncio.new_event_loop()
