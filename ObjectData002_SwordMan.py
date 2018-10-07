from ObjectData001_BasePlayer import *
import math
import json


SwordMan_data_file = open('UnitData\\Player.json', 'r')
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
        self.class_num = 2
        self.image = load_image("Resource_Image\\Player001_SwordMan.png")
        self.x = x
        self.y = y
        self.HpPotion.number += 2
        self.StaminaPotion.number += 1

        # 스킬레벨 변수
        self.typhoon_slash_level = 0
        self.air_splitter_level = 1

        self.skill_image = None
        if self.skill_image is None:
            self.skill_image = load_image("Resource_Image\\Effects_000.png")

        # 바람 가르기 스킬용 변수
        self.old_dir = 0
        self.air_splitter_flag = False
        self.air_splitter_frame = 0
        self.air_splitter_frame_time = 0
        self.air_splitter_x, self.air_splitter_y = 0, 0
        self.air_splitter_rad = 0.0
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

        # 바람 쪼개기
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
                if self.air_splitter_flag is False:
                    if self.MP >= self.air_splitter_mp and self.STAMINA >= self.air_splitter_sp:
                        self.MP -= self.air_splitter_mp
                        self.STAMINA -= self.air_splitter_sp
                        self.air_splitter_flag = True
                        self.air_splitter_x, self.air_splitter_y = self.x, self.y
                        self.air_splitter_size = self.air_splitter_level * 2 + 32
                    self.old_dir = self.dir
        if self.air_splitter_flag is True:
            air_splitter_time_limit = 2.5
            self.air_splitter_frame_time += ((1.0 / self.air_splitter_level) *
                                             self.FRAMES_PER_ACTION_atk * self.ACTION_PER_TIME_atk * frame_time)
            if self.air_splitter_frame_time > (self.air_splitter_frame + 1) * air_splitter_time_limit / 4.0:
                self.air_splitter_frame += 1
            if self.old_dir is 2:
                self.air_splitter_rad = 3 * math.pi / 2.0
                self.air_splitter_y -= (self.distance * 8)
            elif self.old_dir is 8:
                self.air_splitter_rad = math.pi / 2.0
                self.air_splitter_y += (self.distance * 8)
            elif self.old_dir is 4:
                self.air_splitter_rad = math.pi
                self.air_splitter_x -= (self.distance * 8)
            elif self.old_dir is 6:
                self.air_splitter_rad = 0.0
                self.air_splitter_x += (self.distance * 8)
            elif self.old_dir is 1:
                self.air_splitter_rad = 5 * math.pi / 4.0
                self.air_splitter_x -= (self.distance * 8)
                self.air_splitter_y -= (self.distance * 8)
            elif self.old_dir is 3:
                self.air_splitter_rad = 7 * math.pi / 4.0
                self.air_splitter_x += (self.distance * 8)
                self.air_splitter_y -= (self.distance * 8)
            elif self.old_dir is 7:
                self.air_splitter_rad = 3 * math.pi / 4.0
                self.air_splitter_x -= (self.distance * 8)
                self.air_splitter_y += (self.distance * 8)
            elif self.old_dir is 9:
                self.air_splitter_rad = 1 * math.pi / 4.0
                self.air_splitter_x += (self.distance * 8)
                self.air_splitter_y += (self.distance * 8)
            if self.air_splitter_frame_time > air_splitter_time_limit:
                self.air_splitter_x, self.air_splitter_y = -100, -100
                self.air_splitter_frame_time = 0
                self.air_splitter_frame = 0
                self.air_splitter_flag = False

    def draw(self):
        super(SwordMan, self).draw()
        if self.state == SKILL_ATTACK_2:
            if self.dir is 2:
                if self.box_draw_Trigger:
                    self.draw_hbs(self.x, self.melee_atk_point_DownY - self.height / 4, self.attack_size)
                if self.attack_motion is 0:
                    self.image.clip_draw(self.width * 2, self.height * 3, self.width * 2, self.height,
                                         self.x - self.background.window_left, self.y - self.background.window_bottom)
                elif self.attack_motion is 1:
                    self.image.clip_draw(self.width * 6, self.height * 7, self.width * 2, self.height,
                                         self.x - self.background.window_left, self.y - self.background.window_bottom)
            elif self.dir is 8:
                if self.box_draw_Trigger:
                    self.draw_hbs(self.x, self.melee_atk_point_UpY + self.height / 4, self.attack_size)
                if self.attack_motion is 0:
                    self.image.clip_draw(self.width * 4, self.height * 3, self.width * 2, self.height,
                                         self.x - self.background.window_left, self.y - self.background.window_bottom)
                elif self.attack_motion is 1:
                    self.image.clip_draw(self.width * 6, self.height * 6, self.width * 2, self.height,
                                         self.x - self.background.window_left, self.y - self.background.window_bottom)
            elif self.dir is 4:
                if self.box_draw_Trigger:
                    self.draw_hbs(self.melee_atk_point_LeftX - self.width / 2, self.y, self.attack_size)
                if self.attack_motion is 0:
                    self.image.clip_draw(self.width * 4, self.height * 1, self.width * 2, self.height,
                                         self.x - self.width / 2 - self.background.window_left,
                                         self.y - self.background.window_bottom)
                elif self.attack_motion is 1:
                    self.image.clip_draw(self.width * 6, self.height * 5, self.width * 2, self.height,
                                         self.x - self.width / 2 - self.background.window_left,
                                         self.y - self.background.window_bottom)
            elif self.dir is 6:
                if self.box_draw_Trigger:
                    self.draw_hbs(self.melee_atk_point_RightX + self.width / 2, self.y, self.attack_size)
                if self.attack_motion is 0:
                    self.image.clip_draw(self.width * 2, self.height * 1, self.width * 2, self.height,
                                         self.x - self.background.window_left + self.width / 2,
                                         self.y - self.background.window_bottom)
                elif self.attack_motion is 1:
                    self.image.clip_draw(self.width * 6, self.height * 4, self.width * 2, self.height,
                                         self.x - self.background.window_left + self.width / 2,
                                         self.y - self.background.window_bottom)
            # 대각선 이미지인 경우 프레임 위치 조정
            elif self.dir is 1:
                if self.box_draw_Trigger:
                    self.draw_hbs(self.melee_atk_point_LeftX, self.melee_atk_point_DownY, self.attack_size)
                if self.attack_motion is 0:
                    self.image.clip_draw(self.width * 4, self.height * 0, self.width * 2, self.height,
                                         self.x - self.background.window_left - 7,
                                         self.y - self.background.window_bottom)
                elif self.attack_motion is 1:
                    self.image.clip_draw(self.width * 0, self.height * 3, self.width * 2, self.height,
                                         self.x - self.background.window_left,
                                         self.y - self.background.window_bottom)
            elif self.dir is 3:
                if self.box_draw_Trigger:
                    self.draw_hbs(self.melee_atk_point_RightX, self.melee_atk_point_DownY, self.attack_size)
                if self.attack_motion is 0:
                    self.image.clip_draw(self.width * 2, self.height * 2, self.width * 2, self.height,
                                         self.x - self.background.window_left,
                                         self.y - self.background.window_bottom)
                elif self.attack_motion is 1:
                    self.image.clip_draw(self.width * 0, self.height * 2, self.width * 2, self.height,
                                         self.x - self.background.window_left,
                                         self.y - self.background.window_bottom)
            elif self.dir is 7:
                if self.box_draw_Trigger:
                    self.draw_hbs(self.melee_atk_point_LeftX, self.melee_atk_point_UpY, self.attack_size)
                if self.attack_motion is 0:
                    self.image.clip_draw(self.width * 4, self.height * 2, self.width * 2, self.height,
                                         self.x - self.background.window_left,
                                         self.y - self.background.window_bottom)
                elif self.attack_motion is 1:
                    self.image.clip_draw(self.width * 0, self.height * 1, self.width * 2, self.height,
                                         self.x - self.background.window_left,
                                         self.y - self.background.window_bottom)
            elif self.dir is 9:
                if self.box_draw_Trigger:
                    self.draw_hbs(self.melee_atk_point_RightX, self.melee_atk_point_UpY, self.attack_size)
                if self.attack_motion is 0:
                    self.image.clip_draw(self.width * 2, self.height * 0, self.width * 2, self.height,
                                         self.x - self.background.window_left + 11,
                                         self.y - self.background.window_bottom)
                elif self.attack_motion is 1:
                    self.image.clip_draw(self.width * 0, self.height * 0, self.width * 2, self.height,
                                         self.x - self.background.window_left + 2,
                                         self.y - self.background.window_bottom)
        if self.air_splitter_flag is True:
            self.draw_air_splitter_effects()
            if self.box_draw_Trigger is True:
                self.draw_air_splitter_hb()

    def handle_events(self, event):
        super(SwordMan, self).handle_events(event)
        if self.state != MELEE_ATTACK:
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_a):
                self.state = SKILL_ATTACK_1
            elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_s):
                self.state = SKILL_ATTACK_2

    def draw_air_splitter_effects(self):
        self.skill_image.clip_composite_draw((self.air_splitter_frame + 2) * self.width, 14 * self.width, 32, 32,
                                             self.air_splitter_rad, 'v',
                                             self.air_splitter_x - self.background.window_left,
                                             self.air_splitter_y - self.background.window_bottom,
                                             self.air_splitter_size, self.air_splitter_size)

    def air_splitter_hb(self):
        return self.air_splitter_x - self.air_splitter_size / 2, self.air_splitter_y - self.air_splitter_size / 2, \
               self.air_splitter_x + self.air_splitter_size / 2, self.air_splitter_y + self.air_splitter_size / 2

    def draw_air_splitter_hb(self):
        draw_rectangle(self.air_splitter_hb()[0] - self.background.window_left,
                       self.air_splitter_hb()[1] - self.background.window_bottom,
                       self.air_splitter_hb()[2] - self.background.window_left,
                       self.air_splitter_hb()[3] - self.background.window_bottom)

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
        if self.air_splitter_flag is True:
            return True

    def melee_atk_collide(self, enemy):
        left_a, bottom_a, right_a, top_a = self.get_melee_atk_hb()
        left_b, bottom_b, right_b, top_b = enemy.get_bb()
        if left_a > right_b:
            return False
        if right_a < left_b:
            return False
        if top_a < bottom_b:
            return False
        if bottom_a > top_b:
            return False
        if self.state is MELEE_ATTACK or self.state is SKILL_ATTACK_2:
            return True
