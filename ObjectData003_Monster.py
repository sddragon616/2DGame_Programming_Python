from ObjectData000_BaseObject_BaseUnit import *
from random import *
import Project_SceneFrameWork


Monster_data_file = open('UnitData\\Monster.json', 'r')
Monster_Data = json.load(Monster_data_file)
Monster_data_file.close()

# define
STAND = 0  # 서 있기
WALK = 1   # 걷기

PIXEL_PER_METER = (32.0 / 1.0)           # 32pixel == 1m

NON_PREEMPTIVE = 0  # 공격받기 전 까지는 비 선제 공격
PREEMPTIVE = 1      # 시야 내 발견 시 선제 공격
CHASE = 2           # 시작부터 추적


class Monster(BaseUnit):
    def __init__(self, hp, max_hp, mp, max_mp, stamina, max_stamina,
                 strength, defense, magic, magic_resist, move_speed, atk_speed, sight, experience, ai_type):
        super(Monster, self).__init__(hp, max_hp, mp, max_mp, stamina, max_stamina,
                                      strength, defense, magic, magic_resist, move_speed, atk_speed)
        self.frame = 0                  # 애니메이션을 출력하기 위한 프레임변수
        self.MP = mp                    # 현재 MP, 마법 스킬을 사용하기 위한 자원
        self.MAX_MP = max_mp            # 최대 MP
        self.STAMINA = stamina          # 현재 SP, 물리 스킬을 사용하기 위한 자원
        self.MAX_STAMINA = max_stamina  # 최대 SP, 물리 스킬을 사용하기 위한 자원
        self.STR = strength             # 물리 공격력
        self.MAG = magic                # 마법 공격력
        self.sight = sight              # 몬스터의 시야
        self.get_exp = experience       # 몬스터를 쓰러뜨리면 획득할 수 있는 경험치량
        self.AI_type = ai_type          # 해당 몬스터의 인공지능 형태

        self.dir = 2
        self.state = STAND
        self.exp_pay = False            # 이 몬스터가 경험치를 지급했는가 여부
        self.contact = False            # 이 몬스터가 유저를 인식했는가 여부
        self.box_draw_Trigger = False

        self.distance = 0

        self.image = None
        self.MONSTER_HP_BAR = None
        self.death_sound = None

    def update(self, frame_time, user, others):
        if self.death() is True:            # 대상이 사망했는가>
            if self.exp_pay is False:
                self.get_experience(user)
                self.exp_pay = True
        else:                               # 대상이 사망하지 않았다면
            if self.AI_type is PREEMPTIVE:
                if self.recognize(user) and user.death() is False:      # 생존중인 플레이어가 시야 내에 접근하였을 때
                    self.contact = True     # 플레이어를 인식
            elif self.AI_type is NON_PREEMPTIVE:
                if self.HP < self.MAX_HP:   # 플레이어에게 피격당하여 HP가 깎였을 때
                    self.contact = True     # 플레이어를 인식
            elif self.AI_type is CHASE:
                self.contact = True         # 플레이어를 인식
            if user.death() is True:    # 플레이어가 사망하였을 때
                self.state = STAND      # 대기
                self.contact = False    # 플레이어 인식을 해제
            if self.contact:            # 플레이어를 인식한 경우
                self.state = WALK
                self.user_chase(frame_time, user)
            self.distance = self.RUN_SPEED_PPS * frame_time
            self.total_frames_run += self.FRAMES_PER_ACTION_run * self.ACTION_PER_TIME_run * frame_time
            self.frame = int(self.total_frames_run) % 3
            # 바라보는 방향에 따라, 현재 걷기 상태라면 이동한다.
            if self.state is WALK:
                if self.dir is 2:
                    self.y = max(0, self.y - self.distance)
                elif self.dir is 8:
                    self.y = min(self.background.h, self.y + self.distance)
                elif self.dir is 4:
                    self.x = max(0, self.x - self.distance)
                elif self.dir is 6:
                    self.x = min(self.background.w, self.x + self.distance)
                elif self.dir is 1:
                    self.x = max(0, self.x - self.distance)
                    self.y = max(0, self.y - self.distance)
                elif self.dir is 3:
                    self.x = min(self.background.w, self.x + self.distance)
                    self.y = max(0, self.y - self.distance)
                elif self.dir is 7:
                    self.x = max(0, self.x - self.distance)
                    self.y = min(self.background.h, self.y + self.distance)
                elif self.dir is 9:
                    self.x = min(self.background.w, self.x + self.distance)
                    self.y = min(self.background.h, self.y + self.distance)
                if others is not []:
                    for other in others:
                        if collide(self, other):
                            if self.dir is 2:
                                self.y = max(0, self.y + self.distance)
                            elif self.dir is 8:
                                self.y = min(self.background.h, self.y - self.distance)
                            elif self.dir is 4:
                                self.x = max(0, self.x + self.distance)
                            elif self.dir is 6:
                                self.x = min(self.background.w, self.x - self.distance)
                            elif self.dir is 1:
                                self.x = max(0, self.x + self.distance)
                                self.y = max(0, self.y + self.distance)
                            elif self.dir is 3:
                                self.x = min(self.background.w, self.x - self.distance)
                                self.y = max(0, self.y + self.distance)
                            elif self.dir is 7:
                                self.x = max(0, self.x + self.distance)
                                self.y = min(self.background.h, self.y - self.distance)
                            elif self.dir is 9:
                                self.x = min(self.background.w, self.x - self.distance)
                                self.y = min(self.background.h, self.y - self.distance)
        # 플레이어에게 공격받았을 때 무적을 0.25초간 걸어서 연속프레임 공격 방지
        if self.invincibility is True:
            self.invincible_time += frame_time
            if self.invincible_time > 0.25:
                self.invincibility = False
                self.invincible_time = 0

    def user_chase(self, frame_time, user):
        if user.x < self.x - (self.width / 2):
            if user.y < self.y - (self.height / 2):
                self.dir = 1
            elif user.y > self.y + (self.height / 2):
                self.dir = 7
            else:
                self.dir = 4
        elif user.x > self.x + (self.width / 2):
            if user.y < self.y - (self.height / 2):
                self.dir = 3
            elif user.y > self.y + (self.height / 2):
                self.dir = 9
            else:
                self.dir = 6
        elif user.y > self.y + (self.height / 2):
            self.dir = 8
        elif user.y < self.y - (self.height / 2):
            self.dir = 2

    def hit_by_str(self, damage, direction, others):
        super(Monster, self).hit_by_str(damage)
        if self.hit_sound is not None:
            self.hit_sound_play()
        self.knock_back(direction, others)

    def hit_by_mag(self, damage, direction, others):
        super(Monster, self).hit_by_mag(damage)
        if self.hit_sound is not None:
            self.hit_sound_play()
        self.knock_back(direction, others)

    def get_experience(self, user):
        user.get_exp(self.get_exp)

    def get_bb(self):
        return self.x - self.width / 4, self.y - self.height / 4, self.x + self.width / 4, self.y + self.height / 4

    def draw_bb(self):
        draw_rectangle(self.get_bb()[0] - self.background.window_left,
                       self.get_bb()[1] - self.background.window_bottom,
                       self.get_bb()[2] - self.background.window_left,
                       self.get_bb()[3] - self.background.window_bottom)
        draw_rectangle(self.get_contact_box()[0] - self.background.window_left,
                       self.get_contact_box()[1] - self.background.window_bottom,
                       self.get_contact_box()[2] - self.background.window_left,
                       self.get_contact_box()[3] - self.background.window_bottom)

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

    def draw_hp_bar(self):
        # Border
        self.MONSTER_HP_BAR.clip_draw(0, 6, 10, 6,
                                      self.x - self.background.window_left,
                                      self.y - self.background.window_bottom + int(self.height / 2) + 12,
                                      int(self.width * 6 / 5), 12)
        # HPs
        self.MONSTER_HP_BAR.clip_draw(0, 0, 10, 6,
                                      self.x - self.background.window_left -
                                      int(self.width * ((self.MAX_HP-self.HP) / (self.MAX_HP * 2))),
                                      self.y - self.background.window_bottom + int(self.height / 2) + 12,
                                      int(self.width * 6 / 5)*(self.HP/self.MAX_HP), 12)


