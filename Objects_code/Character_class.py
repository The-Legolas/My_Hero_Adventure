import random

class Character():
    def __init__(self, name: str, hp: int, damage: int, defence: int, equipment: dict[str, any], level: int | None = None):
        self.name = name
        self.hp = hp
        self.damage = damage
        self.defence = defence
        self.equipment = equipment
        self.level = level

    def take_damage(self, damage) -> None:
        self.hp -= damage
    
    def is_alive(self) -> bool:
        return True if self.hp > 0 else False
    
    def debug_attack(self, other: 'Character') -> None:
        text_block = ""

        text_block += f"{self.name} is attacking {other.name}"

        temp_damage = self.damage
        if random.random() >= 0.95:
            temp_damage *= 2

        if temp_damage > other.defence:
            damage_dealt = temp_damage - other.defence
            other.take_damage(damage_dealt)
            text_block += f" and deals {damage_dealt} damage!\n"

        else:
            text_block += " but it was blocked!\n"

        return text_block
    
    def attack(self, other: 'Character') -> None:
        outcome_table = {
            "attacker": self.name,
            "target": other.name,
            "damage": 0,
            "critical_hit": False,
            "blocked": False,
            "died": False
        }

        temp_damage = self.damage

        if random.random() >= 0.95:
            temp_damage *= 2
            outcome_table["critical hit"] = True
        
        if temp_damage > other.defence:
            damage_dealt = temp_damage - other.defence
            outcome_table["damage"] = damage_dealt
            other.take_damage(damage_dealt)
        
        else:
            outcome_table["blocked"] = True
        
        if not other.is_alive():
            outcome_table["died"] = True
        
        return outcome_table
    
    def __str__(self):
        return f"name:{self.name}, hp:{self.hp}, damage:{self.damage}, level:{self.level}"
    

class Warrior(Character):
    def __init__(self, name, hp, damage, defence, equipment, level = None):
        super().__init__(name, hp, damage, defence, equipment, level)




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

