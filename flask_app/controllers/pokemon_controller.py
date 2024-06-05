from flask_app import app
from flask import Flask, render_template, request, redirect, session, flash
#? JSON Package for Python
# Allows json to be interpreted into Python
import json

# ? Requests package for Python
# Used to make API calls within Python
# in the terminal `pip import requests`
import requests

#* Class Model Imports
# from flask_app.models.class_model import Class
from flask_app.models.pokemon_model import Pokemon

#* Index
#* Show All Route
@app.route("/")
def index():

    all_pkmn = Pokemon.get_all_pkmn()

    return render_template("index.html", all_pkmn = all_pkmn)

#* Create

# Add new Pokemon to the DB
@app.route("/pkmn/add_pkmn/", methods = ['GET', 'POST'])
def add_pkmn():

    # Pass name from form submission
    sub_data = {
        "name":request.form["pkmn_name"]
    }

    # Test pkmn_name sub from form
    # print("--------model test sub_data value (user input) ----------")
    # print(sub_data["name"])
    # print("--------------------- end of test -----------------------")

    # Get pokemon from PokeAPI
    new_pkmn = Pokemon.pkapi_get(sub_data["name"])

    # Test that response made it to the route
    # print("-------------- controller test new_pkmn value -------------")
    # print(new_pkmn["name"])
    # print(new_pkmn["id"])
    # print(new_pkmn["sprites"]["front_default"])
    # print(new_pkmn["sprites"]["front_shiny"])
    # print(f"{new_pkmn['stats'][0]['stat']['name']}: {new_pkmn['stats'][0]['base_stat']}")
    # print(f"{new_pkmn['stats'][1]['stat']['name']}: {new_pkmn['stats'][0]['base_stat']}")
    # print(f"{new_pkmn['stats'][2]['stat']['name']}: {new_pkmn['stats'][0]['base_stat']}")
    # print(f"{new_pkmn['stats'][3]['stat']['name']}: {new_pkmn['stats'][0]['base_stat']}")
    # print(f"{new_pkmn['stats'][4]['stat']['name']}: {new_pkmn['stats'][0]['base_stat']}")
    # print(f"{new_pkmn['stats'][5]['stat']['name']}: {new_pkmn['stats'][0]['base_stat']}")
    # print(f"Type One: {new_pkmn['types'][0]['type']['name']}")
    # print("------------------------ end of test ----------------------")

    # Type Two Conditional
    type_two_var = None

    if len(new_pkmn["types"]) > 1:
        type_two_var = new_pkmn["types"][1]["type"]["name"]

    # Parse into Python Dict
    pkmn_data = {
        "poke_name":new_pkmn["name"],
        "poke_id": new_pkmn["id"],
        "type_one": new_pkmn["types"][0]["type"]["name"],
        "type_two": type_two_var,
        "sprite_default": new_pkmn["sprites"]["front_default"],
        "sprite_shiny": new_pkmn["sprites"]["front_shiny"],
        "hp_stat": new_pkmn["stats"][0]["base_stat"],
        "attack_stat": new_pkmn["stats"][1]["base_stat"],
        "defense_stat": new_pkmn["stats"][2]["base_stat"],
        "spec_attack_stat": new_pkmn["stats"][3]["base_stat"],
        "spec_defense_stat": new_pkmn["stats"][4]["base_stat"],
        "speed_stat": new_pkmn["stats"][5]["base_stat"]
    }
    
    # Test that information has been loaded into Dict.
    # print("------------- controller test pkmn_data values ------------")
    # for key in pkmn_data:
    #     print(f"{key}: {pkmn_data[key]}")
    # print("----------------------- end of test -----------------------")

    # Add the pkmn_data to the DB
    Pokemon.add_pkmn(pkmn_data)

    # Get New Pokemon by Name
    new_poke_name = pkmn_data["poke_name"]

    # Show Route to display newly added Pokemon
    return redirect(f"/pkmn/show_one/{new_poke_name}")

#* Read

# Get one Pokemon by Name
@app.route("/pkmn/show_one/<poke_name>")
def show_one_pkmn(poke_name):

    # Test Name
    # print("======================================")
    # test_name = poke_name
    # print(test_name)
    # print("======================================")

    one_pkmn = Pokemon.get_pkmn_by_name({"poke_name": poke_name})

    # Test: Validate Pokemon Fetch
    # print("-------- Test Controller one_pkmn values --------")
    # print(f"Object type is {type(one_pkmn)}")
    # print(f"The name of one_pkmn is {one_pkmn.poke_name}")
    # print(f"The speed of {one_pkmn.poke_name} is {one_pkmn.speed_stat}.")
    # print("----------------- End of Test -------------------")

    base_stat_total = one_pkmn.hp_stat + one_pkmn.attack_stat + one_pkmn.defense_stat + one_pkmn.spec_attack_stat + one_pkmn.spec_defense_stat + one_pkmn.speed_stat

    return render_template("show_one_pkmn.html", one_pkmn = one_pkmn, base_stat_total=base_stat_total)

#* Update

#* Delete