import Project_SceneFrameWork
from pico2d import *
import os
import Scene001_Title

name = "LogoScene"
image = None
logo_time = 0.0




def enter():
    global image
    open_canvas(Project_SceneFrameWork.Window_W, Project_SceneFrameWork.Window_H)
    hide_lattice()
    image = load_image('Resource_Image\\GoldDragon_Logo_1024x773-by_solstice_arctic_luna-d6yrudl.png')


def exit():
    global image
    del image
    close_canvas()


def update():
    global logo_time
    if logo_time > 1.0:
        logo_time = 0
        Project_SceneFrameWork.scene_push(Scene001_Title)
    delay(0.01)
    logo_time += 0.01


def draw():
    global image
    clear_canvas()
    image.draw(Project_SceneFrameWork.Window_W / 2, Project_SceneFrameWork.Window_H / 2)
    update_canvas()


def handle_events():
    events = get_events()
    pass


def pause(): pass


def resume(): pass
