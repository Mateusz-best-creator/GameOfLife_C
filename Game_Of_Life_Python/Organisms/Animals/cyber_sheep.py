from Organisms.animal import Animal
from organism import OrganismInitialData

class CyberSheep(Animal):
    def __init__(self, name, row, column):
        strength = OrganismInitialData[name]["strength"]
        initiative = OrganismInitialData[name]["initiative"]
        character = OrganismInitialData[name]["character"]
        super().__init__(strength, initiative, name, character, row, column)

    def action():
        pass

    def collision():
        pass


