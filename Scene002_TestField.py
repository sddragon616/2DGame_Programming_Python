from pico2d import *
import Project_FrameWork


name = "TestField"
image = None


def enter():
    global image
    if image is None:
        image = load_image('TestField_1024x768.png')


def exit():
    global image
    del image


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            Project_FrameWork.quit()
        else:
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
                Project_FrameWork.quit()


def draw():
    clear_canvas()
    image.draw(Project_FrameWork.Window_W/2, Project_FrameWork.Window_H/2)
    update_canvas()


def update(): pass


def pause(): pass


def resume(): pass


if __name__ == '__main__':
    print("This is Wrong Playing.\n")
