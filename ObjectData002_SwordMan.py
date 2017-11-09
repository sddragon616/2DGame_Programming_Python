from ObjectData001_BasePlayer import *
import json

SwordMan_data_file = open('UnitData\\SwordMan.txt', 'r')
sword_user_data = json.load(SwordMan_data_file)
SwordMan_data_file.close()


class SwordMan(Player):
    global sword_user_data

    def __init__(self, x, y):
        super(SwordMan, self).__init__(sword_user_data[SwordMan]['HP'], sword_user_data[SwordMan]['MAX_HP'], sword_user_data[SwordMan]['MP'], sword_user_data[SwordMan]['MAX_MP'], sword_user_data[SwordMan]['Stamina'], sword_user_data[SwordMan]['MAX_Stamina'], sword_user_data[SwordMan]['STR'], sword_user_data[SwordMan]['DEF'], sword_user_data[SwordMan]['MAG'], sword_user_data[SwordMan]['MR'], sword_user_data[SwordMan]['MOVE_SPEED'], sword_user_data[SwordMan]['ATK_SPEED'])
        self.image = load_image("Resource_Image\\Player001_SwordMan.png")
        self.x = x
        self.y = y

    def show_stat(self):
        super(SwordMan, self).show_stat()
        print('\n')

