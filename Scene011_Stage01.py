from pico2d import *
import Project_SceneFrameWork
import Scene003_BaseBattletScene
import ObjectData000_BaseObject_BaseUnit
import ObjectData003_Monster
import Scene012_Stage02
import Mapdata
import Resource_Manager as rssmgr


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
Message_font = None
Cannot_Move_Zone = []
collide_zone = []
size_width = 0
size_height = 0
Loading_Trigger = False


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
    global Message_font
    global Map_Data

    Scene003_BaseBattletScene.enter()
    KeyEvent = load_wav('Resource_Sound\\Effect_Sound\\Drinking.wav')
    KeyEvent.set_volume(64)
    size_width = get_canvas_width()
    size_height = get_canvas_height()

    # 돌 신발
    KeyZone = ObjectData000_BaseObject_BaseUnit.DataNoneBaseZone(3450, 2400 - 350, 32, 32)

    # 다음 스테이지로 이동하는 영역
    StageMoveZone = ObjectData000_BaseObject_BaseUnit.DataNoneBaseZone(10, 550, 20, 100)

    # 돌 신을 신고 뛰어보자 폴짝
    JumpZone = ObjectData000_BaseObject_BaseUnit.DataNoneBaseZone(905, 1550, 295, 65)

    if KeyItem is None:
        KeyItem = load_image('Resource_Image\\stone_shoes.png')

    background = Mapdata.BackGround_Tilemap('Map\\Mapdata\\Forest_Shining.json',
                                            'Map\\Mapdata\\Forest_Shining_Ground.png')

    # 이동불가 영역
    Cannot_Move_Zone = [ObjectData000_BaseObject_BaseUnit.BaseZone(
        background.tile_map.layers[3]['objects'][i], 2400)
        for i in range(len(background.tile_map.layers[3]['objects']))]

    flies = [ObjectData003_Monster.Fly(
        background.tile_map.layers[2]['objects'][index], 2400)
        for index in range(len(background.tile_map.layers[2]['objects']))]

    KeyZone.set_background(background)
    StageMoveZone.set_background(background)
    JumpZone.set_background(background)

    background.set_center_object(Scene003_BaseBattletScene.user)
    Scene003_BaseBattletScene.user.set_background(background)

    for Zone in Cannot_Move_Zone:
        Zone.set_background(background)

    for fly in flies:
        fly.set_background(background)

    if BGM is None:
        BGM = Stage1_Bgm()
    else:
        BGM.bgm.repeat_play()


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
    flies.clear()
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
    global Loading_Trigger
    background.draw()
    for fly in flies:
        if abs(Scene003_BaseBattletScene.user.x - fly.x) < size_width and \
                        abs(Scene003_BaseBattletScene.user.y - fly.y) < size_height:
            fly.draw()
        else:
            fly.contact = False
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
    elif collide(Scene003_BaseBattletScene.user, KeyZone):
        rssmgr.Korean_font.draw(150, Project_SceneFrameWork.Window_H - 100,
                                '튼튼한 돌 신발을 주웠다. 이걸 신으면 높은 곳에서 떨어져도 괜찮을 것 같다.', (255, 255, 255))
        rssmgr.Korean_font.draw(10, Project_SceneFrameWork.Window_H - 150,
                                '마물이 먹다가 뱉은 것 같다. 전 주인은 돌 신발만 남기고 뱃속에서 소화되었겠지...', (255, 255, 255))

    if collide(Scene003_BaseBattletScene.user, JumpZone):
        if KeyTrigger is True and Scene003_BaseBattletScene.user.dir is 2:
            Scene003_BaseBattletScene.user.y -= 250
            Scene003_BaseBattletScene.user.dir = 2
        else:
            rssmgr.Korean_font.draw(125, Project_SceneFrameWork.Window_H - 150,
                                    '높이가 높은 절벽이다. 떨어지면 발이 아플 것 같다...', (0, 0, 0))

    if Loading_Trigger is True:
        rssmgr.Korean_font.draw(125, Project_SceneFrameWork.Window_H / 2,
                                '다음 스테이지를 로딩중입니다, 조금 기다려 주세요!', (225, 0, 0))


def update(frame_time):
    global collide_zone
    global size_width
    global size_height
    global KeyZone
    global KeyTrigger
    global JumpZone
    global StageMoveZone
    global KeyEvent
    global Loading_Trigger
    background.update(frame_time)

    if collide(Scene003_BaseBattletScene.user, KeyZone):
        if KeyTrigger is False:
            KeyEvent.play()
            KeyTrigger = True

    if collide(Scene003_BaseBattletScene.user, JumpZone):
        if KeyTrigger is True and Scene003_BaseBattletScene.user.dir is 2:
            Scene003_BaseBattletScene.user.y -= 250
            Scene003_BaseBattletScene.user.dir = 2

    collide_zone = []
    for Zone in Cannot_Move_Zone:
        if abs(Scene003_BaseBattletScene.user.x - Zone.x) < size_width and \
                        abs(Scene003_BaseBattletScene.user.y - Zone.y) < size_height:
            collide_zone.append(Zone)
    Scene003_BaseBattletScene.update(frame_time, flies, collide_zone)

    if collide(Scene003_BaseBattletScene.user, StageMoveZone):
        Loading_Trigger = True
        draw(frame_time)
        Project_SceneFrameWork.scene_push(Scene012_Stage02)
        Loading_Trigger = False
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
