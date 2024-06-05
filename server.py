# Import Controllers Here
# from flask_app.controllers import class_controller
from flask_app.controllers import pokemon_controller


#! Be sure to set the secret Key in __init__.py

from flask_app import app

#! Debugger is for Development & Testing Only, NOT Production
#Todo: Turn off Debugger before App is in Production
if __name__=="__main__":
    app.run(debug=True)