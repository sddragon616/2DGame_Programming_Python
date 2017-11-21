from pico2d import *


class BaseObject:
    def __init__(self, hp, max_hp, defense, magic_resist, move_speed):
        self.name = self.__class__.__name__     # 현재 클래스의 이름
        self.image = 'Test_img.png'             # 객체의 이미지 초기화
        self.x, self.y = 0, 0                   # 객체의 좌표값 초기화
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

    def hit_by_str(self, dmg):
        hit = dmg - self.DEF  # 물리 방어력에 따른 들어오는 최종 데미지 연산식
        self.HP = self.HP - hit

    def hit_by_mag(self, dmg):
        hit = dmg - self.MR  # 마법 저향력에 따른 들어오는 최종 데미지 연산식
        self.HP = self.HP - hit

    def hp_heal(self, heal):
        if self.HP + heal < self.MAX_HP:    # 힐량 결과가 최대 체력보다 적다면
            self.HP = self.HP + heal        # 힐량 효과만큼 회복
        else:
            self.HP = self.MAX_HP           # 최대 체력을 넘어서는 회복 불가

    def get_bb(self):
        return self.x - 50, self.y - 50, self.x + 50, self.y + 50

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
        if self.MP + heal < self.MAX_MP:    # 힐량 결과가 최대 마력보다 적다면
            self.MP = self.MP + heal        # 힐량 효과만큼 회복
        else:
            self.MP = self.MAX_MP           # 최대 마력을 넘어서는 회복 불가

    def sp_heal(self, heal):
        if self.STAMINA + heal < self.MAX_STAMINA:    # 힐량 결과가 최대 기력보다 적다면
            self.STAMINA = self.STAMINA + heal        # 힐량 효과만큼 회복
        else:
            self.STAMINA = self.MAX_STAMINA           # 최대 기력을 넘어서는 회복 불가

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