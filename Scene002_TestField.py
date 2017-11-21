from pico2d import *
import Project_SceneFrameWork
import ObjectData002_SwordMan

name = "TestField"
image = None
user = None
fly = None


def enter():
    global image
    global user
    global fly
    user = ObjectData002_SwordMan.SwordMan(500, 600)
    if image is None:
        image = load_image('Resource_Image\\TestField_1024x768.png')


def exit():
    global image
    global user
    global fly
    del user
    del image
    del fly


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


def draw(frame_time):
    clear_canvas()
    image.draw(Project_SceneFrameWork.Window_W/2, Project_SceneFrameWork.Window_H/2)
    user.draw()
    fly.draw()
    fly.draw_bb()
    user.draw_bb()
    update_canvas()


def update(frame_time):
    user.update(frame_time)


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