class Fly(Monster):
    global Monster_Data

    def __init__(self, map_coord_data, map_height):
        super(Fly, self).__init__(Monster_Data['Fly']['HP'], Monster_Data['Fly']['MAX_HP'],
                                  Monster_Data['Fly']['MP'], Monster_Data['Fly']['MAX_MP'],
                                  Monster_Data['Fly']['Stamina'], Monster_Data['Fly']['MAX_Stamina'],
                                  Monster_Data['Fly']['STR'], Monster_Data['Fly']['DEF'],
                                  Monster_Data['Fly']['MAG'], Monster_Data['Fly']['MR'],
                                  Monster_Data['Fly']['MOVE_SPEED'], Monster_Data['Fly']['ATK_SPEED'],
                                  Monster_Data['Fly']['Sight'], Monster_Data['Fly']['Experience'],
                                  Monster_Data['Fly']['AI_Type'])
        self.width = self.height = 32

        self.dir = randint(1, 9)
        if self.dir == 5:
            self.dir = 2

        if self.hit_sound is None:
            self.hit_sound = load_wav('Resource_Sound\\Effect_Sound\\Damage1.wav')
            self.hit_sound.set_volume(64)

        self.x, self.y = map_coord_data['x'] + self.width / 2, map_height - (map_coord_data['y'] + self.height / 2)

    def set_coordinates(self, x, y):
        self.x, self.y = x, y

    def draw(self):
        if self.dir is 2:
            self.image.clip_draw(self.frame * self.width, self.height * 9 + 16, self.width, self.height,
                                 self.x - self.background.window_left, self.y - self.background.window_bottom)
        elif self.dir is 8:
            self.image.clip_draw(self.frame * self.width, self.height * 5 + 16, self.width, self.height,
                                 self.x - self.background.window_left, self.y - self.background.window_bottom)
        elif self.dir is 4:
            self.image.clip_draw(self.frame * self.width, self.height * 7 + 16, self.width, self.height,
                                 self.x - self.background.window_left, self.y - self.background.window_bottom)
        elif self.dir is 6:
            self.image.clip_draw((self.frame + 3) * self.width, self.height * 7 + 16, self.width, self.height,
                                 self.x - self.background.window_left, self.y - self.background.window_bottom)
        elif self.dir is 1:
            self.image.clip_draw(self.frame * self.width, self.height * 8 + 16, self.width, self.height,
                                 self.x - self.background.window_left, self.y - self.background.window_bottom)
        elif self.dir is 3:
            self.image.clip_draw((self.frame + 3) * self.width, self.height * 8 + 16, self.width, self.height,
                                 self.x - self.background.window_left, self.y - self.background.window_bottom)
        elif self.dir is 7:
            self.image.clip_draw(self.frame * self.width, self.height * 6 + 16, self.width, self.height,
                                 self.x - self.background.window_left, self.y - self.background.window_bottom)
        elif self.dir is 9:
            self.image.clip_draw((self.frame + 3) * self.width, self.height * 6 + 16, self.width, self.height,
                                 self.x - self.background.window_left, self.y - self.background.window_bottom)
        self.draw_hp_bar()

    def get_bb(self):
        return self.x - self.width / 4, self.y - self.height / 4, self.x + self.width / 4, self.y + self.height / 4


