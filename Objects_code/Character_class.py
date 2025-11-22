import random
from enum import Enum

class Character():
    def __init__(self, name: str, hp: int, damage: int, defence: int, equipment: dict[str, any], level: int | None = None):
        self.name = name
        self.hp = hp
        self.damage = damage
        self.defence = defence
        self.equipment = equipment
        self.level = level

    def take_damage(self, damage: int) -> None:
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
            outcome_table["critical_hit"] = True
        
        if temp_damage > other.defence:
            damage_dealt = temp_damage - other.defence
            outcome_table["damage"] = damage_dealt
            other.take_damage(damage_dealt)
        
        else:
            outcome_table["blocked"] = True
        
        if not other.is_alive():
            outcome_table["died"] = True
        
        return outcome_table
    
    def level_up(self) -> None:
        pass

    def render_attack_text(outcome: dict) -> str:

        text_block = ""

        text_block += "ATTACK RESULT:"
        text_block += outcome["attacker"] + " attacks " + outcome["target"] + "\n"

        if outcome["critical_hit"] is True:
            text_block += "critical hit\n"

        if outcome["blocked"] is True:
            text_block += "The attack was blocked.\n"
        else:
            text_block += "Damage dealt: " + outcome["damage"] + "\n"

        if outcome["warrior_rage"] == True:
            text_block += "Warrior enters RAGE and deals extra damage!\n"

        if outcome["died"] == True:
            text_block += outcome["target"] + " has fallen.\n"

        return text_block

    
    def __str__(self):
        return f"name:{self.name}, hp:{self.hp}, damage:{self.damage}, level:{self.level}, defence: {self.defence}, equipment: {self.equipment}"
    

class Warrior(Character):
    def __init__(self, name: str, hp: int, damage: int, defence: int, equipment: dict[str, any], level: int | None = None):
        super().__init__(name, hp, damage, defence, equipment, level)
        self.defence *= 1.2
        self.hp *= 1.2
        self.damage *= 0.9
        self.max_hp = self.hp
    
    def take_damage(self, damage: int):
        reduced_damage = damage * 0.9
        return super().take_damage(reduced_damage)
    
    def attack(self, other: 'Character'):
        outcome = super().attack(other)
        if outcome["blocked"] == True:
            return outcome

        if self.hp <= (self.max_hp * 0.40) and random.random() >= 0.30: #extra damage eg. rage which will be implemented later
            outcome["warrior_rage"] = True

            extra_damage = int(outcome["damage"] * 0.5)
            
            other.take_damage(extra_damage)
            outcome["damage"] += extra_damage

        return outcome

    

    def level_up(self): #this method should be called exp_up but I don't want to implement it before I know how hard to make the enemies
        if self.level == 10:
            return "Cannot increase to more than 10" # should be reworked when xp have been implemented so the xp just go up and level doesn't change
        temp_level = self.level
                
        #add xp gain later for now I will just increase level by 1 when this method is called
        self.level += 1

        if self.level > temp_level:
            if self.level <= 5:
                self.defence *= 1.3
                self.hp *= 1.3
                self.damage *= 1.2
            
            elif self.level <= 8:
                self.defence *= 1.4
                self.hp *= 1.5
                self.damage *= 1.3
            
            elif self.level == 9:
                self.defence *= 1.6
                self.hp *= 1.7
                self.damage *= 1.4
            
            elif self.level == 10:
                self.defence *= 1.8
                self.hp *= 1.9
                self.damage *= 1.6




class Enemy_Rarity(Enum):
    COMMON = "common"
    UNCOMMON = "uncommon"
    RARE = "rare"
    ELITE = "elite"
    MINI_BOSS = "mini_boss"
    BOSS = "boss"

class Enemy_type(Enum): #only 1 for don't know how many I'll add
    UNDEAD = "undead"

class Behavior_Tag(Enum):
    NORMAL = "normal" # default state
    AGGRESSIVE = "aggressive"
    COWARDLY = "cowardly"
    RANGED = "ranged"
    SLOW = "slow"

class Enemy(Character):
    def __init__(self, name: str, hp: int, damage: int, 
                 defence: int, rarity: Enemy_Rarity, 
                 type: Enemy_type, loot_table: list[dict[str, any]],
                 behavior_tag: Behavior_Tag | None = None):
        super().__init__(name, hp, damage, defence)
        
        self.type = type
        self.rarity = rarity

        self.level_scaling_factor = None # TBA

        self.loot_table = loot_table

        self.behavior_tag = behavior_tag if behavior_tag else self.behavior_tag = Behavior_Tag.NORMAL
    
    def attack(self, other: 'Character') -> dict: # Will be modified later on but for now will act as normal
        return super().attack(other)
    
    def take_damage(self, damage: int) -> None: # Will be modified later on but for now will act as normal
        return super().take_damage(damage)
    
    def scale_stats(self, day_counter: int, depth) -> None:
        day_counter_scaling = 1 + (day_counter / 100)
        depth_scaling = 1 + (depth / 50)

        self.hp = self.hp * day_counter_scaling
        self.defence = self.defence * day_counter_scaling

        self.damage = self.damage * depth_scaling
        



    

    

