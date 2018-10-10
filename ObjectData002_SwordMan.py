from ObjectData001_BasePlayer import *
from ObjectData005_Skill import *
import math
import json


SwordMan_data_file = open('UnitData\\Player.json', 'r')
SwordMan_Data = json.load(SwordMan_data_file)
SwordMan_data_file.close()


class SwordMan(Player):

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

        # 스킬
        self.Typhoon_Slash = None

        if self.Typhoon_Slash is None:
            self.Typhoon_Slash = TyphoonAttack()
            self.Typhoon_Slash.ATK_SPEED = self.ATK_SPEED

        self.Air_split = None
        if self.Air_split is None:
            self.Air_split = AirSplit()
            self.Air_split.MOVE_SPEED = self.MOVE_SPEED

        self.skill_image = None
        if self.skill_image is None:
            self.skill_image = load_image("Resource_Image\\Effects_000.png")

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

    def set_background(self, background):
        super(SwordMan, self).set_background(background)
        self.Typhoon_Slash.set_background(background)
        self.Air_split.set_background(background)

    def update(self, frame_time, others):
        super(SwordMan, self).update(frame_time, others)

        # 회전베기
        if self.state == SKILL_ATTACK_1 and self.Typhoon_Slash.Level > 0:
            self.Typhoon_Slash.x, self.Typhoon_Slash.y = self.x, self.y
            if self.Typhoon_Slash.frame == 0:
                self.Typhoon_Slash.attack_motion = self.dir
            self.Typhoon_Slash.update(frame_time, others)
            if self.Typhoon_Slash.frame >= 8:
                self.Typhoon_Slash.frame = 0
                self.state = STAND

        # 바람 쪼개기
        if self.state == SKILL_ATTACK_2 and self.Air_split.Level > 0:
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
                if self.Air_split.flag is False:
                    if self.MP >= self.Air_split.use_mp and self.STAMINA >= self.Air_split.use_sp:
                        self.MP -= self.Air_split.use_mp
                        self.STAMINA -= self.Air_split.use_sp
                        self.Air_split.flag = True
                        self.Air_split.x, self.Air_split.y = self.x, self.y
                    self.Air_split.start_dir = self.dir
                if self.distance > 0:
                    self.Air_split.distance = self.distance
        self.Air_split.update(frame_time, others)

    def draw(self):
        super(SwordMan, self).draw()
        if self.state == SKILL_ATTACK_1:
            if self.Typhoon_Slash.attack_motion == 2:
                self.image.clip_draw(self.width * 2, self.height * 3, self.width * 2, self.height,
                                     self.x - self.background.window_left, self.y - self.background.window_bottom)
            elif self.Typhoon_Slash.attack_motion == 8:
                self.image.clip_draw(self.width * 4, self.height * 3, self.width * 2, self.height,
                                     self.x - self.background.window_left, self.y - self.background.window_bottom)
            elif self.Typhoon_Slash.attack_motion == 4:
                self.image.clip_draw(self.width * 4, self.height * 1, self.width * 2, self.height,
                                     self.x - self.width / 2 - self.background.window_left,
                                     self.y - self.background.window_bottom)
            elif self.Typhoon_Slash.attack_motion == 6:
                self.image.clip_draw(self.width * 2, self.height * 1, self.width * 2, self.height,
                                     self.x - self.background.window_left + self.width / 2,
                                     self.y - self.background.window_bottom)
            elif self.Typhoon_Slash.attack_motion == 1:
                self.image.clip_draw(self.width * 4, self.height * 0, self.width * 2, self.height,
                                     self.x - self.background.window_left - 7,
                                     self.y - self.background.window_bottom)
            elif self.Typhoon_Slash.attack_motion == 3:
                self.image.clip_draw(self.width * 2, self.height * 2, self.width * 2, self.height,
                                     self.x - self.background.window_left,
                                     self.y - self.background.window_bottom)
            elif self.Typhoon_Slash.attack_motion == 7:
                self.image.clip_draw(self.width * 4, self.height * 2, self.width * 2, self.height,
                                     self.x - self.background.window_left,
                                     self.y - self.background.window_bottom)
            elif self.Typhoon_Slash.attack_motion == 9:
                self.image.clip_draw(self.width * 2, self.height * 0, self.width * 2, self.height,
                                     self.x - self.background.window_left + 11,
                                     self.y - self.background.window_bottom)

            if self.box_draw_Trigger is True:
                self.Typhoon_Slash.draw_hb()

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
        if self.Air_split.flag is True:
            self.Air_split.draw()
            if self.box_draw_Trigger is True:
                self.Air_split.draw_hb()

    def handle_events(self, event):
        super(SwordMan, self).handle_events(event)
        if self.state == STAND or self.state == WALK:
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_a):
                if self.Typhoon_Slash.Level > 0 and \
                                self.MP >= self.Typhoon_Slash.use_mp and self.STAMINA >= self.Typhoon_Slash.use_sp:
                    self.MP -= self.Typhoon_Slash.use_mp
                    self.STAMINA -= self.Typhoon_Slash.use_sp
                    self.state = SKILL_ATTACK_1
            elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_s):
                if self.Air_split.Level > 0:
                    self.state = SKILL_ATTACK_2

    def level_up(self):
        super(SwordMan, self).level_up()
        self.skill_image.clip_draw(96, 9, 32, 32, self.x, self.y + self.height * 2)
        self.MAX_HP += 3
        self.MAX_MP += 1
        self.MAX_STAMINA += 2
        if self.LEVEL % 3 == 2:
            self.HpPotion.number += 1
        elif self.LEVEL % 3 == 0:
            self.MpPotion.number += 1
        elif self.LEVEL % 3 == 1:
            self.StaminaPotion.number += 1

    def air_splitter_collide(self, enemy):
        left_a, bottom_a, right_a, top_a = self.Air_split.get_hb()
        left_b, bottom_b, right_b, top_b = enemy.get_bb()
        if left_a > right_b:
            return False
        if right_a < left_b:
            return False
        if top_a < bottom_b:
            return False
        if bottom_a > top_b:
            return False
        if self.Air_split.flag is True:
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
        return False