class Crab(Monster):
    global Monster_Data

    def __init__(self, map_coord_data, map_height):
        super(Crab, self).__init__(Monster_Data['Crab']['HP'], Monster_Data['Crab']['MAX_HP'],
                                   Monster_Data['Crab']['MP'], Monster_Data['Crab']['MAX_MP'],
                                   Monster_Data['Crab']['Stamina'], Monster_Data['Crab']['MAX_Stamina'],
                                   Monster_Data['Crab']['STR'], Monster_Data['Crab']['DEF'],
                                   Monster_Data['Crab']['MAG'], Monster_Data['Crab']['MR'],
                                   Monster_Data['Crab']['MOVE_SPEED'], Monster_Data['Crab']['ATK_SPEED'],
                                   Monster_Data['Crab']['Sight'], Monster_Data['Crab']['Experience'],
                                   Monster_Data['Crab']['AI_Type'])
        self.width = self.height = 32
        self.image = load_image('Resource_Image\\Monster002_crab.png')
        self.dir = randint(1, 9)
        if self.dir == 5:
            self.dir = 2

        if self.hit_sound is None:
            self.hit_sound = load_wav('Resource_Sound\\Effect_Sound\\Slash12.wav')
            self.hit_sound.set_volume(64)
        self.x, self.y = map_coord_data['x'] + self.width / 2, map_height - (map_coord_data['y'] + self.height / 2)

    def set_coordinates(self, x, y):
        self.x, self.y = x, y

    def draw(self):
        if self.dir is 2:
            self.image.clip_draw(self.frame * self.width, self.height * 4, self.width, self.height,
                                 self.x - self.background.window_left, self.y - self.background.window_bottom)
        elif self.dir is 8:
            self.image.clip_draw(self.frame * self.width, self.height * 0, self.width, self.height,
                                 self.x - self.background.window_left, self.y - self.background.window_bottom)
        elif self.dir is 4:
            self.image.clip_draw(self.frame * self.width, self.height * 2, self.width, self.height,
                                 self.x - self.background.window_left, self.y - self.background.window_bottom)
        elif self.dir is 6:
            self.image.clip_draw((self.frame + 3) * self.width, self.height * 2, self.width, self.height,
                                 self.x - self.background.window_left, self.y - self.background.window_bottom)
        elif self.dir is 1:
            self.image.clip_draw(self.frame * self.width, self.height * 3, self.width, self.height,
                                 self.x - self.background.window_left, self.y - self.background.window_bottom)
        elif self.dir is 3:
            self.image.clip_draw((self.frame + 3) * self.width, self.height * 3, self.width, self.height,
                                 self.x - self.background.window_left, self.y - self.background.window_bottom)
        elif self.dir is 7:
            self.image.clip_draw(self.frame * self.width, self.height * 1, self.width, self.height,
                                 self.x - self.background.window_left, self.y - self.background.window_bottom)
        elif self.dir is 9:
            self.image.clip_draw((self.frame + 3) * self.width, self.height * 1, self.width, self.height,
                                 self.x - self.background.window_left, self.y - self.background.window_bottom)
        self.draw_hp_bar()

    def get_bb(self):
        return self.x - self.width / 3, self.y - self.height / 3, self.x + self.width / 3, self.y + self.height / 3


