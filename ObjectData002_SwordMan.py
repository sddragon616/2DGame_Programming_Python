from ObjectData001_BasePlayer import *
import json

SwordMan_data_file = open('UnitData\\SwordMan.txt', 'r')
SwordMan_data = json.load(SwordMan_data_file)
SwordMan_data_file.close()


class SwordMan(Player):
    def __init__(self, x, y):
        super(SwordMan, self).__init__(SwordMan_data[SwordMan]['HP'], SwordMan_data[SwordMan]['MAX_HP'], SwordMan_data[SwordMan]['MP'], SwordMan_data[SwordMan]['MAX_MP'], SwordMan_data[SwordMan]['Stamina'], SwordMan_data[SwordMan]['MAX_Stamina'], SwordMan_data[SwordMan]['STR'], SwordMan_data[SwordMan]['DEF'], SwordMan_data[SwordMan]['MAG'], SwordMan_data[SwordMan]['MR'], SwordMan_data[SwordMan]['MOVE_SPEED'], SwordMan_data[SwordMan]['ATK_SPEED'])
        self.image = load_image("Resource_Image\\Player001_SwordMan.png")
        self.x = x
        self.y = y

    def show_stat(self):
        super(SwordMan, self).show_stat()
        print('\n')

