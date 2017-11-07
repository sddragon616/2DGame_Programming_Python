from pico2d import *
import Project_SceneFrameWork
import ObjectData002_SwordMan

name = "TestField"
image = None
user = None


def enter():
    global image
    global user
    user = ObjectData002_SwordMan.SwordMan(500, 600)
    if image is None:
        image = load_image('Resource_Image\\TestField_1024x768.png')


def exit():
    global image
    global user
    del user
    del image


def handle_events():
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


def draw():
    clear_canvas()
    image.draw(Project_SceneFrameWork.Window_W/2, Project_SceneFrameWork.Window_H/2)
    user.draw()
    update_canvas()


def update():
    user.update()


def pause(): pass


def resume(): pass


if __name__ == '__main__':
    print("This is Wrong Playing.\n")
