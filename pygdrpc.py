from pypresence import Presence
import time
import gd
import asyncio
import os
version = "1.1.1"

print(f"PyGDRPC v{version} \n\t Starting...")
try:
    memory = gd.memory.get_memory()
except RuntimeError:
    print("Open Geometry Dash before running this!")
    os.system("PAUSE")

smallimage = "none" # fallback in case of the difficulty face not being returned
client = gd.Client()
scenev = memory.get_scene_value()
scene = memory.get_scene()
ltypev = memory.get_level_type_value()
ltype = memory.get_level_type()
iseditor = memory.is_in_editor()
name = memory.get_level_name()
client_id = '703049428822655048'
RPC = Presence(client_id)

print("\t Connecting...")
try:
    RPC.connect()
except:
    print("Failed to connect to discord, try reopening it?")
else:
    print("Connected successfully!")

async def get_difficulty(level: gd.Level) -> str:
    try:
        level = await client.get_level(id)
    except gd.MissingAccess:
        editorlevel = True
    else:
        editorlevel = False
        base = level.difficulty.name.lower().split('_')
        if level.is_epic():
            base.append("epic")
        elif level.is_featured():
            base.append("featured")
        return '-'.join(base)

async def run():
    memory.reload()
    percent = memory.get_normal_percent()
    if percent == 0:
        percent = "   "
    else:
        percent = "(" + str(percent) + "%)"
    if scenev == 3 and iseditor == False and ltypev == 3:
        id = memory.get_level_id()
        smallimage = asyncio.run(get_difficulty(id))
        RPC.update(pid=memory.process_id, state=str(f"{name} {percent}"), details="Playing a level.", large_image="gd", small_image=asyncio.run(get_difficulty(id)))
    if scenev == 3 and iseditor and ltypev != 2:
        RPC.update(pid=memory.process_id, details="In the editor.", large_image="gd")
    if scenev == 3 and iseditor == False and ltypev == 2:
        RPC.update(pid=memory.process_id, state=str(f"{name} {percent}"), details="Playing an editor level.", large_image="gd")
    else:
        if scenev != 3 and iseditor == False and ltypev != 2 and ltypev != 3 and ltypev != 1 or percent == "   " or None and scenev != 4:
            RPC.update(pid=memory.process_id, state="     ", details="In the menu.", large_image="gd")
        else:
            if scenev == 9 and ltypev == 1:
                smallimage = asyncio.run(get_difficulty(id))
                RPC.update(pid=memory.process_id, state="     ", details="Playing an official level.", large_image="gd", small_image=smallimage)

input("\t \t Press [ENTER] to start!")

while True:
    asyncio.run(run())
    time.sleep(5)
