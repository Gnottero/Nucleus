#> Nucleus by Gnottero <#

#> This is a very simple script that generates a datapack template that follows all the conventions <#

#> Importing all the required libraries <#
import os
import requests

#> Setupping the variables <#
dev_name = input('Please insert your name (Minecraft Username): ')
dp_name = input('Please insert your datapack name: ')
dp_item = input('Please insert the id of the item that will be displayed in the advancement: ')
dp_desc = input('Please insert the description of the datapack: ')
namespace = dp_name.replace(" ", "_").lower()


#> Requesting player data from the Mojang API <#
uuid_rq = requests.get(f'https://api.mojang.com/users/profiles/minecraft/{dev_name}')
player_uuid = uuid_rq.json()['id']
skull_value_rq = requests.get(f'https://sessionserver.mojang.com/session/minecraft/profile/{player_uuid}')
skull_value = skull_value_rq.json()['properties'][0]['value']

#> Starting the generation phase <#

g_adv_path = f"./{dp_name}/data/global/advancements"
dp_adv_path = f"./{dp_name}/data/{dev_name.lower()}/advancements/{namespace}"

try:
    os.makedirs(g_adv_path)
except FileExistsError:
    pass

try:
    os.makedirs(dp_adv_path)
except FileExistsError:
    pass


with open(f'./{dp_name}/pack.mcmeta', 'w') as f:
    f.write(f'''
{{
    "pack": {{
        "pack_format": 5,
        "description": "{dp_desc} by {dev_name}"
    }}
}}
    '''
    )
    
with open(f'{g_adv_path}/root.json', 'w') as f:
    f.write(f'''
{{
    "display": {{
        "title": "Installed Datapacks",
        "description": "",
        "icon": {{
            "item": "minecraft:knowledge_book"
        }},
        "background": "minecraft:textures/block/gray_concrete.png",
        "show_toast": false,
        "announce_to_chat": false
    }},
    "criteria": {{
        "trigger": {{
            "trigger": "minecraft:tick"
        }}
    }}
}}
    '''
    )

with open(f'{g_adv_path}/{namespace}.json', 'w') as f:
    f.write(f'''
{{
    "display": {{
        "title": "{dev_name}",
        "description": "",
        "icon": {{
            "item": "minecraft:player_head",
            "nbt": "{{SkullOwner:{{Name:\\"{dev_name}\\",Properties:{{textures:[{{Value:\\"{skull_value}\\"}}]}}}}}}"
        }},
        "show_toast": false,
        "announce_to_chat": false
    }},
    "parent": "global:root",
    "criteria": {{
        "trigger": {{
            "trigger": "minecraft:tick"
        }}
    }}
}}
    '''
    )

with open(f'{dp_adv_path}/{namespace}.json', 'w') as f:
    f.write(f'''
{{
    "display": {{
        "title": "{dp_name.title()}",
        "description": "{dp_desc}",
        "icon": {{
            "item": "minecraft:{dp_item}"
        }},
        "announce_to_chat": false,
        "show_toast": false
    }},
    "parent": "global:{namespace}",
    "criteria": {{
        "trigger": {{
            "trigger": "minecraft:tick"
        }}
    }}
}}
    '''
    )


print(f''' 
Template generated successfully with the following info:
    
    Datapack developer: {dev_name}
    Datapack name: {dp_name}
    Datapack namespace: {namespace}
    Datapack item: minecraft:{dp_item}
    Datapack description: {dp_desc}
'''
)
