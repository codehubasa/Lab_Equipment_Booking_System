import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lab_project.settings')
django.setup()

from booking.models import Equipment

EQUIPMENT_DATA_INITIAL = [
    ("physics", [("Telescope", 2), ("Oscilloscope", 6), ("Multimeter", 30), ("Prism", 40), ("Lens Set", 30), ("Magnet Kit", 25), ("Tuning Forks", 20), ("Spring Balance", 30), ("Vernier Caliper", 40), ("Micrometer", 40), ("Diffraction Grating", 30), ("Galvanometer", 15), ("Rheostat", 20), ("Electromagnet", 10), ("Pendulum", 15), ("Laser Pointer", 15), ("Stopwatch", 40), ("Thermocouple", 15), ("Cathode Ray Tube", 2), ("Laser Diode", 10)]),
    ("chemistry", [("Chemical Set", 5), ("Beaker 500ml", 100), ("Bunsen Burner", 40), ("Test Tube Rack", 60), ("Erlenmeyer Flask", 80), ("Pipette", 150), ("Burette", 50), ("Thermometer", 40), ("Safety Goggles", 60), ("Litmus Paper", 200), ("Volumetric Flask", 40), ("Glass Stirring Rod", 120), ("Crucible", 40), ("Mortar and Pestle", 30), ("Watch Glass", 80), ("Dropper", 100), ("pH Meter", 5), ("Centrifuge Tube", 200), ("Funnel", 60), ("Ring Stand", 40)]),
    ("biology", [("Microscope", 20), ("Slide Set", 100), ("Petri Dish", 200), ("Dissection Kit", 40), ("Human Skeleton Model", 2), ("DNA Model", 5), ("Magnifying Glass", 50), ("Specimen Jar", 80), ("Centrifuge", 2), ("Incubator", 2), ("Scalpel", 60), ("Tweezers", 100), ("Microscope Slides", 300), ("Staining Kit", 20), ("Beaker 250ml", 80), ("Thermometer", 40), ("Anatomy Chart", 10), ("Safety Gloves", 500), ("Autoclave", 1), ("Pipettor", 40)]),
    ("computer", [("Computer", 40), ("Raspberry Pi", 25), ("Arduino Board", 30), ("Breadboard", 50), ("Soldering Iron", 15), ("Network Switch", 5), ("Cat6 Cable", 100), ("Monitor", 40), ("Keyboard/Mouse", 45), ("Server Rack", 2), ("SSD Drive", 20), ("GPU", 5), ("RAM Stick", 30), ("Motherboard", 10), ("Power Supply Unit", 15), ("Multimeter", 20), ("Wire Strippers", 20), ("Heat Shrink Tubing", 100), ("Breadboard Jumpers", 500), ("Cooling Fan", 20)]),
    ("geography", [("Globe", 5), ("World Map", 15), ("Topographic Map", 30), ("Compass", 40), ("Weather Station", 2), ("Rock Collection", 10), ("Soil Test Kit", 15), ("Barometer", 5), ("Anemometer", 5), ("Telescope (Geo)", 2), ("Seismograph Model", 2), ("Rain Gauge", 15), ("Hygrometer", 10), ("Geological Hammer", 15), ("Clinometer", 20), ("Altimeter", 5), ("Sundial", 5), ("Sextant", 5), ("GPS Receiver", 10), ("Fossil Collection", 10)])
]

def populate():
    print("Populating database with initial equipment...")
    count = 0
    for category, items in EQUIPMENT_DATA_INITIAL:
        for name, quantity in items:
            # get_or_create to avoid duplicates if run multiple times
            equip, created = Equipment.objects.get_or_create(
                name=name,
                category=category,
                defaults={'available': quantity}
            )
            if created:
                count += 1
    
    print(f"Successfully added {count} new equipment items to the database.")

if __name__ == '__main__':
    populate()
