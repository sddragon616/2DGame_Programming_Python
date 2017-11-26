from ObjectData000_BaseObject_BaseUnit import *
from random import *
import Project_SceneFrameWork


Monster_data_file = open('UnitData\\Monster.txt', 'r')
Monster_Data = json.load(Monster_data_file)
Monster_data_file.close()


STAND = 0  # 서 있기
WALK = 1   # 걷기

PIXEL_PER_METER = (32.0 / 1.0)           # 32pixel == 1m


class Monster(BaseUnit):
    def __init__(self, hp, max_hp, mp, max_mp, stamina, max_stamina,
                 strength, defense, magic, magic_resist, move_speed, atk_speed, sight, experience):
        super(Monster, self).__init__(hp, max_hp, mp, max_mp, stamina, max_stamina,
                                      strength, defense, magic, magic_resist, move_speed, atk_speed)
        self.frame = 0                  # 애니메이션을 출력하기 위한 프레임변수
        self.MP = mp                    # 현재 MP, 마법 스킬을 사용하기 위한 자원
        self.MAX_MP = max_mp            # 최대 MP
        self.STAMINA = stamina          # 현재 SP, 물리 스킬을 사용하기 위한 자원
        self.MAX_STAMINA = max_stamina  # 최대 SP, 물리 스킬을 사용하기 위한 자원
        self.STR = strength             # 물리 공격력
        self.MAG = magic                # 마법 공격력
        self.sight = sight  # 몬스터의 시야
        self.get_exp = experience  # 몬스터를 쓰러뜨리면 획득할 수 있는 경험치량

        self.image = None
        self.dir = 2

        self.exp_pay = False            # 이 몬스터가 경험치를 지급했는가 여부
        self.box_draw = False

    def update(self, frame_time, user):
        if self.recognize(user):
            self.auto_intelligence(frame_time, user)
        if self.death() is True:
            if self.exp_pay is False:
                self.get_experience(user)
                self.exp_pay = True

    def auto_intelligence(self, frame_time, user):
        user.get_bb()

    def get_experience(self, user):
        user.get_exp(self.get_exp)

    def get_bb(self):
        return self.x - self.width / 4, self.y - self.height / 4, self.x + self.width / 4, self.y + self.height / 4

    def draw_bb(self):
        draw_rectangle(*self.get_bb())

    def get_contact_box(self):
        return self.x - self.sight, self.y - self.sight, self.x + self.sight, self.y + self.sight

    def recognize(self, user):
        left_a, bottom_a, right_a, top_a = self.get_contact_box()
        left_b, bottom_b, right_b, top_b = user.get_bb()
        if left_a > right_b:
            return False
        if right_a < left_b:
            return False
        if top_a < bottom_b:
            return False
        if bottom_a > top_b:
            return False
        return True


class Fly(Monster):
    global Monster_Data

    def __init__(self):
        super(Fly, self).__init__(Monster_Data['Fly']['HP'], Monster_Data['Fly']['MAX_HP'],
                                  Monster_Data['Fly']['MP'], Monster_Data['Fly']['MAX_MP'],
                                  Monster_Data['Fly']['Stamina'], Monster_Data['Fly']['MAX_Stamina'],
                                  Monster_Data['Fly']['STR'], Monster_Data['Fly']['DEF'],
                                  Monster_Data['Fly']['MAG'], Monster_Data['Fly']['MR'],
                                  Monster_Data['Fly']['MOVE_SPEED'], Monster_Data['Fly']['ATK_SPEED'],
                                  Monster_Data['Fly']['Sight'], Monster_Data['Fly']['Experience'])
        self.width = self.height = 32
        self.image = load_image('Resource_Image\\Monster001_fly.png')
        self.dir = 2
        self.state = STAND
        self.x, self.y = randint(0, 1024), randint(0, 768)

    def draw(self):
        if self.dir == 2 or self.dir == 5:
            self.image.clip_draw(self.frame * self.width, self.height * 9 + 16, self.width, self.height, self.x, self.y)

    def get_bb(self):
        return self.x - self.width / 4, self.y - self.height / 4, self.x + self.width / 4, self.y + self.height / 4

    def draw_bb(self):
        draw_rectangle(*self.get_bb())



