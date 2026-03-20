"""Utilities to assist with controlling zaber motors."""

import asyncio

from zaber_motion import Units
from zaber_motion.binary import BinarySettings
from zaber_motion.binary.device import Device

MAX_SPEED_ERROR = "Parameter max_speed must be greater than zero."
"""_summary_"""
RUNTIME_EXISTS_ERROR = "Active asyncio event loop exists. Use async version."
"""_summary_"""


async def auto_home_async(
    devices: list[Device] | Device,
    *,
    max_speed: float | None = None,
    unit: Units = Units.NATIVE,
    timeout: float = Device.DEFAULT_MOVEMENT_TIMEOUT,
) -> list[float]:
    """_summary_.

    :param devices: _description_
    :param max_speed: _description_, defaults to None
    :param unit: _description_, defaults to Units.NATIVE
    :param timeout: _description_, defaults to Device.DEFAULT_MOVEMENT_TIMEOUT
    :raises ValueError: max_speed is non-negative or zero.
    :return: _description_
    """
    if isinstance(devices, Device):
        devices = [devices]

    if max_speed is not None:
        if max_speed <= 0:
            raise ValueError(MAX_SPEED_ERROR)

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
) -> list[float]:
    """_summary_.

    :param devices: _description_
    :param max_speed: _description_, defaults to None
    :param unit: _description_, defaults to Units.NATIVE
    :param timeout: _description_, defaults to Device.DEFAULT_MOVEMENT_TIMEOUT
    :raises ValueError: _description
    :raises RuntimeError: _description_
    :return: _description_
    """
    try:
        asyncio.get_running_loop()
    except RuntimeError:
        return asyncio.run(
            auto_home_async(
                devices=devices,
                max_speed=max_speed,
                unit=unit,
                timeout=timeout,
            ),
        )
    else:
        raise RuntimeError(RUNTIME_EXISTS_ERROR)
