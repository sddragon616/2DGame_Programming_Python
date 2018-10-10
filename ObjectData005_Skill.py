from pico2d import *

PIXEL_PER_METER = (32.0 / 1.0)  # 32pixel == 1m


class Skill:
    def __init__(self):
        self.Level = 0
        self.use_hp = 0
        self.use_mp = 0
        self.use_sp = 0
        self.flag = False

        self.skill_frame_time = 0
        self.start_dir = 0
        self.skill_image = None
        self.background = None
        self.attack_sound = None

        self.attack_motion = 0
        self.frame = 0
        self.before_frame = 0

        # 프레임 타임 애니메이션 관련 변수들 정의
        self.total_frames_run = 0.0
        self.total_frames_atk = 0.0
        self.life_time = 0.0

        self.MOVE_SPEED = 22.2
        self.ATK_SPEED = 1.0
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

    def update(self, frame_time):
        pass

    def draw(self):
        pass

    def get_hb(self):
        return self.x - self.size / 2, self.y - self.size / 2, self.x + self.size / 2, self.y + self.size / 2

    def get_bb(self):
        return self.get_hb()

    def draw_hb(self):
        draw_rectangle(self.get_hb()[0] - self.background.window_left,
                       self.get_hb()[1] - self.background.window_bottom,
                       self.get_hb()[2] - self.background.window_left,
                       self.get_hb()[3] - self.background.window_bottom)

    def set_background(self, background):
        self.background = background


class DirectionRangeSkill(Skill):
    def __init__(self):
        super(DirectionRangeSkill, self).__init__()
        self.x, self.y = 0, 0
        self.rad = 0.0
        self.size = 0
        self.distance = 0


class CircleRangeSkill(Skill):
    def __init__(self):
        super(CircleRangeSkill, self).__init__()
        self.x, self.y = 0, 0
        self.size = 0
        self.distance = 0


class LineAssaultSkill(Skill):
    pass


class TyphoonAttack(CircleRangeSkill):
    def __init__(self):
        super(TyphoonAttack, self).__init__()
        if self.attack_sound is None:
            self.attack_sound = load_wav('Resource_Sound\\Effect_Sound\\Slash12.wav')
            self.attack_sound.set_volume(64)
        self.use_mp = 0
        self.use_sp = 10

    def update(self, frame_time, others):
        self.size = min(self.Level, 9) * 4 + 128
        self.total_frames_atk += self.FRAMES_PER_ACTION_atk * self.ACTION_PER_TIME_atk * frame_time * 10
        self.frame = int(self.total_frames_atk) % 9
        if self.frame - self.before_frame == 1:
            if self.attack_sound is not None:
                self.attack_sound.play()
            if self.attack_motion == 1:
                self.attack_motion = 2
            elif self.attack_motion == 2:
                self.attack_motion = 3
            elif self.attack_motion == 3:
                self.attack_motion = 6
            elif self.attack_motion == 6:
                self.attack_motion = 9
            elif self.attack_motion == 9:
                self.attack_motion = 8
            elif self.attack_motion == 8:
                self.attack_motion = 7
            elif self.attack_motion == 7:
                self.attack_motion = 4
            elif self.attack_motion == 4:
                self.attack_motion = 1
        self.before_frame = self.frame
        if self.frame >= 8:
            self.total_frames_atk = 0.0


class AirSplit(DirectionRangeSkill):
    def __init__(self):
        super(AirSplit, self).__init__()
        if self.skill_image is None:
            self.skill_image = load_image("Resource_Image\\Effects_000.png")

        self.use_mp = 3
        self.use_sp = 1
        self.distance = 1.0

    def update(self, frame_time, others):
        self.size = min(self.Level, 9) * 4 + 32
        if self.flag is True:
            air_splitter_time_limit = 1.0
            self.skill_frame_time += ((1.0 / self.Level)
                                      * self.FRAMES_PER_ACTION_atk * self.ACTION_PER_TIME_atk * frame_time)
            if self.skill_frame_time > (self.frame + 1) * air_splitter_time_limit / 4.0:
                self.frame += 1
            if self.start_dir is 2:
                self.rad = 3 * math.pi / 2.0
                self.y -= (self.distance * 8)
            elif self.start_dir is 8:
                self.rad = math.pi / 2.0
                self.y += (self.distance * 8)
            elif self.start_dir is 4:
                self.rad = math.pi
                self.x -= (self.distance * 8)
            elif self.start_dir is 6:
                self.rad = 0.0
                self.x += (self.distance * 8)
            elif self.start_dir is 1:
                self.rad = 5 * math.pi / 4.0
                self.x -= (self.distance * 8)
                self.y -= (self.distance * 8)
            elif self.start_dir is 3:
                self.rad = 7 * math.pi / 4.0
                self.x += (self.distance * 8)
                self.y -= (self.distance * 8)
            elif self.start_dir is 7:
                self.rad = 3 * math.pi / 4.0
                self.x -= (self.distance * 8)
                self.y += (self.distance * 8)
            elif self.start_dir is 9:
                self.rad = 1 * math.pi / 4.0
                self.x += (self.distance * 8)
                self.y += (self.distance * 8)
            if self.skill_frame_time > air_splitter_time_limit:
                self.x, self.y = -100, -100
                self.skill_frame_time = 0
                self.frame = 0
                self.flag = False

    def draw(self):
        self.skill_image.clip_composite_draw((self.frame + 2) * 32, 14 * 32, 32, 32,
                                             self.rad, 'v',
                                             self.x - self.background.window_left,
                                             self.y - self.background.window_bottom,
                                             self.size, self.size)