class Skull_Golem(Monster):
    global Monster_Data

    def __init__(self, map_coord_data, map_height):
        super(Skull_Golem, self).__init__(Monster_Data['Skull Golem']['HP'], Monster_Data['Skull Golem']['MAX_HP'],
                                          Monster_Data['Skull Golem']['MP'], Monster_Data['Skull Golem']['MAX_MP'],
                                          Monster_Data['Skull Golem']['Stamina'],
                                          Monster_Data['Skull Golem']['MAX_Stamina'],
                                          Monster_Data['Skull Golem']['STR'], Monster_Data['Skull Golem']['DEF'],
                                          Monster_Data['Skull Golem']['MAG'], Monster_Data['Skull Golem']['MR'],
                                          Monster_Data['Skull Golem']['MOVE_SPEED'],
                                          Monster_Data['Skull Golem']['ATK_SPEED'],
                                          Monster_Data['Skull Golem']['Sight'],
                                          Monster_Data['Skull Golem']['Experience'],
                                          Monster_Data['Skull Golem']['AI_Type'])
        self.width = self.height = 32
        self.image = load_image('Resource_Image\\Monster003_SkullGolem.png')
        self.dir = randint(1, 9)
        if self.dir == 5:
            self.dir = 2

        if self.hit_sound is None:
            self.hit_sound = load_wav('Resource_Sound\\Effect_Sound\\Slash11.wav')
            self.hit_sound.set_volume(64)

        self.x, self.y = map_coord_data['x'] + self.width / 2, map_height - (map_coord_data['y'] + self.height / 2)

    def set_coordinates(self, x, y):
        self.x, self.y = x, y

    def draw(self):
        if self.dir is 2:
            self.image.clip_draw(self.frame * self.width, self.height * 4, self.width, self.height,
                                 self.x - self.background.window_left, self.y - self.background.window_bottom,
                                 self.width * 2, self.height * 2)
        elif self.dir is 8:
            self.image.clip_draw(self.frame * self.width, self.height * 0, self.width, self.height,
                                 self.x - self.background.window_left, self.y - self.background.window_bottom,
                                 self.width * 2, self.height * 2)
        elif self.dir is 4:
            self.image.clip_draw(self.frame * self.width, self.height * 2, self.width, self.height,
                                 self.x - self.background.window_left, self.y - self.background.window_bottom,
                                 self.width * 2, self.height * 2)
        elif self.dir is 6:
            self.image.clip_draw((self.frame + 3) * self.width, self.height * 2, self.width, self.height,
                                 self.x - self.background.window_left, self.y - self.background.window_bottom,
                                 self.width * 2, self.height * 2)
        elif self.dir is 1:
            self.image.clip_draw(self.frame * self.width, self.height * 3, self.width, self.height,
                                 self.x - self.background.window_left, self.y - self.background.window_bottom,
                                 self.width * 2, self.height * 2)
        elif self.dir is 3:
            self.image.clip_draw((self.frame + 3) * self.width, self.height * 3, self.width, self.height,
                                 self.x - self.background.window_left, self.y - self.background.window_bottom,
                                 self.width * 2, self.height * 2)
        elif self.dir is 7:
            self.image.clip_draw(self.frame * self.width, self.height * 1, self.width, self.height,
                                 self.x - self.background.window_left, self.y - self.background.window_bottom,
                                 self.width * 2, self.height * 2)
        elif self.dir is 9:
            self.image.clip_draw((self.frame + 3) * self.width, self.height * 1, self.width, self.height,
                                 self.x - self.background.window_left, self.y - self.background.window_bottom,
                                 self.width * 2, self.height * 2)

    def get_bb(self):
        return self.x - self.width, self.y - self.height, self.x + self.width, self.y + self.height


