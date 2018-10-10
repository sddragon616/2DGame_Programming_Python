import Project_SceneFrameWork
from pico2d import *

import Scene001_Title

name = "LogoScene"
image = None
logo_time = 0.0


def enter():
    global image
    open_canvas(Project_SceneFrameWork.Window_W, Project_SceneFrameWork.Window_H)
    caption = ('DungeonSlayer (' + str(Project_SceneFrameWork.Window_W) + 'x' + str(Project_SceneFrameWork.Window_H) +
               ')' + ' 1000.0 FPS').encode('UTF-8')
    SDL_SetWindowTitle(pico2d.window, caption)
    hide_lattice()
    image = load_image('Resource_Image\\GoldDragon_Logo_1024x773-by_solstice_arctic_luna-d6yrudl.png')


def exit():
    global image
    image = None
    close_canvas()


def update(frame_time):
    global logo_time
    if logo_time > 2.5:
        logo_time = 0
        Project_SceneFrameWork.scene_push(Scene001_Title)
    logo_time += frame_time


def draw(frame_time):
    global image
    clear_canvas()

    image.draw(Project_SceneFrameWork.Window_W / 2, Project_SceneFrameWork.Window_H / 2)
    update_canvas()


def handle_events(frame_time):
    events = get_events()
    pass


def pause(): pass


def resume(): pass
