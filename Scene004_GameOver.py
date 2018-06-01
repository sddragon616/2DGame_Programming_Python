import Project_SceneFrameWork
import Scene003_BaseBattletScene
from pico2d import *
import os


name = "GameOver"
image = None
overBGM = None


class GameOverBGM:
    def __init__(self):
        self.bgm = load_music('Resource_Sound\\BGM\\GameOver.mp3')
        self.bgm.set_volume(128)
        self.bgm.repeat_play()


def enter():
    global image
    global overBGM
    hide_lattice()
    image = load_image('Resource_Image\\GameOver.png')
    if overBGM is None:
        overBGM = GameOverBGM()


def exit():
    global image
    global overBGM
    Scene003_BaseBattletScene.user = None
    del image
    del overBGM


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
                Project_SceneFrameWork.scene_pop()


def pause(): pass


def resume(): pass