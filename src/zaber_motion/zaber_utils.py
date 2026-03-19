"""Utilities to assist with controlling zaber motors."""

import asyncio

from zaber_motion import Units
from zaber_motion.binary import BinarySettings, Connection
from zaber_motion.binary.device import Device


async def auto_home_async(
    devices: list[Device] | Device,
    *,
    max_speed: float | None = None,
    unit: Units = Units.NATIVE,
    timeout: float = Device.DEFAULT_MOVEMENT_TIMEOUT,
) -> list[float]:
    """_summary_.

    :param devices: Devices to automatically home
    :param max_speed: _description_, defaults to None
    :param unit: _description_, defaults to Units.NATIVE
    :param timeout: _description_, defaults to Device.DEFAULT_MOVEMENT_TIMEOUT
    :return: _description_
    """
    if isinstance(devices, Device):
        devices = [devices]

    if max_speed:
        for device in devices:
            device.settings.set(
                BinarySettings.HOME_SPEED,
                value=max_speed,
                unit=unit,
            )

    return await asyncio.gather(
        *[device.home_async(unit=unit, timeout=timeout) for device in devices],
    )


def auto_home(
    devices: list[Device] | Device,
    *,
    max_speed: float | None = None,
    unit: Units = Units.NATIVE,
    timeout: float = Device.DEFAULT_MOVEMENT_TIMEOUT,
) -> list[float] | float:
    """_summary_.

    :param devices: _description_
    :param max_speed: _description_, defaults to None
    :param unit: _description_, defaults to Units.NATIVE
    :param timeout: _description_, defaults to Device.DEFAULT_MOVEMENT_TIMEOUT
    :return: _description_
    """
    return asyncio.run(
        auto_home_async(
            devices=devices,
            max_speed=max_speed,
            unit=unit,
            timeout=timeout,
        ),
    )


if __name__ == "__main__":
    with Connection.open_serial_port("/dev/ttyUSB0") as conn:
        devices = conn.detect_devices()
        devices_to_home = devices[1:5]
        auto_home(devices=devices_to_home)
