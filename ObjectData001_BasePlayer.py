from pico2d import *
from ObjectData000_BaseObject_BaseUnit import *
from ObjectData004_Item import *
import Project_SceneFrameWork
import math

# define
STAND = 0   # 서 있기
WALK = 1    # 걷기
DOWN = 2    # 다운
MELEE_ATTACK = 3    # 근접 평타 공격
SKILL_ATTACK_1 = 4  # 첫번째 스킬 모션
SKILL_ATTACK_2 = 5  # 두번째 스킬 모션

# 32 * 64
PIXEL_PER_METER = (32.0 / 1.0)           # 32pixel == 1m


class Player(BaseUnit):
    def __init__(self, hp, max_hp, mp, max_mp, stamina, max_stamina,
                 strength, defense, magic, magic_resist, move_speed, atk_speed):
        super(Player, self).__init__(hp, max_hp, mp, max_mp, stamina, max_stamina,
                                     strength, defense, magic, magic_resist, move_speed, atk_speed)
        self.class_num = 1
        self.image = load_image("Resource_Image\\Player001_SwordMan.png")
        self.width = 32  # 스프라이트 x축 길이
        self.height = 64  # 스프라이트 y축 길이
        self.LEVEL = 1
        self.Experience = 0
        self.Max_Experience = (self.LEVEL * 8) + 2
        self.Ability_Point = 0
        self.Skill_Point = 1

        self.HpPotion = HpPotion(3)  # HP 포션 3개 소지
        self.MpPotion = MpPotion(1)  # MP 포션 1개 소지
        self.StaminaPotion = StaminaPotion(1)  # SP 포션 2개 소지
        self.dir = 2            # 캐릭터가 바라보고 있는 방향을 나타내는 변수. 숫자 키패드의 위치로 판단

        self.state = STAND      # 캐릭터의 현재 모션 상태를 나타내고 있는 변수
        self.old_state = 0      # 캐릭터의 과거 모션 상태를 저장하는 변수
        self.distance = 0       # 캐릭터의 이동 거리

        # 모션 출력용 프레임 조절 변수 (직접적인 스프라이트 위치와 무관)
        self.walk_motion = 0
        self.attack_motion = 0

        # 공격범위 변수. 공격위치의 중점 좌표와, 공격 히트박스의 크기를 의미한다.
        self.melee_atk_point_x = self.x
        self.melee_atk_point_y = self.y
        self.melee_atk_reach = 36   # 공격범위 1.125m
        self.attack_size = 32       # 공격범위 1m

        self.life_regenerate_time = 0.0
        self.mana_regenerate_time = 0.0
        self.stamina_regenerate_time = 0.0

        # 디버깅용 바운딩박스 출력
        self.box_draw_Trigger = False

        self.attack_sound = None
        self.Level_up_sound = None
        if self.Level_up_sound is None:
            self.Level_up_sound = load_wav('Resource_Sound\\Effect_Sound\\LevelUp.wav')
            self.Level_up_sound.set_volume(128)

    def show_stat(self):
        print('Lv. {}'.format(self.LEVEL))
        super(Player, self).show_stat()
        print('AP : {}'.format(self.Ability_Point))
        print('SP : {}'.format(self.Skill_Point))
        print('Exp : {}'.format(self.Experience), '/ {}'.format(self.Max_Experience))

    def update(self, frame_time, others):
        self.life_regenerate_time += frame_time
        self.mana_regenerate_time += frame_time
        self.stamina_regenerate_time += frame_time

        # 자연치유
        if self.life_regenerate_time >= 1.5:
            self.hp_heal(1 + (self.MAX_HP / 100))
            self.life_regenerate_time = 0

        if self.mana_regenerate_time >= 2.5:
            self.mp_heal(1 + (self.MAX_MP / 100))
            self.mana_regenerate_time = 0

        if self.stamina_regenerate_time >= 2.0:
            self.sp_heal(1 + (self.MAX_STAMINA / 100))
            self.stamina_regenerate_time = 0

        # 걷거나 서 있을 때
        if self.state == WALK:
            self.distance = self.RUN_SPEED_PPS * frame_time
            self.total_frames_run += self.FRAMES_PER_ACTION_run * self.ACTION_PER_TIME_run * frame_time
            self.walk_motion = int(self.total_frames_run) % 4
            if self.walk_motion is 3:
                self.frame = 1
            else:
                self.frame = self.walk_motion
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

        # 근접 공격 중일 때
        elif self.state is MELEE_ATTACK:
            # 공격범위 변수
            if self.dir == 2:
                self.melee_atk_point_x = self.x
                self.melee_atk_point_y = self.y - self.melee_atk_reach
            elif self.dir == 4:
                self.melee_atk_point_x = self.x - self.melee_atk_reach
                self.melee_atk_point_y = self.y
            elif self.dir == 6:
                self.melee_atk_point_x = self.x + self.melee_atk_reach
                self.melee_atk_point_y = self.y
            elif self.dir == 8:
                self.melee_atk_point_x = self.x
                self.melee_atk_point_y = self.y + self.melee_atk_reach
            elif self.dir == 1:
                self.melee_atk_point_x = self.x - (math.sqrt(0.5) * self.melee_atk_reach)
                self.melee_atk_point_y = self.y - (math.sqrt(0.5) * self.melee_atk_reach)
            elif self.dir == 3:
                self.melee_atk_point_x = self.x + (math.sqrt(0.5) * self.melee_atk_reach)
                self.melee_atk_point_y = self.y - (math.sqrt(0.5) * self.melee_atk_reach)
            elif self.dir == 7:
                self.melee_atk_point_x = self.x - (math.sqrt(0.5) * self.melee_atk_reach)
                self.melee_atk_point_y = self.y + (math.sqrt(0.5) * self.melee_atk_reach)
            elif self.dir == 9:
                self.melee_atk_point_x = self.x + (math.sqrt(0.5) * self.melee_atk_reach)
                self.melee_atk_point_y = self.y + (math.sqrt(0.5) * self.melee_atk_reach)
            self.total_frames_atk += self.FRAMES_PER_ACTION_atk * self.ACTION_PER_TIME_atk * frame_time
            self.attack_motion = int(self.total_frames_atk) % 3
            if self.attack_motion >= 2:
                if self.attack_sound is not None:
                    self.attack_sound.play()
                self.attack_motion = 0
                if self.old_state < 2:
                    self.state = self.old_state
                self.total_frames_atk = 0.0

        # 피격 시 무적을 0.25초간 걸어서 탈출 가능하게 해줌
        if self.invincibility is True:
            self.invincible_time += frame_time
            if self.invincible_time > 0.25:
                self.invincibility = False
                self.invincible_time = 0

    def draw(self):
        # 현재 캐릭터의 바라보는 방향에 따라 이동, 걷기 이미지 출력
        if self.state is STAND or self.state is WALK:
            if self.dir is 2:
                self.image.clip_draw(self.frame * self.width, self.height * 7, self.width, self.height,
                                     self.x - self.background.window_left, self.y - self.background.window_bottom)
            elif self.dir is 8:
                self.image.clip_draw(self.frame * self.width, self.height * 6, self.width, self.height,
                                     self.x - self.background.window_left, self.y - self.background.window_bottom)
            elif self.dir is 4:
                self.image.clip_draw(self.frame * self.width, self.height * 5, self.width, self.height,
                                     self.x - self.background.window_left, self.y - self.background.window_bottom)
            elif self.dir is 6:
                self.image.clip_draw(self.frame * self.width, self.height * 4, self.width, self.height,
                                     self.x - self.background.window_left, self.y - self.background.window_bottom)
            # 대각선 이미지인 경우 프레임 위치 조정
            elif self.dir is 1:
                self.image.clip_draw((self.frame + 3) * self.width, self.height * 7, self.width, self.height,
                                     self.x - self.background.window_left, self.y - self.background.window_bottom)
            elif self.dir is 3:
                self.image.clip_draw((self.frame + 3) * self.width, self.height * 6, self.width, self.height,
                                     self.x - self.background.window_left, self.y - self.background.window_bottom)
            elif self.dir is 7:
                self.image.clip_draw((self.frame + 3) * self.width, self.height * 5, self.width, self.height,
                                     self.x - self.background.window_left, self.y - self.background.window_bottom)
            elif self.dir is 9:
                self.image.clip_draw((self.frame + 3) * self.width, self.height * 4, self.width, self.height,
                                     self.x - self.background.window_left, self.y - self.background.window_bottom)
        # 현재 캐릭터의 바라보는 방향에 따라 근접 공격 애니메이션 출력
        elif self.state is MELEE_ATTACK:
            if self.dir is 2:
                if self.box_draw_Trigger:
                    self.draw_hbs(self.melee_atk_point_x, self.melee_atk_point_y, self.attack_size)
                if self.attack_motion is 0:
                    self.image.clip_draw(self.width * 2, self.height * 3, self.width * 2, self.height,
                                         self.x - self.background.window_left, self.y - self.background.window_bottom)
                elif self.attack_motion is 1:
                    self.image.clip_draw(self.width * 6, self.height * 7, self.width * 2, self.height,
                                         self.x - self.background.window_left, self.y - self.background.window_bottom)
            elif self.dir is 8:
                if self.box_draw_Trigger:
                    self.draw_hbs(self.melee_atk_point_x, self.melee_atk_point_y, self.attack_size)
                if self.attack_motion is 0:
                    self.image.clip_draw(self.width * 4, self.height * 3, self.width * 2, self.height,
                                         self.x - self.background.window_left, self.y - self.background.window_bottom)
                elif self.attack_motion is 1:
                    self.image.clip_draw(self.width * 6, self.height * 6, self.width * 2, self.height,
                                         self.x - self.background.window_left, self.y - self.background.window_bottom)
            elif self.dir is 4:
                if self.box_draw_Trigger:
                    self.draw_hbs(self.melee_atk_point_x, self.melee_atk_point_y, self.attack_size)
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
                    self.draw_hbs(self.melee_atk_point_x, self.melee_atk_point_y, self.attack_size)
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
                    self.draw_hbs(self.melee_atk_point_x, self.melee_atk_point_y, self.attack_size)
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
                    self.draw_hbs(self.melee_atk_point_x, self.melee_atk_point_y, self.attack_size)
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
                    self.draw_hbs(self.melee_atk_point_x, self.melee_atk_point_y, self.attack_size)
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
                    self.draw_hbs(self.melee_atk_point_x, self.melee_atk_point_y, self.attack_size)
                if self.attack_motion is 0:
                    self.image.clip_draw(self.width * 2, self.height * 0, self.width * 2, self.height,
                                         self.x - self.background.window_left + 11,
                                         self.y - self.background.window_bottom)
                elif self.attack_motion is 1:
                    self.image.clip_draw(self.width * 0, self.height * 0, self.width * 2, self.height,
                                         self.x - self.background.window_left + 2,
                                         self.y - self.background.window_bottom)

    def handle_events(self, event):
        if self.state == STAND or self.state == WALK or self.state == MELEE_ATTACK:
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_LEFT):
                if (self.dir == 8 or self.dir == 9) and self.state is WALK:
                    self.dir = 7
                elif (self.dir == 2 or self.dir == 3) and self.state is WALK:
                    self.dir = 1
                else:
                    self.dir = 4
                self.state = WALK
            elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_RIGHT):
                if (self.dir == 8 or self.dir == 7) and self.state is WALK:
                    self.dir = 9
                elif (self.dir == 2 or self.dir == 1) and self.state is WALK:
                    self.dir = 3
                else:
                    self.dir = 6
                self.state = WALK
            elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_UP):
                if self.dir == 4 and self.state is WALK:
                    self.dir = 7
                elif self.dir == 6 and self.state is WALK:
                    self.dir = 9
                else:
                    self.dir = 8
                self.state = WALK
            elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_DOWN):
                if self.dir == 4 and self.state is WALK:
                    self.dir = 1
                elif self.dir == 6 and self.state is WALK:
                    self.dir = 3
                else:
                    self.dir = 2
                self.state = WALK
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_z):      # z 키 - 일반 근접 공격
                if self.state < 2:
                    self.old_state = self.state
                self.state = MELEE_ATTACK
            elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_o):      # o 키 - 히트박스, 바운딩박스 그리기
                if self.box_draw_Trigger:
                    self.box_draw_Trigger = False
                else:
                    self.box_draw_Trigger = True
            # elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_u):  # u 키 - Player
            #    self.show_stat()
            # elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_i):  # i 키 - 아이템 창
            #    print('HP Potion : {}'.format(self.HpPotion.number))

            if (event.type, event.key) == (SDL_KEYUP, SDLK_LEFT):
                if self.dir == 7:
                    self.dir = 8
                elif self.dir == 1:
                    self.dir = 2
                elif self.dir == 4:
                    if self.state is WALK:
                        self.state = STAND
            elif (event.type, event.key) == (SDL_KEYUP, SDLK_RIGHT):
                if self.dir == 9:
                    self.dir = 8
                elif self.dir == 3:
                    self.dir = 2
                elif self.dir == 6:
                    if self.state is WALK:
                        self.state = STAND
            elif (event.type, event.key) == (SDL_KEYUP, SDLK_UP):
                if self.dir == 7:
                    self.dir = 4
                elif self.dir == 9:
                    self.dir = 6
                elif self.dir == 8:
                    self.state = STAND
            elif (event.type, event.key) == (SDL_KEYUP, SDLK_DOWN):
                if self.dir == 1:
                    self.dir = 4
                elif self.dir == 3:
                    self.dir = 6
                elif self.dir == 2:
                    if self.state is WALK:
                        self.state = STAND

            if self.state > 2 and event.type == SDL_KEYUP:
                if self.old_state is WALK:
                    self.old_state = STAND

        if (event.type, event.key) == (SDL_KEYDOWN, SDLK_h):  # h 키 - HP 포션 단축키
            self.HpPotion.use(self)
        if (event.type, event.key) == (SDL_KEYDOWN, SDLK_j):  # j 키 - MP 포션 단축키
            self.MpPotion.use(self)
        if (event.type, event.key) == (SDL_KEYDOWN, SDLK_k):  # k 키 - 스태미나 포션 단축키
            self.StaminaPotion.use(self)

    def get_exp(self, exp):
        self.Experience += exp
        if self.Experience >= self.Max_Experience:
            self.level_up()

    def level_up(self):
            self.Level_up_sound.play()
            self.Experience -= self.Max_Experience
            self.LEVEL += 1
            self.Ability_Point += 3
            self.Skill_Point += 1
            self.Max_Experience = (self.LEVEL * 8) + 2

    def hit_by_str(self, damage, direction, others):
        super(Player, self).hit_by_str(damage)
        if self.hit_sound is not None:
            self.hit_sound_play()
        self.knock_back(direction, others)

    def hit_by_mag(self, damage, direction, others):
        super(Player, self).hit_by_mag(damage)
        self.knock_back(direction, others)

    # 충돌체크용 히트박스
    def get_bb(self):
        return self.x - self.width / 2, self.y - self.height / 4, self.x + self.width / 2, self.y + self.height / 4

    def draw_bb(self):
        draw_rectangle(self.get_bb()[0] - self.background.window_left,
                       self.get_bb()[1] - self.background.window_bottom,
                       self.get_bb()[2] - self.background.window_left,
                       self.get_bb()[3] - self.background.window_bottom)

    # 근접 평타공격 충돌체크 박스
    def get_melee_atk_hb(self):
        return self.melee_atk_point_x - (self.attack_size / 2), \
               self.melee_atk_point_y - (self.attack_size / 2), \
               self.melee_atk_point_x + (self.attack_size / 2), \
               self.melee_atk_point_y + (self.attack_size / 2)

    # 근접 평타공격 객체간 충돌체크
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
        if self.state is MELEE_ATTACK and self.attack_motion == 0:
            return True


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
