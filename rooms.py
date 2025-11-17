from enum import Enum
import random

class Game_World():
    def __init__(self, day_counter, seed=None):
        self.seed = seed
        self.areas = {}
        self.day_counter = day_counter
        self.build_world()
    
    def build_world(self):
        self.build_town()
        random.seed(self.seed)
        self.build_cave()
        self.build_castle()

    def build_town(self):
        town_rooms = []
        town_rooms.append(Room(Room_Types.TAVERN, day_counter=self.day_counter))
        town_rooms.append(Room(Room_Types.SHOP, day_counter=self.day_counter))
        town_rooms.append(Room(Room_Types.INN, day_counter=self.day_counter))

        self.areas["Town"] = town_rooms
    
    def build_cave(self, ):
        cave_rooms = []

        for _ in range(5):
            rnd = random.random()
            if rnd < 1:
                room = Room(Room_Types.ENEMY_ROOM, day_counter=self.day_counter)
            else:
                room = Room(Room_Types.TRESSURE_ROOM, day_counter=self.day_counter)
            cave_rooms.append(room)
        
        self.areas["Cave"] = cave_rooms
    
    def build_castle(self,):
        castle_rooms = []

        for _ in range(5):
            rnd = random.random()
            if rnd < 0.6:
                room = Room(Room_Types.ENEMY_ROOM, day_counter=self.day_counter)
            else:
                room = Room(Room_Types.TRESSURE_ROOM, day_counter=self.day_counter)
            castle_rooms.append(room)
        boss_room = Room(Room_Types.BOSS_ROOM)
        castle_rooms.append(boss_room)
        
        self.areas["Castle"] = castle_rooms

    def __str__(self):
        output = ""

        for area_name, rooms in self.areas.items():
            room_strs = [str(Room) for Room in rooms]  # Use each Room's __str__
            output += f"{area_name}: {', '.join(room_strs)}\n"
        return output.strip()  # Remove trailing newline




class Room_Types(Enum):
    EMPTY = "empty"
    ENEMY_ROOM = "enemy room"
    TRESSURE_ROOM = "tressure room"
    TAVERN = "tavern"
    SHOP = "shop"
    INN = "inn"
    BOSS_ROOM = "boss room"


class Room(): 
    def __init__(self, room_type, day_counter=1):
        self.contents = {
            "enemies": [], 
            "items": []
        }
        self.room_type = room_type
        self.day_counter = day_counter

        match room_type:
            case Room_Types.TRESSURE_ROOM:
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

game  = Game_World(100)
room1 = Room(Room_Types.ENEMY_ROOM)
print(game)
