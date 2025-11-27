from Character_class import Character
from Enemy_class import Enemy
from World_gen_code.Dungeon_room_code import Room
from Heroes import Warrior
from Item_class import Item_Type, Items

class Combat_State():
    def __init__(self, player: Character, enemy_list: list[Enemy]):
        self.player = player
        self.enemy_list = enemy_list
        self.round_number = 0
        self.log = []
        self.is_running = True
        self.turn_order = []

    def alive_enemies(self) -> list[Enemy]:
        return [enemy for enemy in self.enemy_list if enemy.is_alive()]

OUTCOME = {
    "actor": str,
    "target": str,
    "damage": int,
    "blocked": bool,
    "critical": bool,
    "died": bool,
    "extra": {}
}


class Action():
    def __init__(self, actor: Character, action_type: str, target: Character, skill_id = None, item_id = None):
        self.actor = actor
        self.action_type = action_type
        self.target = target
        self.skill_id = skill_id
        self.item_id = item_id


class Status():
    def __init__(self, id: str, remaining_turns: int, magnitude: int | dict | None, source: str | None):
        self.id = id
        self.remaining_turns = remaining_turns
        self.source = source
        self.magnitude = magnitude


def start_encounter(player: Character, room: Room):
    enemy_list = room.contents["enemies"]

    combat = Combat_State(player=player, enemy_list=enemy_list)
    combat.is_running = True

    count = len(enemy_list)
    verb = "enemies" if count > 1 else "enemy"
    combat.log.append(f"Encounter started: you face {count} {verb}")


    while combat.is_running:
        combat.turn_order = [player] + enemy_list

        for actor in combat.turn_order:
            if not actor.is_alive():
                continue
            if not combat.is_running:
                break

            if actor is combat.player:
                action = ask_player_for_action(actor, combat)
                resolve_action(action, actor, combat)

            elif actor in combat.enemy_list:
                ai_action = decide_enemy_action(actor, combat)
                resolve_action(ai_action, actor, combat)
            

            if not combat.alive_enemies():
                combat.is_running = False
                return "Victory!"
            if not actor.is_alive():
                combat.is_running = False
                return "Defeat..."



def ask_player_for_action(actor, combat_state):
    while True:
        action = input("What do you wish to do: attack, use item, or flee?\n:").strip().lower()

        if action in ("attack", "use item", "flee"):
            break
        print("Invalid action.")
    
    match action:
        case "attack":
            while True:
                target = input("From left to right who do you want to hit in a numerical value?\n")
                target = target.strip()
                
                try:
                    idx = int(target)
                    return idx
                except ValueError:
                    print("Please enter a number")
                    continue
                

        case "use item":
            return Action(actor, "item", actor)

        case "flee":
            return Action(actor, "flee", None)