class Spear(Monster):
    global Monster_Data

    def __init__(self, map_coord_data, map_height):
        super(Spear, self).__init__(Monster_Data['Spear']['HP'], Monster_Data['Spear']['MAX_HP'],
                                    Monster_Data['Spear']['MP'], Monster_Data['Spear']['MAX_MP'],
                                    Monster_Data['Spear']['Stamina'], Monster_Data['Spear']['MAX_Stamina'],
                                    Monster_Data['Spear']['STR'], Monster_Data['Spear']['DEF'],
                                    Monster_Data['Spear']['MAG'], Monster_Data['Spear']['MR'],
                                    Monster_Data['Spear']['MOVE_SPEED'], Monster_Data['Spear']['ATK_SPEED'],
                                    Monster_Data['Spear']['Sight'], Monster_Data['Spear']['Experience'],
                                    Monster_Data['Spear']['AI_Type'])
        self.width = self.height = 64
        self.image = load_image('Resource_Image\\Monster004_Spear.png')
        self.dir = randint(1, 9)
        if self.dir == 5:
            self.dir = 2

        if self.hit_sound is None:
            self.hit_sound = load_wav('Resource_Sound\\Effect_Sound\\Slash11.wav')
            self.hit_sound.set_volume(64)
        self.x, self.y = map_coord_data['x'] + self.width / 2, map_height - (map_coord_data['y'] + self.height / 2)

    def set_coordinates(self, x, y):
        self.x, self.y = x, y

    def draw(self):
        if self.dir is 2:
            self.image.clip_draw(self.frame * self.width, self.height * 4, self.width, self.height,
                                 self.x - self.background.window_left, self.y - self.background.window_bottom,
                                 self.width * 2, self.height * 2)
        elif self.dir is 8:
            self.image.clip_draw(self.frame * self.width, self.height * 0, self.width, self.height,
                                 self.x - self.background.window_left, self.y - self.background.window_bottom,
                                 self.width * 2, self.height * 2)
        elif self.dir is 4:
            self.image.clip_draw(self.frame * self.width, self.height * 2, self.width, self.height,
                                 self.x - self.background.window_left, self.y - self.background.window_bottom,
                                 self.width * 2, self.height * 2)
        elif self.dir is 6:
            self.image.clip_draw((self.frame + 3) * self.width, self.height * 2, self.width, self.height,
                                 self.x - self.background.window_left, self.y - self.background.window_bottom,
                                 self.width * 2, self.height * 2)
        elif self.dir is 1:
            self.image.clip_draw(self.frame * self.width, self.height * 3, self.width, self.height,
                                 self.x - self.background.window_left, self.y - self.background.window_bottom,
                                 self.width * 2, self.height * 2)
        elif self.dir is 3:
            self.image.clip_draw((self.frame + 3) * self.width, self.height * 3, self.width, self.height,
                                 self.x - self.background.window_left, self.y - self.background.window_bottom,
                                 self.width * 2, self.height * 2)
        elif self.dir is 7:
            self.image.clip_draw(self.frame * self.width, self.height * 1, self.width, self.height,
                                 self.x - self.background.window_left, self.y - self.background.window_bottom,
                                 self.width * 2, self.height * 2)
        elif self.dir is 9:
            self.image.clip_draw((self.frame + 3) * self.width, self.height * 1, self.width, self.height,
                                 self.x - self.background.window_left, self.y - self.background.window_bottom,
                                 self.width * 2, self.height * 2)
        self.draw_hp_bar()

    def get_bb(self):
        return self.x - self.width / 2, self.y - self.height / 2, self.x + self.width / 2, self.y + self.height / 2


