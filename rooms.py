from enum import Enum
import random

class Game_World():
    def __init__(self, day_counter, seed=None) -> None:
        self.seed = seed
        self.areas = {}
        self.day_counter = day_counter
        self.build_world()
    
    def build_world(self) -> None:
        self.build_town()
        random.seed(self.seed)
        self.build_cave()
        self.build_castle()

    def build_town(self) -> None:
        town_rooms = []
        town_rooms.append(Room(Room_Types.TAVERN, day_counter=self.day_counter))
        town_rooms.append(Room(Room_Types.SHOP, day_counter=self.day_counter))
        town_rooms.append(Room(Room_Types.INN, day_counter=self.day_counter))

        self.areas["Town"] = town_rooms
    
    def build_cave(self) -> dict:
        self.starting_position = (0,0)
        self.starting_room = Room(Room_Types.EMPTY)

        cave_rooms = {
            self.starting_position: self.starting_room,
        }

        base_size = 16
        difficulty_factor = 1 + (self.day_counter * 0.05)
        room_count = base_size + int(self.day_counter * 0.2)

        enemy_room_chance = min(0.5 + self.day_counter * 0.01, 0.9)
        treasure_room_chance = max(0.2 - self.day_counter * 0.005, 0.05)

        current_position = self.starting_position

        for _ in range(room_count):
            next_position = pick_random_adjacent(current_position)

            if next_position not in cave_rooms:
                room_type = choose_room_type(enemy_room_chance, treasure_room_chance)
                cave_rooms[next_position] = Room(room_type, day_counter=self.day_counter)
            
                current_position = next_position
        
        self.areas["cave"] = cave_rooms

        return cave_rooms

        # old logic for liniar system
        """cave_rooms = []

        for _ in range(5):
            rnd = random.random()
            if rnd < 1:
                room = Room(Room_Types.ENEMY_ROOM, day_counter=self.day_counter)
            else:
                room = Room(Room_Types.TRESSURE_ROOM, day_counter=self.day_counter)
            cave_rooms.append(room)
        
        self.areas["Cave"] = cave_rooms"""
    
    def build_castle(self):
        castle_rooms = []

        for _ in range(5):
            rnd = random.random()
            if rnd < 0.6:
                room = Room(Room_Types.ENEMY_ROOM, day_counter=self.day_counter)
            else:
                room = Room(Room_Types.TREASURE_ROOM, day_counter=self.day_counter)
            castle_rooms.append(room)
        boss_room = Room(Room_Types.BOSS_ROOM)
        castle_rooms.append(boss_room)
        
        self.areas["Castle"] = castle_rooms

    def __str__(self) -> str:

        output = ""

        for area_name, rooms in self.areas.items():
            room_strs = [str(room) for room in rooms]  # Use each Room's __str__
            output += f"{area_name}: {', '.join(room_strs)}\n"
        return output.strip()  # Remove trailing newline
    
    def visualize_cave(self, cave_rooms) -> list:
        x_values = [pos[0] for pos in cave_rooms.keys()]
        y_values = [pos[1] for pos in cave_rooms.keys()]

        min_x, max_x = min(x_values), max(x_values)
        min_y, max_y = min(y_values), max(y_values)

        map_rows = []

        for y in range(max_y, min_y - 1, -1):
            row_string = ""

            for x in range(min_x, max_x + 1):
                position = (x, y)

                if position in cave_rooms:
                    room = cave_rooms[position]

                    if position == self.starting_position:
                        symbol = "S"
                    
                    elif room.room_type == Room_Types.TREASURE_ROOM:
                        symbol = "T"

                    elif room.room_type == Room_Types.ENEMY_ROOM:
                        symbol = "E"

                    elif room.room_type == Room_Types.EMPTY:
                        symbol = "P"
                    
                    else:
                        symbol = "."

                else:
                    symbol = " "
                
                row_string += symbol
        
            map_rows.append(row_string)

        return map_rows
                    

        



