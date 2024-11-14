from smbus2 import SMBus
import time

class I2CScanner:
    def __init__(self, bus_number):
        self.bus_number = bus_number
        self.bus = SMBus(bus_number)

    def scan(self):
        found_addresses = []
        for address in range(0x03, 0x78):  
            try:
                self.bus.write_byte(address, 0)  
                found_addresses.append(address) 
            except:
                pass  
        return found_addresses