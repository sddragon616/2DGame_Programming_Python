import json
from pico2d import *


Item_data_file = open('UnitData\\Item.json', 'r')
Item_Data = json.load(Item_data_file)
Item_data_file.close()


class Item:
    def __init__(self, numbers):
        self.image = None
        self.number = numbers
        self.use_sound = None

    def use(self):  # Item 클래스의 부모 사용 함수. 이 함수가 False를 return하면 아이템을 사용할 수 없다.
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
        if self.image is None:
            self.image = load_image('Resource_Image\\Item001_HP_Potion.png')
        if self.use_sound is None:
            self.use_sound = load_wav('Resource_Sound\\Effect_Sound\\Drinking.wav')
            self.use_sound.set_volume(64)

    def use(self, user):
        if super(HpPotion, self).use():
            user.hp_heal(self.healing)


class MpPotion(Item):
    def __init__(self, numbers):
        super(MpPotion, self).__init__(numbers)
        self.healing = Item_Data['MP_Potion']['Healing']
        if self.image is None:
            self.image = load_image('Resource_Image\\Item002_MP_Potion.png')
        if self.use_sound is None:
            self.use_sound = load_wav('Resource_Sound\\Effect_Sound\\Drinking.wav')
            self.use_sound.set_volume(64)

    def use(self, user):
        if super(MpPotion, self).use():
            user.mp_heal(self.healing)


class StaminaPotion(Item):
    def __init__(self, numbers):
        super(StaminaPotion, self).__init__(numbers)
        self.healing = Item_Data['SP_Potion']['Healing']
        if self.image is None:
            self.image = load_image('Resource_Image\\Item003_Stamina_Potion.png')
        if self.use_sound is None:
            self.use_sound = load_wav('Resource_Sound\\Effect_Sound\\Drinking.wav')
            self.use_sound.set_volume(64)

    def use(self, user):
        if super(StaminaPotion, self).use():
            user.sp_heal(self.healing)
