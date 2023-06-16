Instructions:

- Open your desired minecraft version (from the "version" folder) .jar file with a zip program;
- Extract the "recipes" folder from inside ```data\minecraft``` into the "advancements" datapack folder (where the python script is located) and rename it "recipes2";
- Extract the "recipes" folder from inside ```data\minecraft\advancements``` into the same datapack folder;
- Open the terminal from inside the datapack folder and run the script with ```python convert_recipes.py``` (pyhton3 if you are on linux);
- Delete the "recipes2" folder.

Note: make sure use the terminal to run the script from the correct directory, if you have a subfolder named ```recipes``` in the location you are executing the script from (for example your home directory if you open the script directly with VScode and use Code Runner), every .json file present there will be overwitten!

The script will change every item recipe advancement to this:
```
{
    "parent":"minecraft:recipes/root",
    "criteria":{
        "has_ingredients":{
            "trigger":"minecraft:inventory_changed",
            "conditions":{
                "items":[
                    {
                        (required_items)
                    }
                ]
            }
        }
    },
    "requirements":[
        [
            "has_ingredients"
        ]
    ],
    "rewards":{
        "recipes":[
            "minecraft:item_name"
        ]
    }
}
```

And that's it, the datapack is ready! The script should also work with future versions of the game (except if they change the recipe and advancement structure). You can change the ```pack_format``` version from the ```pack.mcmeta``` file if you don't want to get a warning when selecting the datapack.
