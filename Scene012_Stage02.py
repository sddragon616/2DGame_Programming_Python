from pico2d import *
from random import *
import Project_SceneFrameWork
import Scene003_BaseBattletScene
import ObjectData000_BaseObject_BaseUnit
import ObjectData003_Monster
import Scene013_Stage03
import Scene014_Boss_Stage
import Mapdata


name = "Stage_02"
crabs = []
golems = []
monsters = []
BGM = None
background = None
StageMoveZone = None
Cannot_Move_Zone = []
collide_zone = []
size_width = 0
size_height = 0


class Stage2_Bgm:
    def __init__(self):
        self.bgm = load_music('Resource_Sound\\BGM\\Field 02.mp3')
        self.bgm.set_volume(64)
        self.bgm.repeat_play()


def enter():
    global crabs
    global golems
    global monsters
    global BGM
    global background
    global Cannot_Move_Zone
    global size_width
    global size_height
    global StageMoveZone
    size_width = get_canvas_width()
    size_height = get_canvas_height()
    Scene003_BaseBattletScene.enter()
    Scene003_BaseBattletScene.user.x = 1550
    Scene003_BaseBattletScene.user.y = 60
    background = Mapdata.BackGround_Tilemap('Map\\Mapdata\\High_Field.json',
                                            'Map\\Mapdata\\High_Field_Ground.png')
    Cannot_Move_Zone = [ObjectData000_BaseObject_BaseUnit.BaseZone(
        Mapdata.load_tile_map('Map\\Mapdata\\High_Field.json').layers[2]['objects'][i], 1600) for i in range(40)]

    StageMoveZone = ObjectData000_BaseObject_BaseUnit.KeyZone(785, 1530, 90, 40)

    background.set_center_object(Scene003_BaseBattletScene.user)
    Scene003_BaseBattletScene.user.set_background(background)

    for Zone in Cannot_Move_Zone:
        Zone.set_background(background)

    crabs = [ObjectData003_Monster.Crab(randint(0, 1500), randint(0, 1600)) for index in range(50)]
    for crab in crabs:
        crab.set_background(background)
    golems = [ObjectData003_Monster.Skull_Golem(randint(0, 1500), randint(0, 1600)) for index in range(25)]
    for golem in golems:
        golem.set_background(background)

    monsters = crabs + golems
    if BGM is None:
        BGM = Stage2_Bgm()


def exit():
    global monsters
    global BGM
    del monsters
    del BGM


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
    background.draw()
    Scene003_BaseBattletScene.draw_scene(frame_time)
    for monster in monsters:
        if abs(Scene003_BaseBattletScene.user.x - monster.x) < size_width and \
                        abs(Scene003_BaseBattletScene.user.y - monster.y) < size_height:
            monster.draw()
        if Scene003_BaseBattletScene.user.box_draw_Trigger:
            monster.draw_bb()
    for Zone in collide_zone:
        if Scene003_BaseBattletScene.user.box_draw_Trigger:
            Zone.draw_bb()


def update(frame_time):
    global collide_zone
    global size_width
    global size_height
    global monsters
    global StageMoveZone
    background.update(frame_time)
    collide_zone = []
    for Zone in Cannot_Move_Zone:
        if abs(Scene003_BaseBattletScene.user.x - Zone.x) < size_width and \
                        abs(Scene003_BaseBattletScene.user.y - Zone.y) < size_height:
            collide_zone.append(Zone)
    Scene003_BaseBattletScene.update(frame_time, monsters, collide_zone)

    if collide(Scene003_BaseBattletScene.user, StageMoveZone):
        Project_SceneFrameWork.scene_push(Scene014_Boss_Stage)
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