def pick_random_adjacent(position) -> tuple:
    x, y = position
    direction = random.choice(["north", "south", "east", "west"])

    match direction:
        case "north":
            return (x, y + 1)
        case "south":
            return (x, y - 1)
        case "east":
            return (x + 1, y)
        case "west":
            return (x - 1, y)


def choose_room_type(enemy_chance, treasure_chance) -> Enum:
    rnd = random.random()

    if rnd < enemy_chance:
        return Room_Types.ENEMY_ROOM
    elif rnd < (enemy_chance + treasure_chance):
        return Room_Types.TREASURE_ROOM
    else:
        return Room_Types.EMPTY



class Room_Types(Enum):
    EMPTY = "empty"
    ENEMY_ROOM = "enemy room"
    TREASURE_ROOM  = "treassure room"
    TAVERN = "tavern"
    SHOP = "shop"
    INN = "inn"
    BOSS_ROOM = "boss room"


class Room(): 
    def __init__(self, room_type, pos_x=0, pos_y=0, day_counter=1):
        self.room_type = room_type
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.connections = {}
        self.contents = {
            "enemies": [], 
            "items": []
        }
        self.day_counter = day_counter

        match room_type:
            case Room_Types.TREASURE_ROOM:
                for _ in range(random.randint(0, 2)):
                    self.contents["items"].append(random.choice(Items.list()))
                
            case Room_Types.ENEMY_ROOM:
                for _ in range(random.randint(1, 4)):
                    base_enemy = random.choice(Enemy.list())
        
                    # Calculate modifier (e.g., 10% increase per day after day 1)
                    modifier = 1 + (self.day_counter - 1) * 0.1
                    
                    modified_hp = int(base_enemy.hp * modifier)
                    modified_damage = int(base_enemy.damage * modifier)
                    new_enemy = Enemy(base_enemy.name, modified_hp, modified_damage)

                    self.contents["enemies"].append(new_enemy)

                    if len(self.contents["enemies"]) >= 2:
                        break

                    has_ogre = False
                    for enemy in self.contents["enemies"]:
                        if enemy.name == "ogre":
                            has_ogre = True
                            break
                    if has_ogre:
                        break
                
                self.contents["items"].append(random.choice(Items.list()))
            
            case Room_Types.BOSS_ROOM:
                self.contents["enemies"].append(Enemy("Dragon", 50, 20))
                self.contents["items"].append(Items("Magic Potion", "potion", None, 30))
            
            case _: #Types.EMPTY
                pass
    

    def __str__(self):
        enemy_list = ", ".join([f"{enemy.name} ({enemy.hp} HP)" for enemy in self.contents["enemies"]]) or "None"
        item_list = ", ".join([f"{item.name}" for item in self.contents["items"]]) or "None"
        return f"{self.room_type.value}: Enemies - {enemy_list}, Items - {item_list}"

class Enemy():
    def __init__(self, name: str, hp: int, damage: int):
        self.name = name
        self.hp = hp
        self.damage = damage

    def list() -> list:
        list_of_enemies = []
    
        list_of_enemies.append(Enemy("bat", 10, 2))
        list_of_enemies.append(Enemy("skeleton", 5, 10))
        list_of_enemies.append(Enemy("ogre", 100, 30))

        return list_of_enemies


class Items():
    def __init__(self, name: str, type: str, effect:any=None, damage: int=None):
        self.name = name
        self.type = type
        self.damage = damage
        self.effect = effect

    def list():
        list_of_items = []

        list_of_items.append(Items("sword", "weapon", None, 10))
        list_of_items.append(Items("bag", "key item", "holds more space user is now lighter"))
        list_of_items.append(Items("hp potion", "usable", "give hp", 100))

        return list_of_items

game  = Game_World(40)
print(game, "\n", "\n")

cave_rooms = game.build_cave()
map_view = game.visualize_cave(cave_rooms)
for line in map_view:
    print(line)