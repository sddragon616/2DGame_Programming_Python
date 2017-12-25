from ObjectData001_BasePlayer import *
import json


SwordMan_data_file = open('UnitData\\SwordMan.txt', 'r')
SwordMan_Data = json.load(SwordMan_data_file)
SwordMan_data_file.close()


class SwordMan(Player):
    global SwordMan_Data

    def __init__(self, x, y):
        super(SwordMan, self).__init__(SwordMan_Data['SwordMan']['HP'], SwordMan_Data['SwordMan']['MAX_HP'],
                                       SwordMan_Data['SwordMan']['MP'], SwordMan_Data['SwordMan']['MAX_MP'],
                                       SwordMan_Data['SwordMan']['Stamina'], SwordMan_Data['SwordMan']['MAX_Stamina'],
                                       SwordMan_Data['SwordMan']['STR'], SwordMan_Data['SwordMan']['DEF'],
                                       SwordMan_Data['SwordMan']['MAG'], SwordMan_Data['SwordMan']['MR'],
                                       SwordMan_Data['SwordMan']['MOVE_SPEED'], SwordMan_Data['SwordMan']['ATK_SPEED'])
        self.image = load_image("Resource_Image\\Player001_SwordMan.png")
        self.x = x
        self.y = y
        self.HpPotion.number += 2
        self.StaminaPotion.number += 1
        if self.attack_sound is None:
            self.attack_sound = load_wav('Resource_Sound\\Effect_Sound\\Slash12.wav')
            self.attack_sound.set_volume(64)
        if self.hit_sound is None:
            self.hit_sound = load_wav('Resource_Sound\\Effect_Sound\\Damage2.wav')
            self.hit_sound.set_volume(64)

    def show_stat(self):
        super(SwordMan, self).show_stat()
        print('\n')

    def handle_events(self, event):
        super(SwordMan, self).handle_events(event)
        print(self.x, self.y)
        if (event.type, event.key) == (SDL_KEYDOWN, SDLK_d):
            pass



