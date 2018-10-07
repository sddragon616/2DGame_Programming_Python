from pico2d import *
from random import *
import Project_SceneFrameWork
import Scene003_BaseBattletScene
import ObjectData000_BaseObject_BaseUnit
import ObjectData003_Monster
import Scene012_Stage02
import Mapdata


name = "Stage_01"
flies = []
BGM = None
background = None
KeyZone = None
KeyEvent = None
KeyItem = None
KeyTrigger = False
StageMoveZone = None
JumpZone = None
Cannot_Move_Zone = []
collide_zone = []
size_width = 0
size_height = 0


class Stage1_Bgm:
    def __init__(self):
        self.bgm = load_music('Resource_Sound\\BGM\\Field 01.mp3')
        self.bgm.set_volume(64)
        self.bgm.repeat_play()


def enter():
    global flies
    global BGM
    global background
    global Cannot_Move_Zone
    global size_width
    global size_height
    global KeyZone
    global StageMoveZone
    global JumpZone
    global KeyEvent
    global KeyItem
    KeyEvent = load_wav('Resource_Sound\\Effect_Sound\\Drinking.wav')
    KeyEvent.set_volume(64)
    size_width = get_canvas_width()
    size_height = get_canvas_height()
    Scene003_BaseBattletScene.enter()
    KeyZone = ObjectData000_BaseObject_BaseUnit.NonDataBaseZone(3450, 2400 - 350, 32, 32)
    StageMoveZone = ObjectData000_BaseObject_BaseUnit.NonDataBaseZone(10, 550, 20, 100)
    JumpZone = ObjectData000_BaseObject_BaseUnit.NonDataBaseZone(925, 1550, 300, 100)
    if KeyItem is None:
        KeyItem = load_image('Resource_Image\\stone_shoes.png')
    background = Mapdata.BackGround_Tilemap('Map\\Mapdata\\Forest_Shining.json',
                                            'Map\\Mapdata\\Forest_Shining_Ground.png')
    Cannot_Move_Zone = [ObjectData000_BaseObject_BaseUnit.BaseZone(
        Mapdata.load_tile_map('Map\\Mapdata\\Forest_Shining.json').layers[3]['objects'][i], 2400) for i in range(199)]
    fly_image = load_image('Resource_Image\\Monster001_fly.png')
    flies = [ObjectData003_Monster.Fly(
        Mapdata.load_tile_map('Map\\Mapdata\\Forest_Shining.json').layers[2]['objects'][index], 2400)
        for index in range(65)]

    KeyZone.set_background(background)
    StageMoveZone.set_background(background)
    JumpZone.set_background(background)

    background.set_center_object(Scene003_BaseBattletScene.user)
    Scene003_BaseBattletScene.user.set_background(background)

    for Zone in Cannot_Move_Zone:
        Zone.set_background(background)

    for fly in flies:
        fly.set_background(background)
        fly.image = fly_image
        fly.MONSTER_HP_BAR = Scene003_BaseBattletScene.ui_bar_image
        fly.death_sound = Scene003_BaseBattletScene.death_sound

    if BGM is None:
        BGM = Stage1_Bgm()


def exit():
    global flies
    global BGM
    global background
    global Cannot_Move_Zone
    global size_width
    global size_height
    global KeyEvent
    global KeyItem
    global KeyTrigger
    flies = []
    BGM = None
    background = None
    KeyEvent = None
    KeyItem = None
    KeyTrigger = False
    Cannot_Move_Zone = []
    size_width = 0
    size_height = 0


def handle_events(frame_time):
    Scene003_BaseBattletScene.handle_events(frame_time)


def draw(frame_time):
    clear_canvas()
    draw_scene(frame_time)
    update_canvas()


def draw_scene(frame_time):
    global size_width
    global size_height
    global KeyZone
    global StageMoveZone
    global JumpZone
    global KeyItem
    global KeyTrigger
    background.draw()
    for fly in flies:
        if abs(Scene003_BaseBattletScene.user.x - fly.x) < size_width and \
                        abs(Scene003_BaseBattletScene.user.y - fly.y) < size_height:
            fly.draw()
        if Scene003_BaseBattletScene.user.box_draw_Trigger:
            fly.draw_bb()
    Scene003_BaseBattletScene.draw_scene(frame_time)
    if Scene003_BaseBattletScene.user.box_draw_Trigger:
        KeyZone.draw_bb()
        StageMoveZone.draw_bb()
        JumpZone.draw_bb()

    for Zone in collide_zone:
        if Scene003_BaseBattletScene.user.box_draw_Trigger:
            Zone.draw_bb()
    if KeyTrigger is False:
        if KeyItem is None:
            KeyItem = load_image('Resource_Image\\stone_shoes.png')
        KeyItem.draw(KeyZone.x - background.window_left, KeyZone.y - background.window_bottom)


def update(frame_time):
    global collide_zone
    global size_width
    global size_height
    global KeyZone
    global KeyTrigger
    global JumpZone
    global StageMoveZone
    global KeyEvent
    background.update(frame_time)
    if collide(Scene003_BaseBattletScene.user, KeyZone):
        if KeyTrigger is False:
            KeyEvent.play()
            KeyTrigger = True
    if collide(Scene003_BaseBattletScene.user, JumpZone):
        if KeyTrigger is True and Scene003_BaseBattletScene.user.dir is 2:
            Scene003_BaseBattletScene.user.y -= 350
            Scene003_BaseBattletScene.user.dir = 2

    collide_zone = []
    for Zone in Cannot_Move_Zone:
        if abs(Scene003_BaseBattletScene.user.x - Zone.x) < size_width and \
                        abs(Scene003_BaseBattletScene.user.y - Zone.y) < size_height:
            collide_zone.append(Zone)
    Scene003_BaseBattletScene.update(frame_time, flies, collide_zone)

    if collide(Scene003_BaseBattletScene.user, StageMoveZone):
        Project_SceneFrameWork.scene_push(Scene012_Stage02)
        Scene003_BaseBattletScene.user.state = 0


def pause(): pass


def resume(): pass


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
