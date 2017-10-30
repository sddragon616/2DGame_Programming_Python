from pico2d import *
from ObjectData000_BaseObject_BaseUnit import *

# define
SizeX = 32  # 스프라이트 x축 길이
SizeY = 64  # 스프라이트 y축 길이

STAND = 0   # 서 있기
WALK = 1    # 걷기
DOWN = 2    # 다운
MELEE_ATTACK = 3    # 근접 평타 공격
SKILL_ATTACK_1 = 4  # 첫번째 스킬 모션
SKILL_ATTACK_2 = 4  # 두번째 스킬 모션


class Player(BaseUnit):
    def __init__(self, hp, max_hp, mp, max_mp, stamina, max_stamina,
                 strength, defense, magic, magic_resist, move_speed, atk_speed):
        super(Player, self).__init__(hp, max_hp, mp, max_mp, stamina, max_stamina,
                                     strength, defense, magic, magic_resist, move_speed, atk_speed)
        self.image = load_image("Player001_SwordMan.png")
        self.LEVEL = 1
        self.Ability_Point = 0
        self.Skill_Point = 0
        self.dir = 2    # 캐릭터가 바라보고 있는 방향을 나타내는 변수. 숫자 키배드의 위치로 판단
        self.state = STAND  # 캐릭터의 현재 모션 상태를 나타내고 있는 변수
        self.walk_motion = 0

    def show_stat(self):
        print('Lv. {}'.format(self.LEVEL))
        super(Player, self).show_stat()

    def update(self):
        if self.state == WALK:
            self.walk_motion = (self.walk_motion + 1) % 4
            if self.walk_motion is 3:
                self.frame = 1
            else:
                self.frame = self.walk_motion
                if self.dir is 2:
                    self.y -= self.MOVE_SPEED
                elif self.dir is 8:
                    self.y += self.MOVE_SPEED
                elif self.dir is 4:
                    self.x -= self.MOVE_SPEED
                elif self.dir is 6:
                    self.x += self.MOVE_SPEED
                elif self.dir is 1:
                    self.x -= self.MOVE_SPEED
                    self.y -= self.MOVE_SPEED
                elif self.dir is 3:
                    self.x += self.MOVE_SPEED
                    self.y -= self.MOVE_SPEED
                elif self.dir is 7:
                    self.x -= self.MOVE_SPEED
                    self.y += self.MOVE_SPEED
                elif self.dir is 9:
                    self.x += self.MOVE_SPEED
                    self.y += self.MOVE_SPEED

    def draw(self):
        # 현재 캐릭터의 바라보는 방향에 따라 이동, 걷기 이미지 출력
        if self.state is STAND or WALK:
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

    def handle_events(self, event):
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
        elif event.type == SDL_KEYUP:
            self.state = STAND


