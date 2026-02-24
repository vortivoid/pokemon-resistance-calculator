import requests

class Pokemon:

    name = ""

    WEAKNESS = -1
    SUPER_WEAKNESS = -2
    NEUTRAL = 0
    RESISTANCE = 1
    SUPER_RESISTANCE = 2

    weaknesses = []
    super_weaknesses = []
    neutrals = []
    resistances = []
    super_resistances = []
    immunities = []

    def add_type(self, type_data):

        def calc_score(type_name, initial_score):
            score = initial_score
            if type_name in self.weaknesses:
                score = initial_score + self.WEAKNESS
            elif type_name in self.resistances:
                score = initial_score + self.RESISTANCE
            return score

        
        def sort_type(type_name, score):
            clear_duplicates(type_name)
            match score:
                case -2:
                    self.super_weaknesses.append(type_name)
                    return
                case -1:
                    self.weaknesses.append(type_name)
                    return
                case 0:
                    self.neutrals.append(type_name)
                    return
                case 1:
                    self.resistances.append(type_name)
                    return
                case 2:
                    self.super_resistances.append(type_name)
                    return
                case _:
                    print("Undefined Interaction! Score: "+str(score))
                    return
        
        def clear_duplicates(type_name):
            if type_name in self.weaknesses:
                self.weaknesses.remove(type_name)
            if type_name in self.super_weaknesses:
                self.super_weaknesses.remove(type_name)
            if type_name in self.neutrals:
                self.neutrals.remove(type_name)
            if type_name in self.resistances:
                self.resistances.remove(type_name)
            if type_name in self.super_resistances:
                self.super_resistances.remove(type_name)

        damage_relations = type_data["damage_relations"]

        for type in damage_relations["no_damage_from"]:
            if not type in self.immunities:
                self.immunities.append(type["name"])
        
        for type in damage_relations["double_damage_from"]:
            if not type in self.immunities:   
                sort_type(type["name"], calc_score(type["name"], self.WEAKNESS))
        
        for type in damage_relations["half_damage_from"]:
            if not type in self.immunities:
                sort_type(type["name"], calc_score(type["name"], self.RESISTANCE))

    
    def print_relations(self):
        print("--- Weak To ---")
        for type in self.weaknesses:
            print(type)
        print
        print("--- Super Weak To ---")
        for type in self.super_weaknesses:
            print(type)
        print()
        print("--- Resists ---")
        for type in self.resistances:
            print(type)
        print()
        print("--- Super Resists ---")
        for type in self.super_resistances:
            print(type)
        print()
        print("--- Immune To (0x Damage) ---")
        for type in self.immunities:
            print(type)
        print()
        print("Anything not listed here means the pokemon takes neutral damage from it")

def get_pokemon_data(pokemon_name):
    api_url = ("https://pokeapi.co/api/v2/pokemon/" + pokemon_name)
    response = requests.get(api_url)
    if str(response) == "<Response [404]>":
        print("Could not find any data on '" + pokemon_name +"'. Are you sure you spelt it correctly?")
        exit()
    return response.json()

def get_type_data(data, slot: int):
    type_name = data["types"][slot]["type"]["name"]
    api_url = ("https://pokeapi.co/api/v2/type/"+type_name)
    response = requests.get(api_url)
    if str(response) == "<Response [404]>":
        print("Could not find any data on '" + type_name +"'. Are you sure you spelt it correctly?")
        exit()
    return response.json()

def convert_common_mistypes(name):
    if name == "mimikyu":
        return "mimikyu-disguised" # THIS IS SO DUMB WHAT THE FUCK WHY IS POKEAPI LIKE THIS?!?!?! (sob)
    else:
        return name

# Program Start
while True:
    pokemon = Pokemon()
    pokemon.name = convert_common_mistypes(input("Enter the pokemon's name: "))

    data = get_pokemon_data(pokemon.name)

    is_dualtype = (len(data["types"]) == 2)
    type1 = get_type_data(data, 0)
    pokemon.add_type(type1)
    if is_dualtype:
        type2 = get_type_data(data, 1)
        pokemon.add_type(type2)
    pokemon.print_relations()
    if input("Would you like to continue? (Y/n): ").lower == "n":
        exit()
