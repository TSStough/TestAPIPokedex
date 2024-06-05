#Imports
from flask_app.config.mysqlconection import connectToMySQL
from flask import flash, request
# Used to make API calls within Python
# in the terminal `pip import requests`
import requests

#* User Class Model Import
#! Don't import the Class. Only its Model file
# from flask_app.models import class_model

class Pokemon:
    #* Database Shorthand
    DB = "pokedex_test_api"

    #* Constructor
    def __init__(self, data) -> None:
        self.id = data['id']
        self.poke_name = data['poke_name']
        self.poke_id = data['poke_id']
        self.type_one = data['type_one']
        self.type_two = data['type_two']
        self.hp_stat = data['hp_stat']
        self.attack_stat = data['attack_stat']
        self.defense_stat = data['defense_stat']
        self.spec_attack_stat = data['spec_attack_stat']
        self.spec_defense_stat = data['spec_defense_stat']
        self.speed_stat = data['speed_stat']
        self.sprite_default = data['sprite_default']
        self.sprite_shiny = data['sprite_shiny']

    #* Create Methods
    @classmethod
    def add_pkmn(cls,data):
        query = """
            INSERT INTO pokemon
            (poke_name, poke_id, type_one, type_two, hp_stat, attack_stat, defense_stat,spec_attack_stat, spec_defense_stat, speed_stat, sprite_default, sprite_shiny)
            VALUES
            (%(poke_name)s, %(poke_id)s, %(type_one)s, %(type_two)s, %(hp_stat)s, %(attack_stat)s, %(defense_stat)s, %(spec_attack_stat)s, %(spec_defense_stat)s, %(speed_stat)s, %(sprite_default)s, %(sprite_shiny)s);
        """

        result = connectToMySQL(cls.DB).query_db(query,data)

        return result

    #* Read Methods

    # Grab Pkmn object from PokeAPI with Name input
    @classmethod
    def pkapi_get(cls, data):

        # Turn data into a str variable
        pkmn_name = data

        # Pass str variable into Get URL
        response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pkmn_name}/")
        pkmn = response.json()

        # Response Test
        # print("------ model test pkapi_get response value -----------")
        # print(pkmn["forms"][0]["name"])
        # print("------------------ end of response -------------------")

        # Return the Response to the Route
        return pkmn
    
    # Get one Pkmn from DB by poke_name
    @classmethod
    def get_pkmn_by_name(cls, data):
        query = """
            SELECT * FROM pokemon
            WHERE poke_name = %(poke_name)s;
        """

        result = connectToMySQL(cls.DB).query_db(query, data)

        return cls(result[0])
    
    @classmethod
    def get_all_pkmn(cls):

        # Gather all of the logged pokemon in the DB
        query = """
            SELECT * FROM pokemon;
        """

        results = connectToMySQL(cls.DB).query_db(query)

        all_pkmn = []

        # Parse the Data into a dictionary
        for row in results:
            pkmn_data = {
                "id": row["id"],
                "poke_id": row["poke_id"],
                "poke_name": row["poke_name"],
                "sprite_default": row["sprite_default"],
                "sprite_shiny": row["sprite_shiny"],
                "hp_stat": row["hp_stat"],
                "attack_stat": row["attack_stat"],
                "defense_stat": row["defense_stat"],
                "spec_attack_stat": row["spec_attack_stat"],
                "spec_defense_stat": row["spec_defense_stat"],
                "speed_stat": row["speed_stat"],
                "type_one": row["type_one"],
                "type_two": row["type_two"]
            }

            # Assign each row to a pokemon
            one_pkmn = cls(row)

            # Test
            # print("-------- Model Test one_pkmn values ---------")
            # print(one_pkmn.poke_name)
            # print("--------------- End of Test -----------------")

            # Add each pokemon to All Pokemon
            all_pkmn.append(one_pkmn)

            # # Test
            # print("-------- Model Test all_pkmn values ---------")
            # for p in all_pkmn:
            #     print(p.poke_name)
            # print("--------------- End of Test -----------------")

        return all_pkmn

    #* Update Methods

    #* Delete Methods