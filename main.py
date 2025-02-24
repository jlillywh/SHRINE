from utils.unit_utils import load_units, ureg
from geometry.shape import Shape
from geometry.cylinder import Cylinder

# Load units from JSON file
units = load_units("./data/aegis_units.json")

def main():
    # Create an instance of the Shape class
    shape = Shape(size=10.0, unit=units['length'])
    # Create an instance of the Cylinder class
    cylinder = Cylinder(radius=2.0, height=5.0, unit=units['length'])

    # Print the size and unit
    print(f"Shape size: {shape.size}")
    print(f"Shape unit: {shape.display_unit}")
    print(f"Cylinder radius: {cylinder.radius}")
    print(f"Cylinder height: {cylinder.height}")
    print(f"Cylinder base unit: {cylinder.size.units}")
    print(f"Cylinder area: {cylinder.area()}")
    print(f"Cylinder volume: {cylinder.volume()}")

    # Set a new datum
    shape.set_datum(new_elev=100.0, unit=units['length'])
    cylinder.set_datum(new_elev=200.0, unit=units['length'])

    # Print the datum
    print(f"Datum elevation: {shape.datum.elevation}")
    print(f"Cylinder datum elevation: {cylinder.datum.elevation}")

    # Convert units and print the updated size and datum
    shape.change_unit('ft')
    cylinder.change_unit('ft')
    print(f"Shape size in feet: {shape.size}")
    print(f"Datum elevation in feet: {shape.datum.elevation}")
    print(f"Cylinder volume in cubic feet: {cylinder.volume()}")
    print(f"Cylinder datum elevation in feet: {cylinder.datum.elevation}")

if __name__ == "__main__":
    main()