class Slasher(Monster):
    global Monster_Data

    def __init__(self, map_coord_data, map_height):
        super(Slasher, self).__init__(Monster_Data['Slasher']['HP'], Monster_Data['Slasher']['MAX_HP'],
                                      Monster_Data['Slasher']['MP'], Monster_Data['Slasher']['MAX_MP'],
                                      Monster_Data['Slasher']['Stamina'], Monster_Data['Slasher']['MAX_Stamina'],
                                      Monster_Data['Slasher']['STR'], Monster_Data['Slasher']['DEF'],
                                      Monster_Data['Slasher']['MAG'], Monster_Data['Slasher']['MR'],
                                      Monster_Data['Slasher']['MOVE_SPEED'], Monster_Data['Slasher']['ATK_SPEED'],
                                      Monster_Data['Slasher']['Sight'], Monster_Data['Slasher']['Experience'],
                                      Monster_Data['Slasher']['AI_Type'])
        self.width = self.height = 32
        self.image = load_image('Resource_Image\\Monster005_Slasher.png')
        self.dir = randint(1, 9)
        if self.dir == 5:
            self.dir = 2

        if self.hit_sound is None:
            self.hit_sound = load_wav('Resource_Sound\\Effect_Sound\\Slash10.wav')
            self.hit_sound.set_volume(128)

        self.x, self.y = map_coord_data['x'] + self.width / 2, map_height - (map_coord_data['y'] + self.height / 2)

    def set_coordinates(self, x, y):
        self.x, self.y = x, y

    def draw(self):
        if self.dir is 2:
            self.image.clip_draw(self.frame * self.width, self.height * 4, self.width, self.height,
                                 self.x - self.background.window_left, self.y - self.background.window_bottom,
                                 self.width * 2, self.height * 2)
        elif self.dir is 8:
            self.image.clip_draw(self.frame * self.width, self.height * 0, self.width, self.height,
                                 self.x - self.background.window_left, self.y - self.background.window_bottom,
                                 self.width * 2, self.height * 2)
        elif self.dir is 4:
            self.image.clip_draw(self.frame * self.width, self.height * 2, self.width, self.height,
                                 self.x - self.background.window_left, self.y - self.background.window_bottom,
                                 self.width * 2, self.height * 2)
        elif self.dir is 6:
            self.image.clip_draw((self.frame + 3) * self.width, self.height * 2, self.width, self.height,
                                 self.x - self.background.window_left, self.y - self.background.window_bottom,
                                 self.width * 2, self.height * 2)
        elif self.dir is 1:
            self.image.clip_draw(self.frame * self.width, self.height * 3, self.width, self.height,
                                 self.x - self.background.window_left, self.y - self.background.window_bottom,
                                 self.width * 2, self.height * 2)
        elif self.dir is 3:
            self.image.clip_draw((self.frame + 3) * self.width, self.height * 3, self.width, self.height,
                                 self.x - self.background.window_left, self.y - self.background.window_bottom,
                                 self.width * 2, self.height * 2)
        elif self.dir is 7:
            self.image.clip_draw(self.frame * self.width, self.height * 1, self.width, self.height,
                                 self.x - self.background.window_left, self.y - self.background.window_bottom,
                                 self.width * 2, self.height * 2)
        elif self.dir is 9:
            self.image.clip_draw((self.frame + 3) * self.width, self.height * 1, self.width, self.height,
                                 self.x - self.background.window_left, self.y - self.background.window_bottom,
                                 self.width * 2, self.height * 2)
        self.draw_hp_bar()

    def get_bb(self):
        return self.x - self.width, self.y - self.height, self.x + self.width, self.y + self.height


def collide(a, b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()
    if left_a > right_b:
        return False
    if right_a < left_b:
        return False
    if top_a < bottom_b:
        return False
    if bottom_a > top_b:
        return False
    return True
