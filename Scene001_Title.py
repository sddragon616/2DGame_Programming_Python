from pico2d import *
import Project_SceneFrameWork
import Scene002_TestField

name = "Title_Scene"
image = None


def enter():
    global image
    if image is None:
        image = load_image('Resource_Image\\TITLE_1024x806.png')


def exit():
    global image
    del image


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            Project_SceneFrameWork.quit()
        else:
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
                Project_SceneFrameWork.quit()
            elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE):
                Project_SceneFrameWork.scene_change(Scene002_TestField)


def draw():
    clear_canvas()
    image.draw(Project_SceneFrameWork.Window_W/2, Project_SceneFrameWork.Window_H/2)
    update_canvas()


def update(): pass


def pause(): pass


def resume(): pass


if __name__ == '__main__':
    print("This is Wrong Playing.\n")