from pico2d import *
import Project_SceneFrameWork

PIXEL_PER_METER = (32.0 / 1.0)  # 32pixel == 1m


class BaseObject:
    def __init__(self, hp, max_hp, defense, magic_resist, move_speed):
        self.name = self.__class__.__name__     # 현재 클래스의 이름
        self.image = load_image('Resource_Image\\Test_img.png')             # 객체의 이미지 초기화
        self.width, self.height = 1, 1          # 객체의 가로 길이, 세로 길이 초기화
        self.x, self.y = 2, 2                   # 객체의 좌표값 초기화
        self.HP = hp                            # 현재 체력
        self.MAX_HP = max_hp                    # 최대 체력
        self.DEF = defense                      # 물리 방어력
        self.MR = magic_resist                  # 마법 저향력
        self.MOVE_SPEED = move_speed            # 이동속도
        self.background = None
        self.hit_sound = None
        self.death_sound = None

        self.invincibility = False
        # 타이머 전용
        self.invincible_time = 0

    def show_stat(self):
        print('이름: {}'.format(self.name))
        print('체력: {}'.format(self.HP), ' / {}'.format(self.MAX_HP))
        print('물리 방어력: {}'.format(self.DEF))
        print('마법 저항력: {}'.format(self.MR))

    def draw(self):
        self.image.draw(self.x, self.y)

    def set_background(self, background):
        self.background = background

    def death(self):
        if self.HP <= 0:
            return True
        else:
            return False

    def hit_sound_play(self):
        self.hit_sound.play()

    def knock_back(self, direction, walls):
        if direction is 8:
            self.y = min(self.background.h, self.y + self.height/2)
        if direction is 2:
            self.y = max(0, self.y - self.height/2)
        if direction is 4:
            self.x = max(0, self.x - self.width/2)
        if direction is 6:
            self.x = min(self.background.w, self.x + self.width/2)
        if direction is 1:
            self.x = max(0, self.x - self.width / 2)
            self.y = max(0, self.y - self.height / 2)
        if direction is 3:
            self.x = min(self.background.w, self.x + self.width/2)
            self.y = max(0, self.y - self.height/2)
        if direction is 7:
            self.x = max(0, self.x - self.width/2)
            self.y = min(self.background.h, self.y + self.height/2)
        if direction is 9:
            self.x = min(self.background.w, self.x + self.width/2)
            self.y = min(self.background.h, self.y + self.height/2)
        if walls is not []:
            for wall in walls:
                if collide(self, wall):
                    self.invincibility = True     # 넉백 후 벽에 충돌 시 무적 여부
                    if direction is 8:
                        self.y = min(self.background.h, self.y - self.height/2)
                    if direction is 2:
                        self.y = max(0, self.y + self.height/2)
                    if direction is 4:
                        self.x = max(0, self.x + self.width/2)
                    if direction is 6:
                        self.x = min(self.background.w, self.x - self.width/2)
                    if direction is 1:
                        self.x = max(0, self.x + self.width/2)
                        self.y = max(0, self.y + self.height/2)
                    if direction is 3:
                        self.x = min(self.background.w, self.x - self.width/2)
                        self.y = max(0, self.y + self.height/2)
                    if direction is 7:
                        self.x = max(0, self.x + self.width/2)
                        self.y = min(self.background.h, self.y - self.height/2)
                    if direction is 9:
                        self.x = min(self.background.w, self.x - self.width)
                        self.y = min(self.background.h, self.y - self.height)

    def hit_by_str(self, damage):
        if self.invincibility is False:
            hit_damage = max(damage - self.DEF, 1)  # 물리 방어력에 따른 들어오는 최종 데미지 연산식
            self.HP = self.HP - hit_damage
        print('대상의 남은 HP %d ' % self.HP)

    def hit_by_mag(self, dmg):
        if self.invincibility is False:
            hit_damage = max(dmg - self.MR, 1)  # 마법 저향력에 따른 들어오는 최종 데미지 연산식
            self.HP = self.HP - hit_damage
        print('대상의 남은 HP %d ' % self.HP)

    def hp_heal(self, heal):
        self.HP = min(self.HP + heal, self.MAX_HP)        # 힐량 효과만큼 회복

    def get_bb(self):
        return self.x - self.width / 2, self.y - self.height / 2, self.x + self.width / 2, self.y + self.height / 2

    def draw_bb(self):
        draw_rectangle(self.get_bb()[0] - self.background.window_left,
                       self.get_bb()[1] - self.background.window_bottom,
                       self.get_bb()[2] - self.background.window_left,
                       self.get_bb()[3] - self.background.window_bottom)


