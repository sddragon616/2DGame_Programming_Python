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
PIXEL_PER_METER = (32.0 / 1.0)           # 32pixel 1m


class Player(BaseUnit):
    RUN_SPEED_KMPH = 20.0  # Km / Hour
    RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
    RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
    RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)
    TIME_PER_ACTION = 0.5
    ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
    FRAMES_PER_ACTION = 8

    def __init__(self, hp, max_hp, mp, max_mp, stamina, max_stamina,
                 strength, defense, magic, magic_resist, move_speed, atk_speed):
        super(Player, self).__init__(hp, max_hp, mp, max_mp, stamina, max_stamina,
                                     strength, defense, magic, magic_resist, move_speed, atk_speed)
        self.image = load_image("Resource_Image\\Player001_SwordMan.png")
        self.LEVEL = 1
        self.Ability_Point = 0
        self.Skill_Point = 0
        self.dir = 2            # 캐릭터가 바라보고 있는 방향을 나타내는 변수. 숫자 키배드의 위치로 판단
        self.state = STAND      # 캐릭터의 현재 모션 상태를 나타내고 있는 변수
        self.walk_motion = 0
        self.attack_motion = 0
        self.total_frames = 0.0
        self.life_time = 0.0

    def show_stat(self):
        print('Lv. {}'.format(self.LEVEL))
        super(Player, self).show_stat()
        print('AP : {}'.format(self.Ability_Point))
        print('SP : {}'.format(self.Skill_Point))

    def update(self, frame_time):
        self.life_time += frame_time
        distance = Player.RUN_SPEED_PPS * frame_time
        self.total_frames += Player.FRAMES_PER_ACTION * Player.ACTION_PER_TIME * frame_time
        self.x += distance
        if self.state == WALK:
            self.walk_motion = (self.walk_motion + 1) % 4
            if self.walk_motion is 3:
                self.frame = 1
            else:
                self.frame = self.walk_motion
                cnt = 0
                while cnt < 1000:
                    cnt += self.MOVE_SPEED
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
        elif self.state is MELEE_ATTACK:
            for n in range(100000):
                n += 1
            if self.attack_motion > 1:
                self.attack_motion = 0
                # self.state = STAND
            self.attack_motion = (self.attack_motion + 1)

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
        elif self.state is MELEE_ATTACK:
            if self.dir is 2:
                if self.attack_motion is 0:
                    self.image.clip_draw(SizeX * 2, SizeY * 3, SizeX * 2, SizeY, self.x, self.y)
                elif self.attack_motion is 1:
                    self.image.clip_draw(SizeX * 6, SizeY * 7, SizeX * 2, SizeY, self.x, self.y)
            elif self.dir is 8:
                if self.attack_motion is 0:
                    self.image.clip_draw(SizeX * 4, SizeY * 3, SizeX * 2, SizeY, self.x, self.y)
                elif self.attack_motion is 1:
                    self.image.clip_draw(SizeX * 6, SizeY * 6, SizeX * 2, SizeY, self.x, self.y)
            elif self.dir is 4:
                if self.attack_motion is 0:
                    self.image.clip_draw(SizeX * 4, SizeY * 1, SizeX * 2, SizeY, self.x, self.y)
                elif self.attack_motion is 1:
                    self.image.clip_draw(SizeX * 6, SizeY * 5, SizeX * 2, SizeY, self.x, self.y)
            elif self.dir is 6:
                if self.attack_motion is 0:
                    self.image.clip_draw(SizeX * 2, SizeY * 1, SizeX * 2, SizeY, self.x, self.y)
                elif self.attack_motion is 1:
                    self.image.clip_draw(SizeX * 6, SizeY * 4, SizeX * 2, SizeY, self.x, self.y)
            # 대각선 이미지인 경우 프레임 위치 조정
            elif self.dir is 1:
                if self.attack_motion is 0:
                    self.image.clip_draw(SizeX * 4, SizeY * 0, SizeX * 2, SizeY, self.x, self.y)
                elif self.attack_motion is 1:
                    self.image.clip_draw(SizeX * 0, SizeY * 3, SizeX * 2, SizeY, self.x, self.y)
            elif self.dir is 3:
                if self.attack_motion is 0:
                    self.image.clip_draw(SizeX * 2, SizeY * 2, SizeX * 2, SizeY, self.x, self.y)
                elif self.attack_motion is 1:
                    self.image.clip_draw(SizeX * 0, SizeY * 2, SizeX * 2, SizeY, self.x, self.y)
            elif self.dir is 7:
                if self.attack_motion is 0:
                    self.image.clip_draw(SizeX * 4, SizeY * 2, SizeX * 2, SizeY, self.x, self.y)
                elif self.attack_motion is 1:
                    self.image.clip_draw(SizeX * 0, SizeY * 1, SizeX * 2, SizeY, self.x, self.y)
            elif self.dir is 9:
                if self.attack_motion is 0:
                    self.image.clip_draw(SizeX * 2, SizeY * 0, SizeX * 2, SizeY, self.x, self.y)
                elif self.attack_motion is 1:
                    self.image.clip_draw(SizeX * 0, SizeY * 0, SizeX * 2, SizeY, self.x, self.y)
            cnt = 0
            while cnt < 100000:
                cnt += self.ATK_SPEED



    def handle_events(self, event):
        ## if (event.type, event.key) == (SDL_KEYDOWN, SDLK_LEFT and SDLK_DOWN):
        ##     self.dir = 1
        ##     self.state = WALK
        ## elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_RIGHT and SDLK_DOWN):
        ##     self.dir = 3
        ##     self.state = WALK
        ## elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_LEFT and SDLK_UP):
        ##     self.dir = 7
        ##     self.state = WALK
        ## elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_RIGHT and SDLK_UP):
        ##     self.dir = 9
        ##     self.state = WALK
        if (event.type, event.key) == (SDL_KEYDOWN, SDLK_LEFT):
            self.dir = 4
            self.state = WALK
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_RIGHT):
            self.dir = 6
            self.state = WALK
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_UP):
            self.dir = 8
            self.state = WALK
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_DOWN):
            self.dir = 2
            self.state = WALK
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_z):
            self.state = MELEE_ATTACK
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_p):
            self.show_stat()
        elif (event.type, self.state) == (SDL_KEYUP, WALK):
            self.state = STAND


