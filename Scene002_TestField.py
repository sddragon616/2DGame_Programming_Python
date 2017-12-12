from pico2d import *
import Project_SceneFrameWork
import Scene003_Interface
import ObjectData002_SwordMan
import ObjectData003_Monster
import MapData
from random import *

name = "TestField"
image = None
user = None
flies = []
TestBGM = None
background = None


class Testbgm:
    def __init__(self):
        self.bgm = load_music('Resource_Sound\\BGM\\Field 01.mp3')
        self.bgm.set_volume(64)
        self.bgm.repeat_play()


def enter():
    global image
    global user
    global flies
    global TestBGM
    global background
    user = ObjectData002_SwordMan.SwordMan(2000, 32)
    flies = [ObjectData003_Monster.Fly(randint(0, 4000), randint(0, 3200)) for index in range(100)]
    background = MapData.BackGround_Tilemap()
    background.set_center_object(user)
    user.set_background(background)
    for fly in flies:
        fly.set_background(background)
    if image is None:
        image = load_image('Resource_Image\\TestField0_1024x768.png')
    if TestBGM is None:
        TestBGM = Testbgm()


def exit():
    global image
    global user
    global flies
    global TestBGM
    del user
    del image
    del flies
    del TestBGM


def handle_events(frame_time):
    global user
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            Project_SceneFrameWork.quit()
        else:
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
                Project_SceneFrameWork.quit()
            else:
                user.handle_events(event)
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_u):
                Project_SceneFrameWork.scene_push(Scene003_Interface)


def draw(frame_time):
    clear_canvas()
    draw_scene(frame_time)
    update_canvas()


def draw_scene(frame_time):
    background.draw()
    # image.draw(Project_SceneFrameWork.Window_W / 2, Project_SceneFrameWork.Window_H / 2)
    user.draw()
    if user.box_draw:
        user.draw_bb()
    for fly in flies:
        fly.draw()
        if user.box_draw:
            fly.draw_bb()


def update(frame_time):
    user.update(frame_time)

    background.update(frame_time)
    for fly in flies:
        fly.update(frame_time, user)

        if collide(user, fly):
            user.hit_by_str(fly.STR, fly.dir)
        if user.melee_atk_collide(fly):
            fly.hit_by_str(user.STR, user.dir)
        if fly.exp_pay:             # 몬스터가 쓰러져서 경험치를 지급했는가?
            flies.remove(fly)


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
