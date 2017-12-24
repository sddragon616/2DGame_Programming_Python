from pico2d import *
from ObjectData000_BaseObject_BaseUnit import *
from ObjectData004_Item import *
import Project_SceneFrameWork

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
        self.image = load_image("Resource_Image\\Player001_SwordMan.png")
        self.width = 32  # 스프라이트 x축 길이
        self.height = 64  # 스프라이트 y축 길이
        self.LEVEL = 1
        self.Experience = 0
        self.Ability_Point = 0
        self.Skill_Point = 0

        self.HpPotion = HpPotion(3)    # HP 포션 3개 소지
        self.dir = 2            # 캐릭터가 바라보고 있는 방향을 나타내는 변수. 숫자 키패드의 위치로 판단

        self.state = STAND      # 캐릭터의 현재 모션 상태를 나타내고 있는 변수

        # 모션 출력용 프레임 조절 변수 (직접적인 스프라이트 위치와 무관)
        self.walk_motion = 0
        self.attack_motion = 0

        # 공격범위 변수.
        self.melee_atk_point_LeftX = self.x - self.width / 2
        self.melee_atk_point_DownY = self.y - self.height / 4
        self.melee_atk_point_RightX = self.x + self.width / 2
        self.melee_atk_point_UpY = self.y + self.height / 4
        self.attack_size = 40   # 공격범위 1.25m

        # 디버깅용 바운딩박스 출력
        self.box_draw = False

    def show_stat(self):
        print('Lv. {}'.format(self.LEVEL))
        super(Player, self).show_stat()
        print('AP : {}'.format(self.Ability_Point))
        print('SP : {}'.format(self.Skill_Point))
        print('Exp : {}'.format(self.Experience), '/ {}'.format(self.LEVEL * 10))

    def update(self, frame_time):
        self.death()
        self.life_time += frame_time
        # 걷거나 서 있을 때
        if self.state == WALK:
            distance = self.RUN_SPEED_PPS * frame_time
            self.total_frames_run += self.FRAMES_PER_ACTION_run * self.ACTION_PER_TIME_run * frame_time
            self.walk_motion = int(self.total_frames_run) % 4
            if self.walk_motion is 3:
                self.frame = 1
            else:
                self.frame = self.walk_motion
            if self.dir is 2:
                self.y = max(0, self.y - distance)
            elif self.dir is 8:
                self.y = min(self.background.h, self.y + distance)
            elif self.dir is 4:
                self.x = max(0, self.x - distance)
            elif self.dir is 6:
                self.x = min(self.background.w, self.x + distance)
            elif self.dir is 1:
                self.x = max(0, self.x - distance)
                self.y = max(0, self.y - distance)
            elif self.dir is 3:
                self.x = min(self.background.w, self.x + distance)
                self.y = max(0, self.y - distance)
            elif self.dir is 7:
                self.x = max(0, self.x - distance)
                self.y = min(self.background.h, self.y + distance)
            elif self.dir is 9:
                self.x = min(self.background.w, self.x + distance)
                self.y = min(self.background.h, self.y + distance)
        # 근접 공격 중일 때
        elif self.state is MELEE_ATTACK:
            # 공격범위 변수
            self.melee_atk_point_LeftX = self.x - self.width / 2
            self.melee_atk_point_DownY = self.y - self.height / 4
            self.melee_atk_point_RightX = self.x + self.width / 2
            self.melee_atk_point_UpY = self.y + self.height / 4
            self.total_frames_atk += self.FRAMES_PER_ACTION_atk * self.ACTION_PER_TIME_atk * frame_time
            self.attack_motion = int(self.total_frames_atk) % 3
            if self.attack_motion > 1:
                self.attack_motion = 0
                self.state = STAND
                self.total_frames_atk = 0.0

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
                if self.box_draw:
                    self.draw_hbs(self.x, self.melee_atk_point_DownY - self.height / 4, self.attack_size)
                if self.attack_motion is 0:
                    self.image.clip_draw(self.width * 2, self.height * 3, self.width * 2, self.height,
                                         self.x - self.background.window_left, self.y - self.background.window_bottom)
                elif self.attack_motion is 1:
                    self.image.clip_draw(self.width * 6, self.height * 7, self.width * 2, self.height,
                                         self.x - self.background.window_left, self.y - self.background.window_bottom)
            elif self.dir is 8:
                if self.box_draw:
                    self.draw_hbs(self.x, self.melee_atk_point_UpY + self.height / 4, self.attack_size)
                if self.attack_motion is 0:
                    self.image.clip_draw(self.width * 4, self.height * 3, self.width * 2, self.height,
                                         self.x - self.background.window_left, self.y - self.background.window_bottom)
                elif self.attack_motion is 1:
                    self.image.clip_draw(self.width * 6, self.height * 6, self.width * 2, self.height,
                                         self.x - self.background.window_left, self.y - self.background.window_bottom)
            elif self.dir is 4:
                if self.box_draw:
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
                if self.box_draw:
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
                if self.box_draw:
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
                if self.box_draw:
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
                if self.box_draw:
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
                if self.box_draw:
                    self.draw_hbs(self.melee_atk_point_RightX, self.melee_atk_point_UpY, self.attack_size)
                if self.attack_motion is 0:
                    self.image.clip_draw(self.width * 2, self.height * 0, self.width * 2, self.height,
                                         self.x - self.background.window_left + 11,
                                         self.y - self.background.window_bottom)
                elif self.attack_motion is 1:
                    self.image.clip_draw(self.width * 0, self.height * 0, self.width * 2, self.height,
                                         self.x - self.background.window_left + 2,
                                         self.y - self.background.window_bottom)

    def handle_events(self, event):
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
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_z):      # z 키 - 일반 근접 공격
            self.state = MELEE_ATTACK
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_o):      # o 키 - 히트박스, 바운딩박스 그리기
            if self.box_draw:
                self.box_draw = False
            else:
                self.box_draw = True
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_u):  # u 키 - Player
            self.show_stat()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_i):  # i 키 - 아이템 창
            print('HP Potion : {}'.format(self.HpPotion.number))
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_h):  # h 키 - HP 포션 단축키
            self.HpPotion.use(self)

        if (event.type, self.state) == (SDL_KEYUP, SDLK_LEFT):
            if self.dir == 7:
                self.dir = 8
            elif self.dir == 1:
                self.dir = 2
        elif (event.type, self.state) == (SDL_KEYUP, SDLK_RIGHT):
            if self.dir == 9:
                self.dir = 8
            elif self.dir == 3:
                self.dir = 2
        elif (event.type, self.state) == (SDL_KEYUP, SDLK_UP):
            if self.dir == 7:
                self.dir = 4
            elif self.dir == 9:
                self.dir = 6
        elif (event.type, self.state) == (SDL_KEYUP, SDLK_DOWN):
            if self.dir == 1:
                self.dir = 4
            elif self.dir == 3:
                self.dir = 6
        if (event.type, event.key) == (SDL_KEYUP, SDLK_LEFT):
            if self.dir == 7:
                self.dir = 8
            elif self.dir == 1:
                self.dir = 2
            elif self.dir == 4:
                self.state = STAND
        elif (event.type, event.key) == (SDL_KEYUP, SDLK_RIGHT):
            if self.dir == 9:
                self.dir = 8
            elif self.dir == 3:
                self.dir = 2
            elif self.dir == 6:
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
                self.state = STAND

    def get_exp(self, exp):
        self.Experience += exp
        self.level_up()

    def level_up(self):
        if self.Experience >= self.LEVEL*10:
            self.Experience -= self.LEVEL*10
            self.LEVEL += 1
            self.Ability_Point += 5
            # 육성 창 등장

    def hit_by_str(self, damage, direction):
        super(Player, self).hit_by_str(damage)
        if self.hit_sound is not None:
            self.hit_sound_play()
        self.knock_back(direction)

    def hit_by_mag(self, damage, direction):
        super(Player, self).hit_by_mag(damage)
        self.knock_back(direction)

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
        if self.dir == 2:
            return self.x - (self.attack_size / 2), \
                   self.melee_atk_point_DownY - self.height / 4 - (self.attack_size / 2), \
                   self.x + (self.attack_size / 2), \
                   self.melee_atk_point_DownY - self.height / 4 + (self.attack_size / 2)
        elif self.dir == 8:
            return self.x - (self.attack_size / 2), \
                   self.melee_atk_point_UpY + self.height / 4 - (self.attack_size / 2), \
                   self.x + (self.attack_size / 2), \
                   self.melee_atk_point_UpY + self.height / 4 + (self.attack_size / 2)
        elif self.dir == 4:
            return self.melee_atk_point_LeftX - self.width / 2 - (self.attack_size / 2), \
                   self.y - (self.attack_size / 2), \
                   self.melee_atk_point_LeftX - self.width / 2 + (self.attack_size / 2), \
                   self.y + (self.attack_size / 2)
        elif self.dir == 6:
            return self.melee_atk_point_RightX + self.width / 2 - (self.attack_size / 2), \
                   self.y - (self.attack_size / 2), \
                   self.melee_atk_point_RightX + self.width / 2 + (self.attack_size / 2), \
                   self.y + (self.attack_size / 2)
        elif self.dir == 7:
            return self.melee_atk_point_LeftX - (self.attack_size / 2), \
                   self.melee_atk_point_UpY - (self.attack_size / 2), \
                   self.melee_atk_point_LeftX + (self.attack_size / 2), \
                   self.melee_atk_point_UpY + (self.attack_size / 2)
        elif self.dir == 9:
            return self.melee_atk_point_RightX - (self.attack_size / 2), \
                   self.melee_atk_point_UpY - (self.attack_size / 2), \
                   self.melee_atk_point_RightX + (self.attack_size / 2), \
                   self.melee_atk_point_UpY + (self.attack_size / 2)
        elif self.dir == 1:
            return self.melee_atk_point_LeftX - (self.attack_size / 2), \
                   self.melee_atk_point_DownY - (self.attack_size / 2), \
                   self.melee_atk_point_LeftX + (self.attack_size / 2), \
                   self.melee_atk_point_DownY + (self.attack_size / 2)
        elif self.dir == 3:
            return self.melee_atk_point_RightX - (self.attack_size / 2), \
                   self.melee_atk_point_DownY - (self.attack_size / 2), \
                   self.melee_atk_point_RightX + (self.attack_size / 2), \
                   self.melee_atk_point_DownY + (self.attack_size / 2)

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
        if self.state is MELEE_ATTACK:
            return True
