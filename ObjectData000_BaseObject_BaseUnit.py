from pico2d import *
import Project_SceneFrameWork

PIXEL_PER_METER = (32.0 / 1.0)  # 32pixel == 1m


class BaseObject:
    def __init__(self, hp, max_hp, defense, magic_resist, move_speed):
        self.name = self.__class__.__name__     # 현재 클래스의 이름
        self.image = load_image('Resource_Image\\Test_img.png')             # 객체의 이미지 초기화
        self.width, self.height = 0, 0          # 객체의 가로 길이, 세로 길이 초기화
        self.x, self.y = 2, 2                   # 객체의 좌표값 초기화
        self.HP = hp                            # 현재 체력
        self.MAX_HP = max_hp                    # 최대 체력
        self.DEF = defense                      # 물리 방어력
        self.MR = magic_resist                  # 마법 저향력
        self.MOVE_SPEED = move_speed            # 이동속도

    def show_stat(self):
        print('이름: {}'.format(self.name))
        print('체력: {}'.format(self.HP), ' / {}'.format(self.MAX_HP))
        print('물리 방어력: {}'.format(self.DEF))
        print('마법 저항력: {}'.format(self.MR))

    def draw(self):
        self.image.draw(self.x, self.y)

    def death(self):
        if self.HP <= 0:
            self.image = load_image("Resource_Image\\Test_img.png")
            return True
        else:
            return False

    def knock_back(self):
        if self.dir is 2:
            self.y = min(Project_SceneFrameWork.Window_H, self.y + self.height)
        if self.dir is 8:
            self.y = max(0, self.y - self.height)
        elif self.dir is 6:
            self.x = max(0, self.x - self.width)
        elif self.dir is 4:
            self.x = min(Project_SceneFrameWork.Window_W, self.x + self.width)
        elif self.dir is 9:
            self.x = max(0, self.x - self.width)
            self.y = max(0, self.y - self.height)
        elif self.dir is 7:
            self.x = min(Project_SceneFrameWork.Window_W, self.x + self.width)
            self.y = max(0, self.y - self.height)
        elif self.dir is 3:
            self.x = max(0, self.x - self.width)
            self.y = min(Project_SceneFrameWork.Window_H, self.y + self.height)
        elif self.dir is 1:
            self.x = min(Project_SceneFrameWork.Window_W, self.x + self.width)
            self.y = min(Project_SceneFrameWork.Window_H, self.y + self.height)

    def hit_by_str(self, damage):
        hit_damage = max(damage - self.DEF, 1)  # 물리 방어력에 따른 들어오는 최종 데미지 연산식
        self.HP = self.HP - hit_damage
        print('대상의 남은 HP %d ' % self.HP)

    def hit_by_mag(self, dmg):
        hit = max(dmg - self.MR, 1)  # 마법 저향력에 따른 들어오는 최종 데미지 연산식
        self.HP = self.HP - hit

    def hp_heal(self, heal):
        self.HP = min(self.HP + heal, self.MAX_HP)        # 힐량 효과만큼 회복

    def get_bb(self):
        return self.x - self.width / 2, self.y - self.height / 2, self.x + self.width / 2, self.y + self.height / 2

    def draw_bb(self):
        draw_rectangle(*self.get_bb())


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
        return point_x - (hit_size / 2), point_y - (hit_size / 2), point_x + (hit_size / 2), point_y + (hit_size / 2)

    def get_hbr(self, point_x, point_y, hit_size_x, hit_size_y):
        return point_x - (hit_size_x / 2), point_y - (hit_size_y / 2), point_x + (hit_size_x / 2), point_y + (hit_size_y / 2)

    def draw_hbs(self, point_x, point_y, hit_size):
        draw_rectangle(*self.get_hbs(point_x, point_y, hit_size))

    def draw_hbr(self, point_x, point_y, hit_size_x, hit_size_y):
        draw_rectangle(*self.get_hbr(point_x, point_y, hit_size_x, hit_size_y))


if __name__ == '__main__':
    print("This is Wrong Playing.\n")