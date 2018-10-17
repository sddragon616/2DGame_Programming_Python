from pico2d import *


Korean_font = None
English_font = []
UI_font = None

SwordMan = None
Warrior = None
Archer = None
Witch = None

fly = None
crab = None
skull_golem = None
spear = None
slasher = None

stone_shoes = None

UI_bar = None
light_quick_slot = None
dark_quick_slot = None

death_sound = None


def upload_data():
    global SwordMan, Warrior, Archer, Witch
    global fly, crab, skull_golem, spear, slasher
    global stone_shoes
    global UI_bar, light_quick_slot, dark_quick_slot
    global Korean_font, English_font, UI_font
    global death_sound

    fly = MonsterResourceData()
    crab = MonsterResourceData()
    skull_golem = MonsterResourceData()
    spear = MonsterResourceData()
    slasher = MonsterResourceData()

    UI_bar = BaseResourceData()
    light_quick_slot = BaseResourceData()
    dark_quick_slot = BaseResourceData()

    if UI_bar.image is None:
        UI_bar.image = load_image('Resource_Image\\User_Interface\\Gauge_bar.png')

    if light_quick_slot.image is None:
        light_quick_slot.image = load_image('Resource_Image\\User_Interface\\QuickSlotLight_by_JHL.png')
    if dark_quick_slot.image is None:
        dark_quick_slot.image = load_image('Resource_Image\\User_Interface\\QuickSlotDark_by_JHL.png')

    UI_font = load_font('Resource_Font\\Cornerstone.ttf', 15)
    English_font.append(UI_font)
    if Korean_font is None:
        Korean_font = load_font('Resource_Font\\DungGeunMo.otf', 25)

    if death_sound is None:
        death_sound = load_wav('Resource_Sound\\Effect_Sound\\Destroy.wav')
        death_sound.set_volume(64)

    # image pre load
    if fly.image is None:
        fly.image = load_image('Resource_Image\\Monster001_fly.png')
    if crab.image is None:
        crab.image = load_image('Resource_Image\\Monster002_crab.png')
    if skull_golem.image is None:
        skull_golem.image = load_image('Resource_Image\\Monster003_SkullGolem.png')
    if spear.image is None:
        spear.image = load_image('Resource_Image\\Monster004_Spear.png')
    if slasher.image is None:
        slasher.image = load_image('Resource_Image\\Monster005_Slasher.png')

    # wav sound pre load
    if fly.hit_sound is None:
        fly.hit_sound = load_wav('Resource_Sound\\Effect_Sound\\Damage1.wav')
        fly.hit_sound.set_volume(64)
    if crab.hit_sound is None:
        crab.hit_sound = load_wav('Resource_Sound\\Effect_Sound\\Slash12.wav')
        crab.hit_sound.set_volume(64)
    if skull_golem.hit_sound is None:
        skull_golem.hit_sound = load_wav('Resource_Sound\\Effect_Sound\\Slash11.wav')
        skull_golem.hit_sound.set_volume(64)
    if spear.hit_sound is None:
        spear.hit_sound = load_wav('Resource_Sound\\Effect_Sound\\Slash11.wav')
        spear.hit_sound.set_volume(64)
    if slasher.hit_sound is None:
        slasher.hit_sound = load_wav('Resource_Sound\\Effect_Sound\\Slash10.wav')
        slasher.hit_sound.set_volume(128)


class BaseResourceData():
    def __init__(self):
        self.image = None


class PlayerResourceData(BaseResourceData):
    def __init__(self):
        super(MonsterResourceData, self).__init__()
        self.attack_sound = None
        self.Level_up_sound = None


class MonsterResourceData(BaseResourceData):
    def __init__(self):
        super(MonsterResourceData, self).__init__()
        self.hit_sound = None


class Button:
    def __init__(self, idle_image, on_image, push_image):
        self.x, self.y = 512, 275
        self.width, self.height = 375, 100
        self.Trigger = 0
        self.Button_Image = None
        self.Button_On_Image = None
        self.Button_Pushed_Image = None
        if self.Button_Image is None:
            self.Button_Image = idle_image
        if self.Button_On_Image is None:
            self.Button_On_Image = on_image
        if self.Button_Pushed_Image is None:
            self.Button_Pushed_Image = push_image

    def get_bb(self):
        return self.x - int(self.width / 2), self.y - int(self.height / 2), \
               self.x + int(self.width / 2), self.y + int(self.height / 2)
