from abc import ABC, abstractmethod


class EngineInterface(ABC):

    @abstractmethod
    def load_firmware(self, firmware_path):
        pass

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def pause(self):
        pass

    @abstractmethod
    def resume(self):
        pass

    @abstractmethod
    def reset(self):
        pass

    @abstractmethod
    def stop(self):
        pass

    @abstractmethod
    def get_cpu_state(self):
        pass

    @abstractmethod
    def get_hardware_state(self):
        pass

    @abstractmethod
    def set_gpio_input(self, pin, value):
        pass

    @abstractmethod
    def get_status(self):
        pass