from Character_class import Character
from World_gen_code.Dungeon_room_code import Room

class Combat_State():
    def __init__(self, player: Character, room: Room,):
        self.player = player
        self.room_enemy_contents = room.contents["enemies"]
        self.round_number = 1
        self.log = [str]
        self.is_running = True
        self.player_turn_index = 0

        self.turn_order = [self.player]
        for enemy in self.room_enemy_contents:
            if enemy is None:
                continue
            self.turn_order.append(enemy)
            
