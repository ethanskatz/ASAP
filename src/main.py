"""_summary_."""

from zaber_motion.binary import Connection

from .zaber.zaber_utils import auto_home

if __name__ == "__main__":
    with Connection.open_serial_port("/dev/ttyUSB0") as conn:
        devices = conn.detect_devices()
        devices_to_home = devices[1:5]
        auto_home(devices=devices_to_home)
