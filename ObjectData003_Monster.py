from ObjectData000_BaseObject_BaseUnit import *
from random import *
import Resource_Manager as rssmgr
import math


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

        self.dir = 2                    # 몬스터가 바라보고 있는 진행 방향
        self.state = STAND
        self.exp_pay = False            # 이 몬스터가 경험치를 지급했는가 여부
        self.contact = False            # 이 몬스터가 유저를 인식했는가 여부
        self.box_draw_Trigger = False

        self.distance = 0               # 이동 거리

        self.fly_available = False      # 몬스터가 장애물을 뚫는 비행이 가능한가?

        self.max_move_frame = 3         # 그림파일의 이동 애니메이션 프레임 수

    def update(self, frame_time, user, others):
        if self.death() is True:            # 대상이 사망했는가>
            if self.exp_pay is False:
                self.get_experience(user)
                self.exp_pay = True
        else:                               # 대상이 사망하지 않았다면
            if self.AI_type is PREEMPTIVE:
                if self.recognize(user) and user.death() is False:      # 생존중인 플레이어가 시야 내에 접근하였을 때
                    self.contact = True     # 플레이어를 인식
                elif self.HP < self.MAX_HP:
                    self.contact = True
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
            self.frame = int(self.total_frames_run) % self.max_move_frame
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
                    self.x = max(0, self.x - (math.sqrt(0.5) * self.distance))
                    self.y = max(0, self.y - (math.sqrt(0.5) * self.distance))
                elif self.dir is 3:
                    self.x = min(self.background.w, self.x + (math.sqrt(0.5) * self.distance))
                    self.y = max(0, self.y - (math.sqrt(0.5) * self.distance))
                elif self.dir is 7:
                    self.x = max(0, self.x - (math.sqrt(0.5) * self.distance))
                    self.y = min(self.background.h, self.y + (math.sqrt(0.5) * self.distance))
                elif self.dir is 9:
                    self.x = min(self.background.w, self.x + (math.sqrt(0.5) * self.distance))
                    self.y = min(self.background.h, self.y + (math.sqrt(0.5) * self.distance))
                if self.fly_available is False:
                    if others:
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
                                    self.x = max(0, self.x + (math.sqrt(0.5) * self.distance))
                                    self.y = max(0, self.y + (math.sqrt(0.5) * self.distance))
                                elif self.dir is 3:
                                    self.x = min(self.background.w, self.x - (math.sqrt(0.5) * self.distance))
                                    self.y = max(0, self.y + (math.sqrt(0.5) * self.distance))
                                elif self.dir is 7:
                                    self.x = max(0, self.x + (math.sqrt(0.5) * self.distance))
                                    self.y = min(self.background.h, self.y - (math.sqrt(0.5) * self.distance))
                                elif self.dir is 9:
                                    self.x = min(self.background.w, self.x - (math.sqrt(0.5) * self.distance))
                                    self.y = min(self.background.h, self.y - (math.sqrt(0.5) * self.distance))
        # 플레이어에게 공격받았을 때 무적을 0.25초간 걸어서 연속프레임 공격 방지
        if self.invincibility is True:
            self.invincible_time += frame_time
            if self.invincible_time > 0.25:
                self.invincibility = False
                self.invincible_time = 0

    def user_chase(self, frame_time, user):
        if user.x + (user.width / 2) < self.x:
            if user.y + (user.height / 4) < self.y:
                self.dir = 1
            elif user.y - (user.height / 4) > self.y:
                self.dir = 7
            else:
                self.dir = 4
        elif user.x - (user.width / 2) > self.x:
            if user.y + (user.height / 4) < self.y:
                self.dir = 3
            elif user.y - (user.height / 4) > self.y:
                self.dir = 9
            else:
                self.dir = 6
        elif user.y - (user.height / 4) > self.y:
            self.dir = 8
        elif user.y + (user.height / 4) < self.y:
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
        rssmgr.UI_bar.image.clip_draw(0, 6, 10, 6,
                                      self.x - self.background.window_left,
                                      self.y - self.background.window_bottom + int(self.height / 2) + 12,
                                      int(self.width * 6 / 5), 12)
        # HP
        rssmgr.UI_bar.image.clip_draw(0, 0, 10, 6,
                                      self.x - self.background.window_left
                                      - int(self.width * ((self.MAX_HP-self.HP) / (self.MAX_HP * 2))),
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

        self.x, self.y = map_coord_data['x'] + self.width / 2, map_height - (map_coord_data['y'] + self.height / 2)

    def set_coordinates(self, x, y):
        self.x, self.y = x, y

    def draw(self):
        if rssmgr.fly is not None:
            if self.dir is 2:
                rssmgr.fly.image.clip_draw(self.frame * self.width, self.height * 9 + 16, self.width, self.height,
                                           self.x - self.background.window_left, self.y - self.background.window_bottom)
            elif self.dir is 8:
                rssmgr.fly.image.clip_draw(self.frame * self.width, self.height * 5 + 16, self.width, self.height,
                                           self.x - self.background.window_left, self.y - self.background.window_bottom)
            elif self.dir is 4:
                rssmgr.fly.image.clip_draw(self.frame * self.width, self.height * 7 + 16, self.width, self.height,
                                           self.x - self.background.window_left, self.y - self.background.window_bottom)
            elif self.dir is 6:
                rssmgr.fly.image.clip_draw((self.frame + 3) * self.width, self.height * 7 + 16, self.width, self.height,
                                           self.x - self.background.window_left, self.y - self.background.window_bottom)
            elif self.dir is 1:
                rssmgr.fly.image.clip_draw(self.frame * self.width, self.height * 8 + 16, self.width, self.height,
                                           self.x - self.background.window_left, self.y - self.background.window_bottom)
            elif self.dir is 3:
                rssmgr.fly.image.clip_draw((self.frame + 3) * self.width, self.height * 8 + 16, self.width, self.height,
                                           self.x - self.background.window_left, self.y - self.background.window_bottom)
            elif self.dir is 7:
                rssmgr.fly.image.clip_draw(self.frame * self.width, self.height * 6 + 16, self.width, self.height,
                                           self.x - self.background.window_left, self.y - self.background.window_bottom)
            elif self.dir is 9:
                rssmgr.fly.image.clip_draw((self.frame + 3) * self.width, self.height * 6 + 16, self.width, self.height,
                                           self.x - self.background.window_left, self.y - self.background.window_bottom)
            self.draw_hp_bar()

    def get_bb(self):
        return self.x - self.width / 4, self.y - self.height / 4, self.x + self.width / 4, self.y + self.height / 4


class StrongFly(Monster):
    def __init__(self, map_coord_data, map_height):
        super(StrongFly, self).__init__(Monster_Data['Strong Fly']['HP'], Monster_Data['Strong Fly']['MAX_HP'],
                                        Monster_Data['Strong Fly']['MP'], Monster_Data['Strong Fly']['MAX_MP'],
                                        Monster_Data['Strong Fly']['Stamina'],
                                        Monster_Data['Strong Fly']['MAX_Stamina'],
                                        Monster_Data['Strong Fly']['STR'], Monster_Data['Strong Fly']['DEF'],
                                        Monster_Data['Strong Fly']['MAG'], Monster_Data['Strong Fly']['MR'],
                                        Monster_Data['Strong Fly']['MOVE_SPEED'],
                                        Monster_Data['Strong Fly']['ATK_SPEED'],
                                        Monster_Data['Strong Fly']['Sight'], Monster_Data['Strong Fly']['Experience'],
                                        Monster_Data['Strong Fly']['AI_Type'])
        self.width = self.height = 32

        self.dir = randint(1, 9)
        if self.dir == 5:
            self.dir = 2

        self.x, self.y = map_coord_data['x'] + self.width / 2, map_height - (map_coord_data['y'] + self.height / 2)

    def set_coordinates(self, x, y):
        self.x, self.y = x, y

    def draw(self):
        if self.dir is 2:
            rssmgr.fly.image.clip_draw(self.frame * self.width, self.height * 9 + 16, self.width, self.height,
                                       self.x - self.background.window_left, self.y - self.background.window_bottom,
                                       self.width * 2, self.height * 2)
        elif self.dir is 8:
            rssmgr.fly.image.clip_draw(self.frame * self.width, self.height * 5 + 16, self.width, self.height,
                                       self.x - self.background.window_left, self.y - self.background.window_bottom,
                                       self.width * 2, self.height * 2)
        elif self.dir is 4:
            rssmgr.fly.image.clip_draw(self.frame * self.width, self.height * 7 + 16, self.width, self.height,
                                       self.x - self.background.window_left, self.y - self.background.window_bottom,
                                       self.width * 2, self.height * 2)
        elif self.dir is 6:
            rssmgr.fly.image.clip_draw((self.frame + 3) * self.width, self.height * 7 + 16, self.width, self.height,
                                       self.x - self.background.window_left, self.y - self.background.window_bottom,
                                       self.width * 2, self.height * 2)
        elif self.dir is 1:
            rssmgr.fly.image.clip_draw(self.frame * self.width, self.height * 8 + 16, self.width, self.height,
                                       self.x - self.background.window_left, self.y - self.background.window_bottom,
                                       self.width * 2, self.height * 2)
        elif self.dir is 3:
            rssmgr.fly.image.clip_draw((self.frame + 3) * self.width, self.height * 8 + 16, self.width, self.height,
                                       self.x - self.background.window_left, self.y - self.background.window_bottom,
                                       self.width * 2, self.height * 2)
        elif self.dir is 7:
            rssmgr.fly.image.clip_draw(self.frame * self.width, self.height * 6 + 16, self.width, self.height,
                                       self.x - self.background.window_left, self.y - self.background.window_bottom,
                                       self.width * 2, self.height * 2)
        elif self.dir is 9:
            rssmgr.fly.image.clip_draw((self.frame + 3) * self.width, self.height * 6 + 16, self.width, self.height,
                                       self.x - self.background.window_left, self.y - self.background.window_bottom,
                                       self.width * 2, self.height * 2)
        self.draw_hp_bar()

    def get_bb(self):
        return self.x - self.width / 2, self.y - self.height / 2, self.x + self.width / 2, self.y + self.height / 2


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
        self.dir = randint(1, 9)
        if self.dir == 5:
            self.dir = 2

        self.x, self.y = map_coord_data['x'] + self.width / 2, map_height - (map_coord_data['y'] + self.height / 2)

    def set_coordinates(self, x, y):
        self.x, self.y = x, y

    def draw(self):
        if self.dir is 2:
            rssmgr.crab.image.clip_draw(self.frame * self.width, self.height * 4, self.width, self.height,
                                        self.x - self.background.window_left, self.y - self.background.window_bottom)
        elif self.dir is 8:
            rssmgr.crab.image.clip_draw(self.frame * self.width, self.height * 0, self.width, self.height,
                                        self.x - self.background.window_left, self.y - self.background.window_bottom)
        elif self.dir is 4:
            rssmgr.crab.image.clip_draw(self.frame * self.width, self.height * 2, self.width, self.height,
                                        self.x - self.background.window_left, self.y - self.background.window_bottom)
        elif self.dir is 6:
            rssmgr.crab.image.clip_draw((self.frame + 3) * self.width, self.height * 2, self.width, self.height,
                                        self.x - self.background.window_left, self.y - self.background.window_bottom)
        elif self.dir is 1:
            rssmgr.crab.image.clip_draw(self.frame * self.width, self.height * 3, self.width, self.height,
                                        self.x - self.background.window_left, self.y - self.background.window_bottom)
        elif self.dir is 3:
            rssmgr.crab.image.clip_draw((self.frame + 3) * self.width, self.height * 3, self.width, self.height,
                                        self.x - self.background.window_left, self.y - self.background.window_bottom)
        elif self.dir is 7:
            rssmgr.crab.image.clip_draw(self.frame * self.width, self.height * 1, self.width, self.height,
                                        self.x - self.background.window_left, self.y - self.background.window_bottom)
        elif self.dir is 9:
            rssmgr.crab.image.clip_draw((self.frame + 3) * self.width, self.height * 1, self.width, self.height,
                                        self.x - self.background.window_left, self.y - self.background.window_bottom)
        self.draw_hp_bar()

    def get_bb(self):
        return self.x - self.width / 3, self.y - self.height / 3, self.x + self.width / 3, self.y + self.height / 3


class Gigant_Crab(Monster):
    global Monster_Data

    def __init__(self, map_coord_data, map_height):
        super(Gigant_Crab, self).__init__(Monster_Data['Gigant Crab']['HP'], Monster_Data['Gigant Crab']['MAX_HP'],
                                          Monster_Data['Gigant Crab']['MP'], Monster_Data['Gigant Crab']['MAX_MP'],
                                          Monster_Data['Gigant Crab']['Stamina'],
                                          Monster_Data['Gigant Crab']['MAX_Stamina'],
                                          Monster_Data['Gigant Crab']['STR'], Monster_Data['Gigant Crab']['DEF'],
                                          Monster_Data['Gigant Crab']['MAG'], Monster_Data['Gigant Crab']['MR'],
                                          Monster_Data['Gigant Crab']['MOVE_SPEED'], Monster_Data['Gigant Crab']['ATK_SPEED'],
                                          Monster_Data['Gigant Crab']['Sight'], Monster_Data['Gigant Crab']['Experience'],
                                          Monster_Data['Gigant Crab']['AI_Type'])
        self.width = self.height = 32
        self.dir = randint(1, 9)
        if self.dir == 5:
            self.dir = 2

        self.x, self.y = map_coord_data['x'] + self.width / 2, map_height - (map_coord_data['y'] + self.height / 2)

    def set_coordinates(self, x, y):
        self.x, self.y = x, y

    def draw(self):
        if self.dir is 2:
            rssmgr.crab.image.clip_draw(self.frame * self.width, self.height * 4, self.width, self.height,
                                        self.x - self.background.window_left, self.y - self.background.window_bottom,
                                        self.width * 2, self.height * 2)
        elif self.dir is 8:
            rssmgr.crab.image.clip_draw(self.frame * self.width, self.height * 0, self.width, self.height,
                                        self.x - self.background.window_left, self.y - self.background.window_bottom,
                                        self.width * 2, self.height * 2)
        elif self.dir is 4:
            rssmgr.crab.image.clip_draw(self.frame * self.width, self.height * 2, self.width, self.height,
                                        self.x - self.background.window_left, self.y - self.background.window_bottom,
                                        self.width * 2, self.height * 2)
        elif self.dir is 6:
            rssmgr.crab.image.clip_draw((self.frame + 3) * self.width, self.height * 2, self.width, self.height,
                                        self.x - self.background.window_left, self.y - self.background.window_bottom,
                                        self.width * 2, self.height * 2)
        elif self.dir is 1:
            rssmgr.crab.image.clip_draw(self.frame * self.width, self.height * 3, self.width, self.height,
                                        self.x - self.background.window_left, self.y - self.background.window_bottom,
                                        self.width * 2, self.height * 2)
        elif self.dir is 3:
            rssmgr.crab.image.clip_draw((self.frame + 3) * self.width, self.height * 3, self.width, self.height,
                                        self.x - self.background.window_left, self.y - self.background.window_bottom,
                                        self.width * 2, self.height * 2)
        elif self.dir is 7:
            rssmgr.crab.image.clip_draw(self.frame * self.width, self.height * 1, self.width, self.height,
                                        self.x - self.background.window_left, self.y - self.background.window_bottom,
                                        self.width * 2, self.height * 2)
        elif self.dir is 9:
            rssmgr.crab.image.clip_draw((self.frame + 3) * self.width, self.height * 1, self.width, self.height,
                                        self.x - self.background.window_left, self.y - self.background.window_bottom,
                                        self.width * 2, self.height * 2)
        self.draw_hp_bar()

    def get_bb(self):
        return self.x - self.width * 2 / 3, \
               self.y - self.height * 2/ 3, \
               self.x + self.width * 2 / 3, \
               self.y + self.height * 2 / 3


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
        self.dir = randint(1, 9)
        if self.dir == 5:
            self.dir = 2

        self.x, self.y = map_coord_data['x'] + self.width / 2, map_height - (map_coord_data['y'] + self.height / 2)

    def set_coordinates(self, x, y):
        self.x, self.y = x, y

    def draw(self):
        if self.dir is 2:
            rssmgr.skull_golem.image.clip_draw(self.frame * self.width, self.height * 4, self.width, self.height,
                                               self.x - self.background.window_left, self.y - self.background.window_bottom,
                                               self.width * 2, self.height * 2)
        elif self.dir is 8:
            rssmgr.skull_golem.image.clip_draw(self.frame * self.width, self.height * 0, self.width, self.height,
                                               self.x - self.background.window_left, self.y - self.background.window_bottom,
                                               self.width * 2, self.height * 2)
        elif self.dir is 4:
            rssmgr.skull_golem.image.clip_draw(self.frame * self.width, self.height * 2, self.width, self.height,
                                               self.x - self.background.window_left, self.y - self.background.window_bottom,
                                               self.width * 2, self.height * 2)
        elif self.dir is 6:
            rssmgr.skull_golem.image.clip_draw((self.frame + 3) * self.width, self.height * 2, self.width, self.height,
                                               self.x - self.background.window_left, self.y - self.background.window_bottom,
                                               self.width * 2, self.height * 2)
        elif self.dir is 1:
            rssmgr.skull_golem.image.clip_draw(self.frame * self.width, self.height * 3, self.width, self.height,
                                               self.x - self.background.window_left, self.y - self.background.window_bottom,
                                               self.width * 2, self.height * 2)
        elif self.dir is 3:
            rssmgr.skull_golem.image.clip_draw((self.frame + 3) * self.width, self.height * 3, self.width, self.height,
                                               self.x - self.background.window_left, self.y - self.background.window_bottom,
                                               self.width * 2, self.height * 2)
        elif self.dir is 7:
            rssmgr.skull_golem.image.clip_draw(self.frame * self.width, self.height * 1, self.width, self.height,
                                               self.x - self.background.window_left, self.y - self.background.window_bottom,
                                               self.width * 2, self.height * 2)
        elif self.dir is 9:
            rssmgr.skull_golem.image.clip_draw((self.frame + 3) * self.width, self.height * 1, self.width, self.height,
                                               self.x - self.background.window_left, self.y - self.background.window_bottom,
                                               self.width * 2, self.height * 2)
        self.draw_hp_bar()

    def get_bb(self):
        return self.x - self.width, self.y - self.height, self.x + self.width, self.y + self.height


class Mini_Skull_Golem(Monster):
    global Monster_Data

    def __init__(self, map_coord_data, map_height):
        super(Mini_Skull_Golem, self).__init__(Monster_Data['Mini Skull Golem']['HP'],
                                               Monster_Data['Mini Skull Golem']['MAX_HP'],
                                               Monster_Data['Mini Skull Golem']['MP'],
                                               Monster_Data['Mini Skull Golem']['MAX_MP'],
                                               Monster_Data['Mini Skull Golem']['Stamina'],
                                               Monster_Data['Mini Skull Golem']['MAX_Stamina'],
                                               Monster_Data['Mini Skull Golem']['STR'],
                                               Monster_Data['Mini Skull Golem']['DEF'],
                                               Monster_Data['Mini Skull Golem']['MAG'],
                                               Monster_Data['Mini Skull Golem']['MR'],
                                               Monster_Data['Mini Skull Golem']['MOVE_SPEED'],
                                               Monster_Data['Mini Skull Golem']['ATK_SPEED'],
                                               Monster_Data['Mini Skull Golem']['Sight'],
                                               Monster_Data['Mini Skull Golem']['Experience'],
                                               Monster_Data['Mini Skull Golem']['AI_Type'])
        self.width = self.height = 32
        self.dir = randint(1, 9)
        if self.dir == 5:
            self.dir = 2

        self.x, self.y = map_coord_data['x'] + self.width / 2, map_height - (map_coord_data['y'] + self.height / 2)

    def set_coordinates(self, x, y):
        self.x, self.y = x, y

    def draw(self):
        if self.dir is 2:
            rssmgr.skull_golem.image.clip_draw(self.frame * self.width, self.height * 4, self.width, self.height,
                                               self.x - self.background.window_left,
                                               self.y - self.background.window_bottom)
        elif self.dir is 8:
            rssmgr.skull_golem.image.clip_draw(self.frame * self.width, self.height * 0, self.width, self.height,
                                               self.x - self.background.window_left,
                                               self.y - self.background.window_bottom)
        elif self.dir is 4:
            rssmgr.skull_golem.image.clip_draw(self.frame * self.width, self.height * 2, self.width, self.height,
                                               self.x - self.background.window_left,
                                               self.y - self.background.window_bottom)
        elif self.dir is 6:
            rssmgr.skull_golem.image.clip_draw((self.frame + 3) * self.width, self.height * 2, self.width, self.height,
                                               self.x - self.background.window_left,
                                               self.y - self.background.window_bottom)
        elif self.dir is 1:
            rssmgr.skull_golem.image.clip_draw(self.frame * self.width, self.height * 3, self.width, self.height,
                                               self.x - self.background.window_left,
                                               self.y - self.background.window_bottom)
        elif self.dir is 3:
            rssmgr.skull_golem.image.clip_draw((self.frame + 3) * self.width, self.height * 3, self.width, self.height,
                                               self.x - self.background.window_left,
                                               self.y - self.background.window_bottom)
        elif self.dir is 7:
            rssmgr.skull_golem.image.clip_draw(self.frame * self.width, self.height * 1, self.width, self.height,
                                               self.x - self.background.window_left,
                                               self.y - self.background.window_bottom)
        elif self.dir is 9:
            rssmgr.skull_golem.image.clip_draw((self.frame + 3) * self.width, self.height * 1, self.width, self.height,
                                               self.x - self.background.window_left,
                                               self.y - self.background.window_bottom)
        self.draw_hp_bar()

    def get_bb(self):
        return self.x - self.width / 2, self.y - self.height / 2, self.x + self.width / 2, self.y + self.height / 2


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

        self.dir = randint(1, 9)
        if self.dir == 5:
            self.dir = 2

        self.x, self.y = map_coord_data['x'] + self.width / 2, map_height - (map_coord_data['y'] + self.height / 2)

    def set_coordinates(self, x, y):
        self.x, self.y = x, y

    def draw(self):
        if self.dir is 2:
            rssmgr.spear.image.clip_draw(self.frame * self.width, self.height * 4, self.width, self.height,
                                         self.x - self.background.window_left, self.y - self.background.window_bottom)
        elif self.dir is 8:
            rssmgr.spear.image.clip_draw(self.frame * self.width, self.height * 0, self.width, self.height,
                                         self.x - self.background.window_left, self.y - self.background.window_bottom)
        elif self.dir is 4:
            rssmgr.spear.image.clip_draw(self.frame * self.width, self.height * 2, self.width, self.height,
                                         self.x - self.background.window_left, self.y - self.background.window_bottom)
        elif self.dir is 6:
            rssmgr.spear.image.clip_draw((self.frame + 3) * self.width, self.height * 2, self.width, self.height,
                                         self.x - self.background.window_left, self.y - self.background.window_bottom)
        elif self.dir is 1:
            rssmgr.spear.image.clip_draw(self.frame * self.width, self.height * 3, self.width, self.height,
                                         self.x - self.background.window_left, self.y - self.background.window_bottom)
        elif self.dir is 3:
            rssmgr.spear.image.clip_draw((self.frame + 3) * self.width, self.height * 3, self.width, self.height,
                                         self.x - self.background.window_left, self.y - self.background.window_bottom)
        elif self.dir is 7:
            rssmgr.spear.image.clip_draw(self.frame * self.width, self.height * 1, self.width, self.height,
                                         self.x - self.background.window_left, self.y - self.background.window_bottom)
        elif self.dir is 9:
            rssmgr.spear.image.clip_draw((self.frame + 3) * self.width, self.height * 1, self.width, self.height,
                                         self.x - self.background.window_left, self.y - self.background.window_bottom)
        self.draw_hp_bar()

    def get_bb(self):
        return self.x - self.width / 2, self.y - self.height / 2, self.x + self.width / 2, self.y + self.height / 2


class FlyingSpear(Monster):
    global Monster_Data

    def __init__(self, map_coord_data, map_height):
        super(FlyingSpear, self).__init__(Monster_Data['Flying Spear']['HP'], Monster_Data['Flying Spear']['MAX_HP'],
                                          Monster_Data['Flying Spear']['MP'], Monster_Data['Flying Spear']['MAX_MP'],
                                          Monster_Data['Flying Spear']['Stamina'],
                                          Monster_Data['Flying Spear']['MAX_Stamina'],
                                          Monster_Data['Flying Spear']['STR'], Monster_Data['Flying Spear']['DEF'],
                                          Monster_Data['Flying Spear']['MAG'], Monster_Data['Flying Spear']['MR'],
                                          Monster_Data['Flying Spear']['MOVE_SPEED'],
                                          Monster_Data['Flying Spear']['ATK_SPEED'],
                                          Monster_Data['Flying Spear']['Sight'],
                                          Monster_Data['Flying Spear']['Experience'],
                                          Monster_Data['Flying Spear']['AI_Type'])
        self.width = self.height = 64

        self.dir = randint(1, 9)
        if self.dir == 5:
            self.dir = 2

        self.x, self.y = map_coord_data['x'] + self.width / 2, map_height - (map_coord_data['y'] + self.height / 2)
        self.max_move_frame = 2
        self.fly_available = True

    def set_coordinates(self, x, y):
        self.x, self.y = x, y

    def draw(self):
        if self.dir is 2:
            rssmgr.spear.image.clip_draw((self.frame + 2) * self.width, self.height * 12 + 48, self.width, self.height,
                                         self.x - self.background.window_left, self.y - self.background.window_bottom)
        elif self.dir is 8:
            rssmgr.spear.image.clip_draw((self.frame + 2) * self.width, self.height * 8, self.width, self.height,
                                         self.x - self.background.window_left, self.y - self.background.window_bottom)
        elif self.dir is 4:
            rssmgr.spear.image.clip_draw((self.frame + 2) * self.width, self.height * 10 + 16, self.width, self.height,
                                         self.x - self.background.window_left, self.y - self.background.window_bottom)
        elif self.dir is 6:
            rssmgr.spear.image.clip_draw((self.frame + 4) * self.width, self.height * 10 + 16, self.width, self.height,
                                         self.x - self.background.window_left, self.y - self.background.window_bottom)
        elif self.dir is 1:
            rssmgr.spear.image.clip_draw((self.frame + 2) * self.width, self.height * 11 + 32, self.width, self.height,
                                         self.x - self.background.window_left, self.y - self.background.window_bottom)
        elif self.dir is 3:
            rssmgr.spear.image.clip_draw((self.frame + 4) * self.width, self.height * 11 + 32, self.width, self.height,
                                         self.x - self.background.window_left, self.y - self.background.window_bottom)
        elif self.dir is 7:
            rssmgr.spear.image.clip_draw((self.frame + 2) * self.width, self.height * 9, self.width, self.height,
                                         self.x - self.background.window_left, self.y - self.background.window_bottom)
        elif self.dir is 9:
            rssmgr.spear.image.clip_draw((self.frame + 4) * self.width, self.height * 9, self.width, self.height,
                                         self.x - self.background.window_left, self.y - self.background.window_bottom)
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

        self.dir = randint(1, 9)
        if self.dir == 5:
            self.dir = 2

        self.x, self.y = map_coord_data['x'] + self.width / 2, map_height - (map_coord_data['y'] + self.height / 2)

    def set_coordinates(self, x, y):
        self.x, self.y = x, y

    def draw(self):
        if self.dir is 2:
            rssmgr.slasher.image.clip_draw(self.frame * self.width, self.height * 4, self.width, self.height,
                                           self.x - self.background.window_left, self.y - self.background.window_bottom,
                                           self.width * 2, self.height * 2)
        elif self.dir is 8:
            rssmgr.slasher.image.clip_draw(self.frame * self.width, self.height * 0, self.width, self.height,
                                           self.x - self.background.window_left, self.y - self.background.window_bottom,
                                           self.width * 2, self.height * 2)
        elif self.dir is 4:
            rssmgr.slasher.image.clip_draw(self.frame * self.width, self.height * 2, self.width, self.height,
                                           self.x - self.background.window_left, self.y - self.background.window_bottom,
                                           self.width * 2, self.height * 2)
        elif self.dir is 6:
            rssmgr.slasher.image.clip_draw((self.frame + 3) * self.width, self.height * 2, self.width, self.height,
                                           self.x - self.background.window_left, self.y - self.background.window_bottom,
                                           self.width * 2, self.height * 2)
        elif self.dir is 1:
            rssmgr.slasher.image.clip_draw(self.frame * self.width, self.height * 3, self.width, self.height,
                                           self.x - self.background.window_left, self.y - self.background.window_bottom,
                                           self.width * 2, self.height * 2)
        elif self.dir is 3:
            rssmgr.slasher.image.clip_draw((self.frame + 3) * self.width, self.height * 3, self.width, self.height,
                                           self.x - self.background.window_left, self.y - self.background.window_bottom,
                                           self.width * 2, self.height * 2)
        elif self.dir is 7:
            rssmgr.slasher.image.clip_draw(self.frame * self.width, self.height * 1, self.width, self.height,
                                           self.x - self.background.window_left, self.y - self.background.window_bottom,
                                           self.width * 2, self.height * 2)
        elif self.dir is 9:
            rssmgr.slasher.image.clip_draw((self.frame + 3) * self.width, self.height * 1, self.width, self.height,
                                           self.x - self.background.window_left, self.y - self.background.window_bottom,
                                           self.width * 2, self.height * 2)
        self.draw_hp_bar()

    def get_bb(self):
        return self.x - self.width, self.y - self.height, self.x + self.width, self.y + self.height


class GigantSlasher(Monster):
    global Monster_Data

    def __init__(self, map_coord_data, map_height):
        super(GigantSlasher, self).__init__(Monster_Data['Gigant Slasher']['HP'],
                                            Monster_Data['Gigant Slasher']['MAX_HP'],
                                            Monster_Data['Gigant Slasher']['MP'],
                                            Monster_Data['Gigant Slasher']['MAX_MP'],
                                            Monster_Data['Gigant Slasher']['Stamina'],
                                            Monster_Data['Gigant Slasher']['MAX_Stamina'],
                                            Monster_Data['Gigant Slasher']['STR'],
                                            Monster_Data['Gigant Slasher']['DEF'],
                                            Monster_Data['Gigant Slasher']['MAG'],
                                            Monster_Data['Gigant Slasher']['MR'],
                                            Monster_Data['Gigant Slasher']['MOVE_SPEED'],
                                            Monster_Data['Gigant Slasher']['ATK_SPEED'],
                                            Monster_Data['Gigant Slasher']['Sight'],
                                            Monster_Data['Gigant Slasher']['Experience'],
                                            Monster_Data['Gigant Slasher']['AI_Type'])
        self.width = self.height = 32

        self.dir = randint(1, 9)
        if self.dir == 5:
            self.dir = 2

        self.x, self.y = map_coord_data['x'] + self.width / 2, map_height - (map_coord_data['y'] + self.height / 2)

    def set_coordinates(self, x, y):
        self.x, self.y = x, y

    def draw(self):
        if self.dir is 2:
            rssmgr.slasher.image.clip_draw(self.frame * self.width, self.height * 4, self.width, self.height,
                                           self.x - self.background.window_left, self.y - self.background.window_bottom,
                                           self.width * 4, self.height * 4)
        elif self.dir is 8:
            rssmgr.slasher.image.clip_draw(self.frame * self.width, self.height * 0, self.width, self.height,
                                           self.x - self.background.window_left, self.y - self.background.window_bottom,
                                           self.width * 4, self.height * 4)
        elif self.dir is 4:
            rssmgr.slasher.image.clip_draw(self.frame * self.width, self.height * 2, self.width, self.height,
                                           self.x - self.background.window_left, self.y - self.background.window_bottom,
                                           self.width * 4, self.height * 4)
        elif self.dir is 6:
            rssmgr.slasher.image.clip_draw((self.frame + 3) * self.width, self.height * 2, self.width, self.height,
                                           self.x - self.background.window_left, self.y - self.background.window_bottom,
                                           self.width * 4, self.height * 4)
        elif self.dir is 1:
            rssmgr.slasher.image.clip_draw(self.frame * self.width, self.height * 3, self.width, self.height,
                                           self.x - self.background.window_left, self.y - self.background.window_bottom,
                                           self.width * 4, self.height * 4)
        elif self.dir is 3:
            rssmgr.slasher.image.clip_draw((self.frame + 3) * self.width, self.height * 3, self.width, self.height,
                                           self.x - self.background.window_left, self.y - self.background.window_bottom,
                                           self.width * 4, self.height * 4)
        elif self.dir is 7:
            rssmgr.slasher.image.clip_draw(self.frame * self.width, self.height * 1, self.width, self.height,
                                           self.x - self.background.window_left, self.y - self.background.window_bottom,
                                           self.width * 4, self.height * 4)
        elif self.dir is 9:
            rssmgr.slasher.image.clip_draw((self.frame + 3) * self.width, self.height * 1, self.width, self.height,
                                           self.x - self.background.window_left, self.y - self.background.window_bottom,
                                           self.width * 4, self.height * 4)
        self.draw_hp_bar()

    def get_bb(self):
        return self.x - (self.width * 2), self.y - (self.height * 2), \
               self.x + (self.width * 2), self.y + (self.height * 2)


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
