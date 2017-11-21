from pico2d import *
from ObjectData000_BaseObject_BaseUnit import *
import Project_SceneFrameWork

# define
SizeX = 32  # 스프라이트 x축 길이
SizeY = 64  # 스프라이트 y축 길이

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
        self.LEVEL = 1
        self.Ability_Point = 0
        self.Skill_Point = 0
        self.dir = 2            # 캐릭터가 바라보고 있는 방향을 나타내는 변수. 숫자 키패드의 위치로 판단
        self.state = STAND      # 캐릭터의 현재 모션 상태를 나타내고 있는 변수
        self.walk_motion = 0
        self.attack_motion = 0

        # 프레임 타임 애니메이션 관련 변수들 정의
        self.total_frames_run = 0.0
        self.total_frames_atk = 0.0
        self.life_time = 0.0
        self.RUN_SPEED_KMPH = self.MOVE_SPEED  # Km / Hour
        self.RUN_SPEED_MPM = (self.RUN_SPEED_KMPH * 1000.0 / 60.0)
        self.RUN_SPEED_MPS = (self.RUN_SPEED_MPM / 60.0)
        self.RUN_SPEED_PPS = (self.RUN_SPEED_MPS * PIXEL_PER_METER)
        self.TIME_PER_ACTION_run = 0.5
        self.ACTION_PER_TIME_run = 1.0 / self.TIME_PER_ACTION_run
        self.FRAMES_PER_ACTION_run = 8
        self.TIME_PER_ACTION_atk = 2.5
        self.ACTION_PER_TIME_atk = self.ATK_SPEED / self.TIME_PER_ACTION_atk
        self.FRAMES_PER_ACTION_atk = 8

        # 공격범위 변수
        self.melee_atk_p_x1 = self.x - SizeX / 2
        self.melee_atk_p_y1 = self.y - SizeY / 4
        self.melee_atk_p_x2 = self.x + SizeX / 2
        self.melee_atk_p_y2 = self.y + SizeY / 4
        self.attack_size = 40

    def show_stat(self):
        print('Lv. {}'.format(self.LEVEL))
        super(Player, self).show_stat()
        print('AP : {}'.format(self.Ability_Point))
        print('SP : {}'.format(self.Skill_Point))

    def update(self, frame_time):
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
                self.y = min(Project_SceneFrameWork.Window_H, self.y + distance)
            elif self.dir is 4:
                self.x = max(0, self.x - distance)
            elif self.dir is 6:
                self.x = min(Project_SceneFrameWork.Window_W, self.x + distance)
            elif self.dir is 1:
                self.x = max(0, self.x - distance)
                self.y = max(0, self.y - distance)
            elif self.dir is 3:
                self.x = min(Project_SceneFrameWork.Window_W, self.x + distance)
                self.y = max(0, self.y - distance)
            elif self.dir is 7:
                self.x = max(0, self.x - distance)
                self.y = min(Project_SceneFrameWork.Window_H, self.y + distance)
            elif self.dir is 9:
                self.x = min(Project_SceneFrameWork.Window_W, self.x + distance)
                self.y = min(Project_SceneFrameWork.Window_H, self.y + distance)
        # 근접 공격 중일 때
        elif self.state is MELEE_ATTACK:
            # 공격범위 변수
            self.melee_atk_p_x1 = self.x - SizeX / 2
            self.melee_atk_p_y1 = self.y - SizeY / 4
            self.melee_atk_p_x2 = self.x + SizeX / 2
            self.melee_atk_p_y2 = self.y + SizeY / 4
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
                self.image.clip_draw(self.frame * SizeX, SizeY * 7, SizeX, SizeY, self.x, self.y)
            elif self.dir is 8:
                self.image.clip_draw(self.frame * SizeX, SizeY * 6, SizeX, SizeY, self.x, self.y)
            elif self.dir is 4:
                self.image.clip_draw(self.frame * SizeX, SizeY * 5, SizeX, SizeY, self.x, self.y)
            elif self.dir is 6:
                self.image.clip_draw(self.frame * SizeX, SizeY * 4, SizeX, SizeY, self.x, self.y)
            # 대각선 이미지인 경우 프레임 위치 조정
            elif self.dir is 1:
                self.image.clip_draw((self.frame + 3) * SizeX, SizeY * 7, SizeX, SizeY, self.x, self.y)
            elif self.dir is 3:
                self.image.clip_draw((self.frame + 3) * SizeX, SizeY * 6, SizeX, SizeY, self.x, self.y)
            elif self.dir is 7:
                self.image.clip_draw((self.frame + 3) * SizeX, SizeY * 5, SizeX, SizeY, self.x, self.y)
            elif self.dir is 9:
                self.image.clip_draw((self.frame + 3) * SizeX, SizeY * 4, SizeX, SizeY, self.x, self.y)
        # 현재 캐릭터의 바라보는 방향에 따라 근접 공격 애니메이션 출력
        elif self.state is MELEE_ATTACK:
            if self.dir is 2:
                self.draw_hbs(self.x, self.melee_atk_p_y1 - SizeY / 4, self.attack_size)
                if self.attack_motion is 0:
                    self.image.clip_draw(SizeX * 2, SizeY * 3, SizeX * 2, SizeY, self.x, self.y)
                elif self.attack_motion is 1:
                    self.image.clip_draw(SizeX * 6, SizeY * 7, SizeX * 2, SizeY, self.x, self.y)
            elif self.dir is 8:
                self.draw_hbs(self.x, self.melee_atk_p_y2 + SizeY / 4, self.attack_size)
                if self.attack_motion is 0:
                    self.image.clip_draw(SizeX * 4, SizeY * 3, SizeX * 2, SizeY, self.x, self.y)
                elif self.attack_motion is 1:
                    self.image.clip_draw(SizeX * 6, SizeY * 6, SizeX * 2, SizeY, self.x, self.y)
            elif self.dir is 4:
                self.draw_hbs(self.melee_atk_p_x1 - SizeX / 2, self.y, self.attack_size)
                if self.attack_motion is 0:
                    self.image.clip_draw(SizeX * 4, SizeY * 1, SizeX * 2, SizeY, self.x - SizeX / 2, self.y)
                elif self.attack_motion is 1:
                    self.image.clip_draw(SizeX * 6, SizeY * 5, SizeX * 2, SizeY, self.x - SizeX / 2, self.y)
            elif self.dir is 6:
                self.draw_hbs(self.melee_atk_p_x2 + SizeX / 2, self.y, self.attack_size)
                if self.attack_motion is 0:
                    self.image.clip_draw(SizeX * 2, SizeY * 1, SizeX * 2, SizeY, self.x + SizeX / 2, self.y)
                elif self.attack_motion is 1:
                    self.image.clip_draw(SizeX * 6, SizeY * 4, SizeX * 2, SizeY, self.x + SizeX / 2, self.y)
            # 대각선 이미지인 경우 프레임 위치 조정
            elif self.dir is 1:
                self.draw_hbs(self.melee_atk_p_x1, self.melee_atk_p_y1, self.attack_size)
                if self.attack_motion is 0:
                    self.image.clip_draw(SizeX * 4, SizeY * 0, SizeX * 2, SizeY, self.x - 7, self.y)
                elif self.attack_motion is 1:
                    self.image.clip_draw(SizeX * 0, SizeY * 3, SizeX * 2, SizeY, self.x, self.y)
            elif self.dir is 3:
                self.draw_hbs(self.melee_atk_p_x2, self.melee_atk_p_y1, self.attack_size)
                if self.attack_motion is 0:
                    self.image.clip_draw(SizeX * 2, SizeY * 2, SizeX * 2, SizeY, self.x, self.y)
                elif self.attack_motion is 1:
                    self.image.clip_draw(SizeX * 0, SizeY * 2, SizeX * 2, SizeY, self.x, self.y)
            elif self.dir is 7:
                self.draw_hbs(self.melee_atk_p_x1, self.melee_atk_p_y2, self.attack_size)
                if self.attack_motion is 0:
                    self.image.clip_draw(SizeX * 4, SizeY * 2, SizeX * 2, SizeY, self.x, self.y)
                elif self.attack_motion is 1:
                    self.image.clip_draw(SizeX * 0, SizeY * 1, SizeX * 2, SizeY, self.x, self.y)
            elif self.dir is 9:
                self.draw_hbs(self.melee_atk_p_x2, self.melee_atk_p_y2, self.attack_size)
                if self.attack_motion is 0:
                    self.image.clip_draw(SizeX * 2, SizeY * 0, SizeX * 2, SizeY, self.x + 11, self.y)
                elif self.attack_motion is 1:
                    self.image.clip_draw(SizeX * 0, SizeY * 0, SizeX * 2, SizeY, self.x + 2, self.y)

    def handle_events(self, event):
        if (event.type, event.key) == (SDL_KEYDOWN, SDLK_LEFT):
            if self.dir == 8 and self.state is WALK:
                self.dir = 7
            elif self.dir == 2 and self.state is WALK:
                self.dir = 1
            else:
                self.dir = 4
            self.state = WALK
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_RIGHT):
            if self.dir == 8 and self.state is WALK:
                self.dir = 9
            elif self.dir == 2 and self.state is WALK:
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
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_z):
            self.state = MELEE_ATTACK
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_p):
            self.show_stat()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_o):
            print("x, y : (%d, %d) / x1, y1 : (%d, %d) / x2, y2 : (%d, %d)" % (self.x, self.y, self.melee_atk_p_x1, self.melee_atk_p_y1, self.melee_atk_p_x2, self.melee_atk_p_y2))
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
        if (event.type, self.state) == (SDL_KEYUP, WALK):
            self.state = STAND

    def get_bb(self):
        return self.x - SizeX / 2, self.y - SizeY / 2, self.x + SizeX / 2, self.y + SizeY / 2