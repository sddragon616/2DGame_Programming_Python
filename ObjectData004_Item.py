import json
from pico2d import *


Item_data_file = open('UnitData\\Item.txt', 'r')
Item_Data = json.load(Item_data_file)
Item_data_file.close()


class Item:
    def __init__(self, numbers):
        self.number = numbers
        self.use_sound = None

    def use(self):
        if self.number > 0:
            if self.use_sound is not None:
                self.use_sound.play()
            self.number -= 1
            return True
        else:
            return False


class HpPotion(Item):
    def __init__(self, numbers):
        super(HpPotion, self).__init__(numbers)
        self.healing = Item_Data['HP_Potion']['Healing']
        if self.use_sound is None:
            self.use_sound = load_wav('Resource_Sound\\Effect_Sound\\Drinking.wav')
            self.use_sound.set_volume(64)

    def use(self, user):
        if super(HpPotion, self).use():
            user.hp_heal(self.healing)

