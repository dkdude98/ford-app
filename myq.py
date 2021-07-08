import asyncio
from aiohttp import ClientSession
import pymyq


async def main() -> None:
    """Create the aiohttp session and run."""
    async with ClientSession() as websession:
      myq = await pymyq.login('dak190@pitt.edu', 'dkdude123?', websession)

      # Return only cover devices:
      devices = myq.covers
      # >>> {"serial_number123": <Device>}

      # Return only lamps devices:
     # devices = myq.lamps
      # >>> {"serial_number123": <Device>}

      # Return only gateway devices:
      # devices = myq.gateways
      # >>> {"serial_number123": <Device>}

      # Return *all* devices:
      # devices = myq.devices
      # >>> {"serial_number123": <Device>, "serial_number456": <Device>}
      if len(devices) != 0:
        for idx, device_id in enumerate(
          device_id
          for device_id in devices):
            device = devices[device_id]
            store_device = device
            return store_device.name
            print_info(number=idx, device=device)
            #await device.close()

      #CG0846184923

def print_info(number: int, device):
    print(f"      Device {number + 1}: {device.name}")
    print(f"      Device Online: {device.online}")
    print(f"      Device ID: {device.device_id}")
    print(
        f"      Parent Device ID: {device.parent_device_id}",
    )
    print(f"      Device Family: {device.device_family}")
    print(
        f"      Device Platform: {device.device_platform}",
    )
    print(f"      Device Type: {device.device_type}")
    print(f"      Firmware Version: {device.firmware_version}")
    print(f"      Open Allowed: {device.open_allowed}")
    print(f"      Close Allowed: {device.close_allowed}")
    print(f"      Current State: {device.state}")
    print("      ---------")


asyncio.get_event_loop().run_until_complete(main())

#store_device.open()