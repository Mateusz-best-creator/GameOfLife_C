from abc import ABC, abstractmethod
from Organisms.organism import Organism
import random
from enum import Enum

class MoveDirection(Enum):
    LEFT = 1
    RIGHT = 2
    TOP = 3
    BOTTOM = 4

class CollisionTypes(Enum):
    NONE = "None"
    MULTIPLICATION = "Multiplication"
    FIGHT = "Fight"

class Animal(Organism, ABC):

    MAX_ANIMAL_AMOUNT = 5
    MIN_STRENGTH_TURTLE_REFLECT = 4

    def __init__(self, strength, initiative, name, character, row, column, image_path):
        super().__init__(strength, initiative, name, character, row, column, image_path)

    @abstractmethod
    def action(self, grid_board):
        pass

    @abstractmethod
    def collision(self, grid_board, organisms, current_index):
        pass

    @abstractmethod
    def get_static_counter(self):
        pass

    @abstractmethod
    def increase_static_counter(self):
        pass

    @abstractmethod
    def decrease_static_counter(self):
        pass

    def default_action_animal(self, grid_board):

        self.age += 1

        self.previous_row = self.row
        self.previous_column = self.column

        direction = MoveDirection(random.randint(1, 4))

        # Check if the movement in the selected direction will keep the organism within the board bounds
        while True:
            if self.row == 0 and direction == MoveDirection.TOP:
                direction = MoveDirection(random.choice(
                    [MoveDirection.LEFT, MoveDirection.RIGHT, MoveDirection.BOTTOM]))
            elif self.row == 9 and direction == MoveDirection.BOTTOM:
                direction = MoveDirection(random.choice(
                    [MoveDirection.LEFT, MoveDirection.RIGHT, MoveDirection.TOP]))
            elif self.column == 0 and direction == MoveDirection.LEFT:
                direction = MoveDirection(random.choice(
                    [MoveDirection.TOP, MoveDirection.RIGHT, MoveDirection.BOTTOM]))
            elif self.column == 9 and direction == MoveDirection.RIGHT:
                direction = MoveDirection(random.choice(
                    [MoveDirection.TOP, MoveDirection.LEFT, MoveDirection.BOTTOM]))
            else:
                break

        grid_board[self.row][self.column] = 'e'
        name = self.name
        if name == "cyber_sheep":
            name = "cyber"
        self.print_to_journal(
            f"{name} from ({self.row}, {self.column}) to ")

        # Perform movement based on the selected direction
        if direction == MoveDirection.LEFT:
            self.organism_go_left()
        elif direction == MoveDirection.TOP:
            self.organism_go_top()
        elif direction == MoveDirection.RIGHT:
            self.organism_go_right()
        elif direction == MoveDirection.BOTTOM:
            self.organism_go_bottom()

        grid_board[self.row][self.column] = self.character
        self.print_to_journal(f"to ({self.row}, {self.column})\n")

    def default_collision_animal(self, grid_board, organisms, current_index):
        
        for organism_index, organism in enumerate(organisms):

            if organism.get_position_row() == self.row and organism.get_position_column() == self.column and organism_index != current_index:

                # Some special plant cases
                if organism.get_name() == "Guarana" or organism.get_name() == "Belladonna" or organism.get_name() == "Sosnowsky_hogweed":
                    # self.print_to_journal(f"{self.character} vs {organism.get_character()} at ({self.row}, {self.column})\n")
                    return CollisionTypes("None"), None

                # Multiplication case
                elif self.character == organism.get_character():
                    
                    self.row = self.previous_row
                    self.column = self.previous_column
                    grid_board[self.row][self.column] = self.character
                    if self.get_static_counter() > Animal.MAX_ANIMAL_AMOUNT:
                        self.print_to_journal(f"""{self.character} vs {organism.get_character()} -> cant be more than {Animal.MAX_ANIMAL_AMOUNT}\n""")
                        return CollisionTypes("None"), None

                    else:
                        return CollisionTypes("Multiplication"), self.type(self.name, self.row, self.column)

                # Turtle collision
                elif organism.get_name() == 'turtle' and self.strength <= Animal.MIN_STRENGTH_TURTLE_REFLECT:
                    
                    self.row = self.previous_row
                    self.column = self.previous_column
                    grid_board[self.row][self.column] = self.character
                    self.print_to_journal(f"""{self.character} vs {organism.get_character()} -> {self.character} back to ({self.row}, {self.column})\n""")
                    return CollisionTypes("None"), None

                # Fight case
                else:

                    if self.strength >= organism.get_strength():
                        
                        self.print_to_journal(f"""{self.character} vs {organism.get_character()} -> {self.character} wins at ({self.row}, {self.column})\n""")
                        grid_board[self.row][self.column] = self.character
                        return CollisionTypes("Fight"), organism_index

                    else:

                        self.print_to_journal(f"""{self.character} vs {organism.get_character()} -> {organism.get_character()} wins at ({self.row}, {self.column})\n""")
                        grid_board[self.row][self.column] = organism.get_character()
                        return CollisionTypes("Fight"), current_index


        grid_board[self.row][self.column] = self.character
        return CollisionTypes("None"), None