class BaseUnit(BaseObject):
    def __init__(self, hp, max_hp, mp, max_mp, stamina, max_stamina,
                 strength, defense, magic, magic_resist, move_speed, atk_speed):
        super(BaseUnit, self).__init__(hp, max_hp, defense, magic_resist, move_speed)
        self.frame = 0      # 애니메이션을 출력하기 위한 프레임변수
        self.MP = mp                    # 현재 MP, 마법 스킬을 사용하기 위한 자원
        self.MAX_MP = max_mp            # 최대 MP
        self.STAMINA = stamina          # 현재 SP, 물리 스킬을 사용하기 위한 자원
        self.MAX_STAMINA = max_stamina  # 최대 SP, 물리 스킬을 사용하기 위한 자원
        self.STR = strength             # 물리 공격력
        self.INT = magic                # 마법 공격력
        self.ATK_SPEED = atk_speed      # 공격속도

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

    def show_stat(self):
        print('이름: {}'.format(self.name))
        print('체력: {}'.format(self.HP), ' / {}'.format(self.MAX_HP))
        print('마력: {}'.format(self.MP), ' / {}'.format(self.MAX_MP))
        print('기력: {}'.format(self.STAMINA), ' / {}'.format(self.MAX_STAMINA))
        print('물리 공격력: {}'.format(self.STR))
        print('마법 공격력: {}'.format(self.INT))
        print('물리 방어력: {}'.format(self.DEF))
        print('마법 저항력: {}'.format(self.MR))

    def mp_heal(self, heal):
        self.MP = min(self.MP + heal, self.MAX_MP)

    def sp_heal(self, heal):
        self.STAMINA = min(self.STAMINA + heal, self.MAX_STAMINA)

    def get_hbs(self, point_x, point_y, hit_size):
        return point_x - (hit_size / 2) - self.background.window_left, \
               point_y - (hit_size / 2) - self.background.window_bottom, \
               point_x + (hit_size / 2) - self.background.window_left, \
               point_y + (hit_size / 2) - self.background.window_bottom

    def get_hbr(self, point_x, point_y, hit_size_x, hit_size_y):
        return point_x - (hit_size_x / 2) - self.background.window_left, \
               point_y - (hit_size_y / 2) - self.background.window_bottom, \
               point_x + (hit_size_x / 2) - self.background.window_left, \
               point_y + (hit_size_y / 2) - self.background.window_bottom

    def draw_hbs(self, point_x, point_y, hit_size):
        draw_rectangle(*self.get_hbs(point_x, point_y, hit_size))

    def draw_hbr(self, point_x, point_y, hit_size_x, hit_size_y):
        draw_rectangle(*self.get_hbr(point_x, point_y, hit_size_x, hit_size_y))


class BaseZone:
    def __init__(self, zone_data, base_height):
        self.width, self.height = zone_data['width'], zone_data['height']
        self.x, self.y = zone_data['x'] + self.width / 2, base_height - (zone_data['y'] + self.height / 2)

        self.background = None

    def set_background(self, background):
        self.background = background

    def get_bb(self):
        return self.x - self.width / 2, self.y - self.height / 2, self.x + self.width / 2, self.y + self.height / 2

    def draw_bb(self):
        draw_rectangle(self.get_bb()[0] - self.background.window_left,
                       self.get_bb()[1] - self.background.window_bottom,
                       self.get_bb()[2] - self.background.window_left,
                       self.get_bb()[3] - self.background.window_bottom)


class NonDataBaseZone:
    def __init__(self, x, y, w, h):
        self.x, self.y = x, y
        self.width = w
        self.height = h
        self.background = None

    def set_background(self, background):
        self.background = background

    def get_bb(self):
        return self.x - self.width / 2, self.y - self.height / 2, self.x + self.width / 2, self.y + self.height / 2

    def draw_bb(self):
        draw_rectangle(self.get_bb()[0] - self.background.window_left,
                       self.get_bb()[1] - self.background.window_bottom,
                       self.get_bb()[2] - self.background.window_left,
                       self.get_bb()[3] - self.background.window_bottom)


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


if __name__ == '__main__':
    print("This is Wrong Playing.\n")