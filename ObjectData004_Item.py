import json


Item_data_file = open('UnitData\\Item.txt', 'r')
Item_Data = json.load(Item_data_file)
Item_data_file.close()


class Item:
    def __init__(self, numbers):
        self.number = numbers

    def use(self):
        if self.number > 0:
            self.number -= 1
            return True
        else:
            return False


class HpPotion(Item):
    def __init__(self, numbers):
        super(HpPotion, self).__init__(numbers)
        self.healing = Item_Data['HP_Potion']['Healing']

    def use(self, user):
        if super(HpPotion, self).use():
            user.hp_heal(self.healing)

