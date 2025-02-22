import json
import pint

# Initialize the unit registry
ureg = pint.UnitRegistry()

def load_units(filepath):
    with open(filepath, 'r') as file:
        units = json.load(file)
    return units