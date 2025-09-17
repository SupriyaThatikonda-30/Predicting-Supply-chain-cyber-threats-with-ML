# A simple class to represent the system state (extend this with more data)
class SystemState:
    def __init__(self, cpu_usage, ram_usage, disk_usage):
        self.cpu_usage = cpu_usage
        self.ram_usage = ram_usage
        self.disk_usage = disk_usage
