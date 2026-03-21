import platform

def get_system_info():
    return {
        "system": platform.system(),
        "architecture": platform.machine()
    }
