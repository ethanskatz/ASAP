"""_summary_."""

from zaber_motion import Units
from zaber_motion.binary import BinarySettings, Connection

from .zaber.zaber_utils import auto_home, get_devices


def _placeholder_apply_configs() -> None:
    pass


del auto_home


def main() -> None:
    # Read config.json and save settings
    with Connection.open_serial_port("/dev/cu.usbserial-AB0LDNKK") as conn:
        devices = get_devices(conn)

        _placeholder_apply_configs()
        devices_to_home = devices[1:5]
        print(
            devices_to_home[3].settings.get(
                BinarySettings.HOME_SPEED,
                unit=Units.VELOCITY_MILLIMETRES_PER_SECOND,
            ),
        )
        # auto_home(devices=devices_to_home)


if __name__ == "__main__":
    main()
