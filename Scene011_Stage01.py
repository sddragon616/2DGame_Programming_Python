from pico2d import *
from random import *
import Project_SceneFrameWork
import Scene003_BaseBattletScene
import ObjectData003_Monster
import Mapdata


name = "TestField"
flies = []
BGM = None
background = None


class Stage1_Bgm:
    def __init__(self):
        self.bgm = load_music('Resource_Sound\\BGM\\Field 01.mp3')
        self.bgm.set_volume(64)
        self.bgm.repeat_play()


def enter():
    global flies
    global BGM
    global background
    Scene003_BaseBattletScene.enter()
    background = Mapdata.BackGround_Tilemap()
    background.set_center_object(Scene003_BaseBattletScene.user)
    Scene003_BaseBattletScene.user.set_background(background)
    flies = [ObjectData003_Monster.Fly(randint(0, 4000), randint(0, 3200)) for index in range(100)]
    for fly in flies:
        fly.set_background(background)
    if BGM is None:
        BGM = Stage1_Bgm()


def exit():
    global flies
    global BGM
    del flies
    del BGM


def handle_events(frame_time):
    Scene003_BaseBattletScene.handle_events(frame_time)


def draw(frame_time):
    clear_canvas()
    draw_scene(frame_time)
    update_canvas()


def draw_scene(frame_time):
    background.draw()
    Scene003_BaseBattletScene.draw_scene(frame_time)
    for fly in flies:
        fly.draw()
        if Scene003_BaseBattletScene.user.box_draw_Trigger:
            fly.draw_bb()


def update(frame_time):
    background.update(frame_time)
    Scene003_BaseBattletScene.update(frame_time, flies)


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
