from pico2d import *
from random import *
import Project_SceneFrameWork
import Scene003_BaseBattletScene
import Scene012_Stage02
import ObjectData000_BaseObject_BaseUnit
import ObjectData003_Monster
import Scene005_GameClear
import Mapdata
import Resource_Manager as rssmgr


name = "Boss_Stage"
slashers = []
Bosses = []
BGM = None
background = None
Cannot_Move_Zone = []
collide_zone = []
size_width = 0
size_height = 0
BeforeStageZone = None
Before_Loading_Trigger = False


class Boss_Bgm:
    def __init__(self):
        self.bgm = load_music('Resource_Sound\\BGM\\Boss.mp3')
        self.bgm.set_volume(64)
        self.bgm.repeat_play()


def enter():
    global slashers, Bosses
    global BGM
    global background
    global Cannot_Move_Zone, BeforeStageZone
    global size_width
    global size_height
    size_width = get_canvas_width()
    size_height = get_canvas_height()
    Scene003_BaseBattletScene.enter()
    Scene003_BaseBattletScene.user.x = 768
    Scene003_BaseBattletScene.user.y = 96
    background = Mapdata.BackGround_Tilemap('Map\\Mapdata\\BossMap.json',
                                            'Map\\Mapdata\\BossMap_Ground.png')

    background.set_center_object(Scene003_BaseBattletScene.user)
    Scene003_BaseBattletScene.user.set_background(background)

    BeforeStageZone = ObjectData000_BaseObject_BaseUnit.DataNoneBaseZone(768, 8, 128, 16)

    Cannot_Move_Zone = [ObjectData000_BaseObject_BaseUnit.BaseZone(
        Mapdata.load_tile_map('Map\\Mapdata\\BossMap.json').layers[2]['objects'][i], 4800)
        for i in range(len(Mapdata.load_tile_map('Map\\Mapdata\\BossMap.json').layers[2]['objects']))]

    slashers = [ObjectData003_Monster.Slasher(
        Mapdata.load_tile_map('Map\\Mapdata\\BossMap.json').layers[3]['objects'][i], 4800)
        for i in range(len(Mapdata.load_tile_map('Map\\Mapdata\\BossMap.json').layers[3]['objects']))]

    Bosses = [ObjectData003_Monster.GigantSlasher(
        Mapdata.load_tile_map('Map\\Mapdata\\BossMap.json').layers[4]['objects'][i], 4800)
        for i in range(1)]

    for slasher in slashers:
        slasher.set_background(background)

    for gigantslasher in Bosses:
        gigantslasher.x = gigantslasher.x + 10
        gigantslasher.y = gigantslasher.y - 50
        gigantslasher.set_background(background)

    for Zone in Cannot_Move_Zone:
        Zone.set_background(background)

    if BGM is None:
        BGM = Boss_Bgm()


def exit():
    global BGM
    BGM = None


def handle_events(frame_time):
    Scene003_BaseBattletScene.handle_events(frame_time)


def draw(frame_time):
    clear_canvas()
    draw_scene(frame_time)
    update_canvas()


def draw_scene(frame_time):
    global size_width
    global size_height
    global Bosses, slashers
    background.draw()
    Scene003_BaseBattletScene.draw_scene(frame_time)

    for slasher in slashers:
        if abs(Scene003_BaseBattletScene.user.x - slasher.x) < size_width and \
                        abs(Scene003_BaseBattletScene.user.y - slasher.y) < size_height:
            slasher.draw()
        if Scene003_BaseBattletScene.user.box_draw_Trigger:
            slasher.draw_bb()

    for Boss in Bosses:
        if abs(Scene003_BaseBattletScene.user.x - Boss.x) < size_width and \
                        abs(Scene003_BaseBattletScene.user.y - Boss.y) < size_height:
            Boss.draw()
        if Scene003_BaseBattletScene.user.box_draw_Trigger:
            Boss.draw_bb()
    for Zone in collide_zone:
        if Scene003_BaseBattletScene.user.box_draw_Trigger:
            Zone.draw_bb()

    if Before_Loading_Trigger is True:
        rssmgr.Korean_font.draw(125, Project_SceneFrameWork.Window_H / 2,
                                '이전 스테이지를 로딩중입니다, 조금 기다려 주세요!', (225, 0, 0))


def update(frame_time):
    global collide_zone
    global size_width
    global size_height
    global Bosses, slashers
    global Before_Loading_Trigger
    global BeforeStageZone

    background.update(frame_time)
    collide_zone = []
    for Zone in Cannot_Move_Zone:
        if abs(Scene003_BaseBattletScene.user.x - Zone.x) < size_width and \
                        abs(Scene003_BaseBattletScene.user.y - Zone.y) < size_height:
            collide_zone.append(Zone)
    Scene003_BaseBattletScene.update(frame_time, slashers, collide_zone)
    Scene003_BaseBattletScene.update(frame_time, Bosses, collide_zone)

    if collide(Scene003_BaseBattletScene.user, BeforeStageZone):
        Before_Loading_Trigger = True
        draw(frame_time)
        Project_SceneFrameWork.scene_change(Scene012_Stage02)
        Scene003_BaseBattletScene.user.state = 0
        Scene003_BaseBattletScene.user.x = 2350
        Scene003_BaseBattletScene.user.y = 3057
        Before_Loading_Trigger = False

    if not Bosses:
        Project_SceneFrameWork.scene_push(Scene005_GameClear)
        Scene003_BaseBattletScene.user = None


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