from utils.unit_utils import load_units, ureg
from geometry.shape import Shape

# Load units from JSON file
units = load_units("./data/aegis_units.json")

def main():
    # Create an instance of the Shape class
    shape = Shape(size=10.0, unit=units['length'])
    
    # Print the size and unit
    print(f"Shape size: {shape.size}")
    print(f"Display unit: {shape.display_unit}")
    
    # Set a new datum
    shape.set_datum(new_elev=100.0, unit=units['length'])
    
    # Print the datum
    print(f"Datum elevation: {shape.datum.elevation}")
    
    # Convert units and print the updated size and datum
    shape.change_unit('ft')
    print(f"Shape size in feet: {shape.size}")
    print(f"Datum elevation in feet: {shape.datum.elevation}")

if __name__ == "__main__":
    main()