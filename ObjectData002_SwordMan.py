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

        # 스킬레벨 변수
        self.typhoon_slash_level = 0
        self.air_splitter_level = 0

        # 바람 가르기 스킬용 변수
        self.air_splitter_x, air_splitter_y = 0, 0
        self.air_splitter_size = 0
        self.air_splitter_mp = 3
        self.air_splitter_sp = 1

        # 소드맨의 효과음
        if self.attack_sound is None:
            self.attack_sound = load_wav('Resource_Sound\\Effect_Sound\\Slash12.wav')
            self.attack_sound.set_volume(64)
        if self.hit_sound is None:
            self.hit_sound = load_wav('Resource_Sound\\Effect_Sound\\Damage2.wav')
            self.hit_sound.set_volume(64)

    def show_stat(self):
        super(SwordMan, self).show_stat()
        print('\n')

    def update(self, frame_time, others):
        super(SwordMan, self).update(frame_time, others)
        if self.state == SKILL_ATTACK_2:
            # 공격범위 변수
            self.melee_atk_point_LeftX = self.x - self.width / 2
            self.melee_atk_point_DownY = self.y - self.height / 4
            self.melee_atk_point_RightX = self.x + self.width / 2
            self.melee_atk_point_UpY = self.y + self.height / 4
            self.total_frames_atk += self.FRAMES_PER_ACTION_atk * self.ACTION_PER_TIME_atk * frame_time
            self.attack_motion = int(self.total_frames_atk) % 3
            if self.attack_motion > 1:
                if self.attack_sound is not None:
                    self.attack_sound.play()
                self.attack_motion = 0
                self.state = STAND
                self.total_frames_atk = 0.0



    def handle_events(self, event):
        super(SwordMan, self).handle_events(event)
        print(self.x, self.y)
        if (event.type, event.key) == (SDL_KEYDOWN, SDLK_a):
            self.state = SKILL_ATTACK_1
        if (event.type, event.key) == (SDL_KEYDOWN, SDLK_s):
            if self.MP >= self.air_splitter_mp and self.STAMINA >= self.air_splitter_sp:
                self.MP -= self.air_splitter_mp
                self.STAMINA -= self.air_splitter_sp
                self.state = SKILL_ATTACK_2


    def draw_air_splitter_effects(self):


    def air_splitter_hb(self):


    def air_splitter_collide(self, enemy):
        left_a, bottom_a, right_a, top_a = self.air_splitter_hb()
        left_b, bottom_b, right_b, top_b = enemy.get_bb()
        if left_a > right_b:
            return False
        if right_a < left_b:
            return False
        if top_a < bottom_b:
            return False
        if bottom_a > top_b:
            return False
        if self.state is MELEE_ATTACK:
            return True


