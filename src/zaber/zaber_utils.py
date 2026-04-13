"""Utilities to assist with controlling zaber motors."""

import asyncio
import logging
import time

from zaber_motion import CommandPreemptedException, Units
from zaber_motion.binary import BinarySettings, CommandCode, Connection
from zaber_motion.binary.device import Device

MAX_SPEED_ERROR = "Parameter max_speed must be greater than zero."
"""_summary_"""
RUNTIME_EXISTS_ERROR = "Active asyncio event loop exists. Use async version."
"""_summary_"""

_logger = logging.getLogger(__name__)


def get_devices(
    conn: Connection,
    *,
    timeout: float = 0.5,
    retries: int = 3,
) -> list[Device]:

    conn.generic_command_no_response(0, CommandCode.STOP)

    devices = None
    error = BaseException
    for _ in range(retries):
        try:
            devices = conn.detect_devices()
            break
        except CommandPreemptedException as err:
            time.sleep(timeout)
            error = err
    if devices is None:
        raise error
    return devices


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
        await asyncio.gather(
            *[
                device.settings.set_async(
                    BinarySettings.HOME_SPEED,
                    value=max_speed,
                    unit=unit,
                )
                for device in devices
            ],
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
        _ = asyncio.get_running_loop()
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


async def move_stepped(device: Device) -> None:
    pass
