#> Nucleus by Gnottero <#

#> This is a very simple script that generates a datapack template that follows all the conventions <#

#> Importing all the required libraries <#
import os
import requests
import json

#> Setupping the variables <#
dev_name = input('Please insert your name (Minecraft Username): ')
dp_name = input('Please insert your datapack name: ')
namespace = input('Please insert the name of the namespace: ').replace(" ", "_").lower()
project_name = input('Please insert the project name: ').replace(" ", "_").lower()
dp_item = input('Please insert the id of the item that will be displayed in the advancement: ')
dp_desc = input('Please insert the description of the datapack: ')
main_name = input('Please insert the name of the main function: ').replace(" ", "_").lower()
load_name = input('Please insert the name of the load function: ').replace(" ", "_").lower()


#> Adding default values if the description or the item or the main fun name or the load fun name are not defined <#
if len(project_name) == 0:
    project_name= dp_name.replace(" ", "_").lower()
else:
    pass

if len(namespace) == 0:
    namespace= project_name
else:
    pass

if len(dp_item) == 0:
    dp_item= 'name_tag'
else:
    pass

if len(dp_desc) == 0:
    dp_desc = 'This is the pack description'
else:
    pass

if len(main_name) == 0:
    main_name = 'main'
else:
    pass

if len(load_name) == 0:
    load_name = 'setup'
else:
    pass

#> Requesting player data from the Mojang API <#
uuid_rq = requests.get(f'https://api.mojang.com/users/profiles/minecraft/{dev_name}')
player_uuid = uuid_rq.json()['id']
skull_value_rq = requests.get(f'https://sessionserver.mojang.com/session/minecraft/profile/{player_uuid}')
skull_value = skull_value_rq.json()['properties'][0]['value']

#> Starting the generation phase <#

#> Generating all the needed folder <#
g_adv_path = f"./{dp_name}/data/global/advancements"
dp_adv_path = f"./{dp_name}/data/{namespace}/advancements/{project_name}"
mc_tags_path = f"./{dp_name}/data/minecraft/tags/functions"
dp_tags_path = f"./{dp_name}/data/{namespace}/tags/functions/{project_name}"
dp_fun_path = f"./{dp_name}/data/{namespace}/functions/{project_name}"


def try_mkdir(path):
    try:
        os.makedirs(path)
    except FileExistsError:
        pass

try_mkdir(g_adv_path)   
try_mkdir(dp_adv_path)
try_mkdir(mc_tags_path)
try_mkdir(dp_tags_path)
try_mkdir(dp_fun_path)


def gen_pack_mcmeta(dp_name,dev_name):
    pack = {"pack": {"pack_format": 5,"description": f"{dp_name} by {dev_name}"}}
    with open(f'./{dp_name}/pack.mcmeta', 'w') as f:
        f.write(json.dumps(pack, indent=5, sort_keys=True))


def global_advancements(g_adv_path,namespace,dev_name,skull_value):
    root = {"display": {"title": "Installed Datapacks","description": "","icon": {"item": "minecraft:knowledge_book"},"background": "minecraft:textures/block/gray_concrete.png","show_toast": False,"announce_to_chat": False},"criteria": {"trigger": {"trigger": "minecraft:tick"}}}
    dev = {"display": {"title": f"{dev_name}","description": "","icon": {"item": "minecraft:player_head","nbt": f"{{SkullOwner:{{Name: \"{dev_name}\", Properties: {{textures: [{{Value: \"{skull_value}\"}}]}}}}}}"},"show_toast": False,"announce_to_chat": False},"parent": "global:root","criteria": {"trigger": {"trigger": "minecraft:tick"}}}
    
    with open(f'{g_adv_path}/root.json', 'w') as f:
        f.write(json.dumps(root, indent=5, sort_keys=True))
    with open(f'{g_adv_path}/{namespace}.json', 'w') as f:
        f.write(json.dumps(dev, indent=5, sort_keys=True))


def dp_advancement(dp_adv_path,project_name,dp_name,dp_desc,dp_item):
    dp_adv = {"display": {"title": f"{dp_name.title()}","description": f"{dp_desc}","icon": {"item": f"minecraft:{dp_item}"},"announce_to_chat": False,"show_toast": False},"parent": f"global:{namespace}","criteria": {"trigger": {"trigger": "minecraft:tick"}}}
    with open(f'{dp_adv_path}/{project_name}.json', 'w') as f:
        f.write(json.dumps(dp_adv, indent=5, sort_keys=True))


def mc_tags(mc_tags_path,namespace,project_name):
    mc_load = {"values": [f"#{namespace}:{project_name}/load"]}
    mc_tick = {"values": [f"#{namespace}:{project_name}/loop"]}
    
    with open(f'{mc_tags_path}/load.json', 'w') as f:
        f.write(json.dumps(mc_load, indent=5, sort_keys=True))
    with open(f'{mc_tags_path}/tick.json', 'w') as f:
        f.write(json.dumps(mc_tick, indent=5, sort_keys=True))


def dp_tags(dp_tags_path,namespace,main_name,load_name,project_name):
    ns_load = {"values": [f"{namespace}:{project_name}/{load_name}"]}
    ns_loop = {"values": [f"{namespace}:{project_name}/{main_name}"]}
    
    with open(f'{dp_tags_path}/load.json', 'w') as f:
        f.write(json.dumps(ns_load, indent=5, sort_keys=True))
    with open(f'{dp_tags_path}/loop.json', 'w') as f:
        f.write(json.dumps(ns_loop, indent=5, sort_keys=True))


def dp_fun(dp_fun_path,main_name,load_name):
    with open(f'{dp_fun_path}/{main_name}.mcfunction', 'w') as f:
        f.write('#> This is the main function, that will run once per tick')
    with open(f'{dp_fun_path}/{load_name}.mcfunction', 'w') as f:
        f.write('#> This function will run on datapack loading')



#> Calling all the functions <#
gen_pack_mcmeta(dp_name,dev_name)
global_advancements(g_adv_path,namespace,dev_name,skull_value)
dp_advancement(dp_adv_path,project_name,dp_name,dp_desc,dp_item)
mc_tags(mc_tags_path,namespace,project_name)
dp_tags(dp_tags_path,namespace,main_name,load_name,project_name)
dp_fun(dp_fun_path,main_name,load_name)


print(
    f'''Template generated successfully with the following info:
    
    Datapack developer: {dev_name}
    Datapack name: {dp_name}
    Datapack namespace: {namespace}
    Datapack item: minecraft:{dp_item}
    Datapack description: {dp_desc}

'''
)