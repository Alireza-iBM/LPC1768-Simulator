class FakeHardwareAdapter:

    def __init__(self):
        self.connected = False
        self.gpio_pins = {}

    def connect(self):
        self.connected = True

        return {
            "success": True,
            "message": "Fake hardware connected"
        }

    def disconnect(self):
        self.connected = False

        return {
            "success": True,
            "message": "Fake hardware disconnected"
        }

    def set_gpio(self, pin, value):
        if not self.connected:
            return {
                "success": False,
                "message": "Hardware is not connected"
            }

        self.gpio_pins[pin] = bool(value)

        return {
            "success": True,
            "pin": pin,
            "value": self.gpio_pins[pin]
        }

    def read_gpio(self, pin):
        if not self.connected:
            return {
                "success": False,
                "message": "Hardware is not connected"
            }

        return {
            "success": True,
            "pin": pin,
            "value": self.gpio_pins.get(pin, False)
        }

    def get_status(self):
        return {
            "connected": self.connected,
            "gpio_pins": self.gpio_pins
        }