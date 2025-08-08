import os, json


def extract_ingredients_shapeless(data):
    ingredients = []
    for item in data["ingredients"]:
        if isinstance(item,list):
            #if there is a list the items inside it are funglible, and would need to be put together in the advancement:
            ingredient = {"items":[]}
            for element in item:
                ingredient["items"].append(element["item"])
            ingredients.append(ingredient)
            print(ingredient)
        else:
            ingredient = {}
            if "tag" in item:
                ingredient["tag"] = item["tag"]
            else:
                ingredient["items"] = [item["item"]]
            ingredients.append(ingredient)
            print(ingredient)
    return ingredients


def remove_duplicates(ingredients):
    unique_ingredients = []
    for ingredient in ingredients:
        if ingredient not in unique_ingredients:
            unique_ingredients.append(ingredient)
    return unique_ingredients
    

def extract_ingredients_other(data, item_name, parent=None):
    ingredients = []
    #if it finds an item or tag it will add it to the ingredients, else it will keep searching:
    if isinstance(data, dict):
        for key, value in data.items():
            if (key == "item" or key == "tag") and parent != "result":
                #if the item found is not the result of the recipe it gets added to the ingredients list:
                if(value[10:] != item_name):    #(excluding the "minecraft:" prefix in order to only get the item name)
                    ingredient = [key, value, parent]
                    ingredients.append(ingredient)
                    print(ingredient)
            elif isinstance(value, (dict, list)):
                ingredients.extend(extract_ingredients_other(value, item_name, parent=key))
    elif isinstance(data, list):
        for element in data:
            ingredients.extend(extract_ingredients_other(element, item_name, parent=parent))
    return ingredients


def merge_fungible_ingredients(ingredients_list):
    ingredients_by_symbol = {}
    resulting_list = []
    for type, item, symbol in ingredients_list:
        #if two items have the same symbol in the recipe (for example "#") they will be put together as fungible
        if symbol in ingredients_by_symbol:
            ingredients_by_symbol[symbol][1].append(item)
        else:
            ingredients_by_symbol[symbol] = [type, [item]]
    for values in ingredients_by_symbol.values():
        #the items are finally taken out from the dictionary and put inside a list:
        resulting_list.append([values[0], values[1]])
    return resulting_list


if __name__ == "__main__":
    print(os.getcwd())  #print current directory
    for root, dirs, files in os.walk("./recipes"):
        for file in files:  #search the recipes folder for every recipe advancement
            filepath = os.path.join(root, file)
            if file.startswith("root.json"):    #(the root.json file is not needed)
                os.remove(filepath)
            elif file.endswith(".json"):
                print("\n-", file)

                #search for the corresponding file in the actual recipes folder in order to extract the ingredients
                filepath2 = os.path.join("./recipes2", file)
                with open(filepath2, "r") as f:
                    data = json.load(f)
                    ingredients = []
                    if data["type"] == "minecraft:crafting_shapeless":
                        print("type: crafting_shapeless")
                        ingredients = extract_ingredients_shapeless(data)
                        ingredients = remove_duplicates(ingredients)
                    else:
                        print("type:", data["type"][10:])
                        ingredients = extract_ingredients_other(data, file[:len(file)-5]) #excludes the .json extension and passes the name of the file
                        ingredients = merge_fungible_ingredients(ingredients)

                with open(filepath, 'w') as f:
                    advancement = {
                        "parent": "minecraft:recipes/root",
                        "criteria": {
                            "has_ingredients": {
                                "trigger": "minecraft:inventory_changed",
                                "conditions": {
                                    "items": [
                                        #crafting ingredients will go here
                                    ]
                                }
                            }
                        },
                        "requirements": [
                            [
                                "has_ingredients"
                            ]
                        ],
                        "rewards": {
                            "recipes": [
                                "minecraft:{}".format(file[:len(file)-5])
                            ]
                        }
                    }
                    
                    items = advancement["criteria"]["has_ingredients"]["conditions"]["items"]
                    
                    #the ingredients previously extracted from the recipe file are added to the advancement:
                    if data["type"] == "minecraft:crafting_shapeless":
                        for item in ingredients:
                            items.append(item)
                    else:
                        for item in ingredients:
                            if item[0] == "item":
                                ingredient = { "items": item[1] }
                            elif item[0] == "tag":
                                ingredient = { "tag": item[1][0] }  #(the tag does not need to be inside a list)
                            items.append(ingredient)

                    json_string = json.dumps(advancement, indent=2)
                    f.write(json_string)
