from pico2d import *
import Project_SceneFrameWork
import ObjectData002_SwordMan
import ObjectData003_Monster

name = "TestField"
image = None
user = None
flies = []


def enter():
    global image
    global user
    global flies
    user = ObjectData002_SwordMan.SwordMan(500, 600)
    flies = [ObjectData003_Monster.Fly() for index in range(10)]
    if image is None:
        image = load_image('Resource_Image\\TestField_1024x768.png')


def exit():
    global image
    global user
    global flies
    del user
    del image
    del flies


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
    if user.box_draw:
        user.draw_bb()
    for fly in flies:
        fly.draw()
        if user.box_draw:
            fly.draw_bb()

    update_canvas()


def update(frame_time):
    user.update(frame_time)
    for fly in flies:
        fly.update(frame_time, user)
        if collide(user, fly):
            user.hit_by_str(fly.STR)
        if user.melee_atk_collide(fly):
            fly.hit_by_str(user.STR)
            if fly.exp_pay:
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
