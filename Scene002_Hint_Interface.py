from pico2d import *
import Project_SceneFrameWork
import Scene003_BaseBattletScene

name = "PauseState"
image = None


def enter():
    global image
    image = load_image('Resource_Image\\User_Interface\\Hint_UI_1024x768.png')


def exit():
    global image
    del image


def handle_events(frame_time):
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            Project_SceneFrameWork.quit()
        else:
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
                Project_SceneFrameWork.quit()
            elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_h):
                Project_SceneFrameWork.scene_pop()


def draw(frame_time):
    clear_canvas()
    image.draw(Project_SceneFrameWork.Window_W / 2, Project_SceneFrameWork.Window_H / 2)
    update_canvas()


def update(frame_time):
    pass


def pause():
    pass


def resume():
    pass
