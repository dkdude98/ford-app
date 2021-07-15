import asyncio
from aiohttp import ClientSession
import pymyq

async def main(email, password) -> None:
    """Create the aiohttp session and run."""
    async with ClientSession() as websession:
      myq = await pymyq.login(email, password, websession)

      # Return only garage devices:
      devices = myq.covers
      garages=[None]*(len(devices))
      if len(devices) != 0:
        for idx, device_id in enumerate(
          device_id
          for device_id in devices):
            device = devices[device_id]
            garages[idx] = [device.device_id,device.online,device.state]
            #await device.close()
      return garages

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


#loop = asyncio.get_event_loop().run_until_complete(main('dak190@pitt.edu','dkdude123?'))
#print(loop.name)
#store_device.open()