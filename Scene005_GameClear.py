import Project_SceneFrameWork
import Scene001_Title
from pico2d import *
import os


name = "GameClear"
image = None
BGM = None


class GameOverBGM:
    def __init__(self):
        self.bgm = load_music('Resource_Sound\\BGM\\GameClear.mp3')
        self.bgm.set_volume(128)
        self.bgm.repeat_play()


def enter():
    global image
    global BGM
    hide_lattice()
    image = load_image('Resource_Image\\GameClear.png')
    if BGM is None:
        BGM = GameOverBGM()


def exit():
    global image
    global BGM
    del image
    del BGM


def update(frame_time):
    pass


def draw(frame_time):
    global image
    clear_canvas()
    image.draw(Project_SceneFrameWork.Window_W / 2, Project_SceneFrameWork.Window_H / 2)
    update_canvas()


def handle_events(frame_time):
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            Project_SceneFrameWork.quit()
        else:
            if event.type == SDL_KEYDOWN or event.type == SDL_MOUSEBUTTONDOWN:
                Project_SceneFrameWork.quit()


def pause(): pass


def resume(): pass