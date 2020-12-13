import os
import asyncio
import json
import aiofiles


async def create_dir(dirpath):
    if not os.path.exists(dirpath):
        os.makedirs(dirpath)
        await asyncio.sleep(0)


async def write_to_json_file(data_object, file_name):
    async with aiofiles.open(file_name, "w") as outfile:
        print(f'Writing "{data_object}" to "{file_name}"...')
        await outfile.write(json.dumps(data_object, indent=4))


async def read_from_json_file(filename):
    data_obj = None
    try:
        async with aiofiles.open(filename, "r") as infile:
            data_obj = await infile.read()
        return json.loads(data_obj) if data_obj else data_obj
    except FileNotFoundError:
        async with aiofiles.open(filename, "w+", encoding="utf-8", errors='ignore', newline='\n') as outfile:
            data_obj = {None}
            await outfile.write(json.dumps(data_obj, indent=4))
            #data_obj = await outfile.read()
            return None



