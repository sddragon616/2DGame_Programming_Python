from pico2d import *

import Project_SceneFrameWork
import Scene003_BaseBattletScene
import ObjectData000_BaseObject_BaseUnit
import ObjectData003_Monster
import Scene011_Stage01
import Scene013_Stage03
import Scene014_Boss_Stage
import Mapdata
import Resource_Manager as rssmgr


name = "Stage_02"
strong_flies = []
crabs = []
golems = []
mini_golems = []
gigant_crabs = []
spears = []
flying_spears = []
monsters = []
BGM = None
background = None
StageMoveZone = None
BeforeStageZone = None
Cannot_Move_Zone = []
collide_zone = []
size_width = 0
size_height = 0

Loading_Trigger = False
Before_Loading_Trigger = False


class Stage2_Bgm:
    def __init__(self):
        self.bgm = load_music('Resource_Sound\\BGM\\Field 02.mp3')
        self.bgm.set_volume(64)
        self.bgm.repeat_play()


def enter():
    global crabs
    global golems
    global strong_flies, mini_golems, gigant_crabs, spears, flying_spears
    global monsters
    global BGM
    global background
    global Cannot_Move_Zone
    global size_width
    global size_height
    global StageMoveZone
    global BeforeStageZone

    size_width = get_canvas_width()
    size_height = get_canvas_height()
    Scene003_BaseBattletScene.enter()
    Scene003_BaseBattletScene.user.x = 4700
    Scene003_BaseBattletScene.user.y = 544

    background = Mapdata.BackGround_Tilemap('Map\\Mapdata\\High_Field.json',
                                            'Map\\Mapdata\\High_Field_Ground.png')

    Cannot_Move_Zone = [ObjectData000_BaseObject_BaseUnit.BaseZone(
        background.tile_map.layers[2]['objects'][i], 3200)
        for i in range(len(background.tile_map.layers[2]['objects']))]

    # 다음 지역으로 이동할 영역
    StageMoveZone = ObjectData000_BaseObject_BaseUnit.DataNoneBaseZone(2350, 3136, 128, 80)
    BeforeStageZone = ObjectData000_BaseObject_BaseUnit.DataNoneBaseZone(4784, 544, 32, 96)

    # 유저 세팅
    background.set_center_object(Scene003_BaseBattletScene.user)
    Scene003_BaseBattletScene.user.set_background(background)

    for Zone in Cannot_Move_Zone:
        Zone.set_background(background)

    # 파리들 생성
    strong_flies = [ObjectData003_Monster.StrongFly(
        background.tile_map.layers[3]['objects'][index], 3200)
        for index in range(len(background.tile_map.layers[3]['objects']))]

    for strong_fly in strong_flies:
        strong_fly.set_background(background)

    # 게 생성
    crabs = [ObjectData003_Monster.Crab(
        background.tile_map.layers[4]['objects'][index], 3200)
        for index in range(len(background.tile_map.layers[4]['objects']))]
    for crab in crabs:
        crab.set_background(background)

    # 작은 골렘 생성
    mini_golems = [ObjectData003_Monster.Mini_Skull_Golem(
        background.tile_map.layers[5]['objects'][index], 3200)
        for index in range(len(background.tile_map.layers[5]['objects']))]
    for mini_golem in mini_golems:
        mini_golem.set_background(background)

    # 골렘 생성
    golems = [ObjectData003_Monster.Skull_Golem(
        background.tile_map.layers[6]['objects'][index], 3200)
        for index in range(len(background.tile_map.layers[6]['objects']))]
    for golem in golems:
        golem.set_background(background)

    # 거대 게 생성
    gigant_crabs = [ObjectData003_Monster.Gigant_Crab(
        background.tile_map.layers[7]['objects'][index], 3200)
        for index in range(len(background.tile_map.layers[7]['objects']))]
    for gigant_crab in gigant_crabs:
        gigant_crab.set_background(background)

    # 스피어 생성
    spears = [ObjectData003_Monster.Spear(
        background.tile_map.layers[8]['objects'][index], 3200)
        for index in range(len(background.tile_map.layers[8]['objects']))]
    for spear in spears:
        spear.set_background(background)

    # 비행형 스피어 생성
    flying_spears = [ObjectData003_Monster.FlyingSpear(
        background.tile_map.layers[9]['objects'][index], 3200)
        for index in range(len(background.tile_map.layers[9]['objects']))]
    for flying_spear in flying_spears:
        flying_spear.set_background(background)

    monsters = crabs + golems + strong_flies + mini_golems + gigant_crabs + spears + flying_spears

    if BGM is None:
        BGM = Stage2_Bgm()


def exit():
    global crabs, golems, strong_flies, mini_golems, gigant_crabs, spears, flying_spears, monsters
    global BGM
    crabs.clear()
    golems.clear()
    strong_flies.clear()
    mini_golems.clear()
    gigant_crabs.clear()
    spears.clear()
    flying_spears.clear()
    monsters.clear()
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
    global monsters
    global Loading_Trigger
    background.draw()
    for monster in monsters:
        if abs(Scene003_BaseBattletScene.user.x - monster.x) < size_width and \
                        abs(Scene003_BaseBattletScene.user.y - monster.y) < size_height:
            monster.draw()
        if Scene003_BaseBattletScene.user.box_draw_Trigger:
            monster.draw_bb()
    for Zone in collide_zone:
        if Scene003_BaseBattletScene.user.box_draw_Trigger:
            Zone.draw_bb()
    Scene003_BaseBattletScene.draw_scene(frame_time)
    if Loading_Trigger is True:
        rssmgr.Korean_font.draw(125, Project_SceneFrameWork.Window_H / 2,
                                '다음 스테이지를 로딩중입니다, 조금 기다려 주세요!', (225, 0, 0))

    if Before_Loading_Trigger is True:
        rssmgr.Korean_font.draw(125, Project_SceneFrameWork.Window_H / 2,
                                '이전 스테이지를 로딩중입니다, 조금 기다려 주세요!', (225, 0, 0))


def update(frame_time):
    global collide_zone
    global size_width
    global size_height
    global monsters
    global StageMoveZone, BeforeStageZone
    global Loading_Trigger, Before_Loading_Trigger
    background.update(frame_time)
    collide_zone = []
    for Zone in Cannot_Move_Zone:
        if abs(Scene003_BaseBattletScene.user.x - Zone.x) < size_width and \
                        abs(Scene003_BaseBattletScene.user.y - Zone.y) < size_height:
            collide_zone.append(Zone)
    Scene003_BaseBattletScene.update(frame_time, monsters, collide_zone)

    if collide(Scene003_BaseBattletScene.user, StageMoveZone):
        Loading_Trigger = True
        draw(frame_time)
        Project_SceneFrameWork.scene_push(Scene014_Boss_Stage)
        Scene003_BaseBattletScene.user.state = 0
        Scene003_BaseBattletScene.user.x = 768
        Scene003_BaseBattletScene.user.y = 96
        Loading_Trigger = False

    if collide(Scene003_BaseBattletScene.user, BeforeStageZone):
        Before_Loading_Trigger = True
        draw(frame_time)
        Project_SceneFrameWork.scene_change(Scene011_Stage01)
        Scene003_BaseBattletScene.user.state = 0
        Scene003_BaseBattletScene.user.x = 50
        Scene003_BaseBattletScene.user.y = 550
        Before_Loading_Trigger = False


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