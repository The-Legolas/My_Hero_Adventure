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

    def __str__(self):
        return f"name:{self.name}, hp:{self.hp}, damage:{self.damage}, level:{self.level}, defence: {self.defence}, equipment: {self.equipment}"

def render_attack_text(outcome: dict) -> str:

        text_block = ""

        text_block += "ATTACK RESULT:"
        text_block += outcome["attacker"] + " attacks " + outcome["target"] + "\n"

        if outcome["critical_hit"] is True:
            text_block += "critical hit\n"

        if outcome["blocked"] is True:
            text_block += "The attack was blocked.\n"
        else:
            text_block += f"Damage dealt: {outcome["damage"]}\n"

        if outcome["warrior_rage"] == True:
            text_block += "Warrior enters RAGE and deals extra damage!\n"

        if outcome["died"] == True:
            text_block += outcome["target"] + " has fallen.\n"

        return text_block



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

class Enemy_sub_type(Enum): #only 1 for don't know how many I'll add
    UNDEAD = "undead"
    HUMANOID = "humanoid"
    OOZE = "ooze"
    BEAST = "beast"
    DRAGON = "dragon"

class Enemy_type(Enum):
    ENEMY_GOBLIN = "goblin"
    ENEMY_SLIME = "slime"
    ENEMY_WOLF = "wolf"
    ENEMY_ORC = "orc"
    ENEMY_BOSS_DRAGON = "dragon boss"


class Enemy_behavior_tag(Enum):
    NORMAL = "normal" # default state
    AGGRESSIVE = "aggressive"
    COWARDLY = "cowardly"
    RANGED = "ranged"
    SLOW = "slow"
    HULKING = "hulking"

class Enemy(Character):
    def __init__(self, name: str, hp: int, damage: int, 
                 defence: int, rarity: Enemy_Rarity, 
                 type: Enemy_type, sub_type: Enemy_sub_type, xp_reward: int, gold_reward: int, loot_table: list[dict[str, any]],
                 behavior_tag: Enemy_behavior_tag | None = None):
        super().__init__(name, hp, damage, defence)
        
        self.type = type
        self.sub_type = sub_type
        self.rarity = rarity
        self.xp_reward = xp_reward
        self.gold_reward = gold_reward

        self.level_scaling_factor = None # TBA

        self.loot_table = loot_table

        self.behavior_tag = behavior_tag if behavior_tag else Enemy_behavior_tag.NORMAL

        self.is_scaled = False
    
    
    def scale_stats(self, day_counter: int, depth) -> None:
        if self.is_scaled == True:
            return
        day_counter_scaling = 1 + (day_counter / 100)
        depth_scaling = 1 + (depth / 50)

        self.hp = int(self.hp * day_counter_scaling)
        self.defence = int(self.defence * day_counter_scaling)

        self.damage = int(self.damage * depth_scaling)
        self.is_scaled = True
        


ENEMY_DEFINITIONS = {
    Enemy_type.ENEMY_GOBLIN: {
        "name": "Goblin",
        "hp": 20,
        "damage": 4,
        "defence": 1,
        "rarity": Enemy_Rarity.COMMON,
        "sub_type": Enemy_sub_type.HUMANOID,
        "xp_reward": 50,
        "gold_reward": 3,
        "loot_table": [],
        "behavior_tag": Enemy_behavior_tag.NORMAL
    },
    Enemy_type.ENEMY_SLIME: {
        "name": "Slime",
        "hp": 14,
        "damage": 2,
        "defence": 5,
        "rarity": Enemy_Rarity.COMMON,
        "sub_type": Enemy_sub_type.OOZE,
        "xp_reward": 40,
        "gold_reward": 2,
        "loot_table": [],
        "behavior_tag": Enemy_behavior_tag.COWARDLY
    },
    Enemy_type.ENEMY_WOLF:  {
        "name": "Wolf",
        "hp": 23,
        "damage": 5,
        "defence": 3,
        "rarity": Enemy_Rarity.UNCOMMON,
        "sub_type": Enemy_sub_type.BEAST,
        "xp_reward": 60,
        "gold_reward": 3,
        "loot_table": [],
        "behavior_tag": Enemy_behavior_tag.AGGRESSIVE
    },
    Enemy_type.ENEMY_ORC: {
        "name": "Orc",
        "hp": 50,
        "damage": 7,
        "defence": 5,
        "rarity": Enemy_Rarity.RARE,
        "sub_type": Enemy_sub_type.HUMANOID,
        "xp_reward": 100,
        "gold_reward": 20,
        "loot_table": [],
        "behavior_tag": Enemy_behavior_tag.SLOW
    },
    Enemy_type.ENEMY_BOSS_DRAGON : {
        "name": "Dragon",
        "hp": 150,
        "damage": 40,
        "defence": 28,
        "rarity": Enemy_Rarity.BOSS,
        "sub_type": Enemy_sub_type.DRAGON,
        "xp_reward": 1800,
        "gold_reward": 450,
        "loot_table": [],
        "behavior_tag": Enemy_behavior_tag.HULKING
    }
}

def spawn_enemy(enemy_type):
    data = ENEMY_DEFINITIONS[enemy_type].copy()
    
    #adds the missing constructor to the enemy class since we use it as a dict key 
    # without having it in the enemy definition part of the code
    data["type"] = enemy_type 


    return Enemy(**data)