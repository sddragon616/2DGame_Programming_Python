from pico2d import *
import Project_SceneFrameWork
import Scene003_BaseBattletScene

name = "PauseState"
image = None
back_button = None
mouseCoord = None
Mouse_Trigger = False
UI_font = None

class Coordinates:
    def __init__(self, x, y):
        self.x, self.y = x, y


class Button:
    def __init__(self, idle_image, on_image, push_image):
        self.x, self.y = 512, 275
        self.width, self.height = 375, 100
        self.Trigger = 0
        self.Button_Image = None
        self.Button_On_Image = None
        self.Button_Pushed_Image = None
        if self.Button_Image is None:
            self.Button_Image = idle_image
        if self.Button_On_Image is None:
            self.Button_On_Image = on_image
        if self.Button_Pushed_Image is None:
            self.Button_Pushed_Image = push_image

    def get_bb(self):
        return self.x - int(self.width / 2), self.y - int(self.height / 2), \
               self.x + int(self.width / 2), self.y + int(self.height / 2)


def enter():
    global image, UI_font
    global back_button, mouseCoord
    image = load_image('Resource_Image\\User_Interface\\Hint_UI_1024x768.png')
    button_image = load_image('Resource_Image\\User_Interface\\Button_by_JHL.png')
    button_on_image = load_image('Resource_Image\\User_Interface\\ButtonOn_by_JHL.png')
    button_pushed_image = load_image('Resource_Image\\User_Interface\\ButtonPush_by_JHL.png')

    if mouseCoord is None:
        mouseCoord = Coordinates(0, 0)
    back_button = Button(button_image, button_on_image, button_pushed_image)
    back_button.x, back_button.y = \
        Project_SceneFrameWork.Window_W - 265, Project_SceneFrameWork.Window_H - 65

    if UI_font is None:
        UI_font = load_font('Resource_Font\\Cornerstone.ttf', 50)


def exit():
    global image
    image = None


def handle_events(frame_time):
    global Mouse_Trigger
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            Project_SceneFrameWork.quit()
        else:
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
                Project_SceneFrameWork.scene_pop()
            # if (event.type, event.key) == (SDL_KEYDOWN, SDLK_h):
                # Project_SceneFrameWork.scene_pop()
            if event.type == SDL_MOUSEMOTION:
                mouseCoord.x, mouseCoord.y = event.x, Project_SceneFrameWork.Window_H - event.y
            if (event.type, event.button) == (SDL_MOUSEBUTTONDOWN, SDL_BUTTON_LEFT):
                Mouse_Trigger = True
            if (event.type, event.button) == (SDL_MOUSEBUTTONUP, SDL_BUTTON_LEFT):
                Mouse_Trigger = False
                if back_button.Trigger == 2:
                    Project_SceneFrameWork.scene_pop()


def draw(frame_time):
    global UI_font
    clear_canvas()
    image.draw(Project_SceneFrameWork.Window_W / 2, Project_SceneFrameWork.Window_H / 2)
    if back_button.Trigger == 0:
        back_button.Button_Image.clip_draw(0, 0, 1307, 598, back_button.x, back_button.y, 500, 100)
    elif back_button.Trigger == 1:
        back_button.Button_On_Image.clip_draw(0, 0, 1413, 704, back_button.x, back_button.y, int(405 * 4 / 3), 117)
    elif back_button.Trigger == 2:
        back_button.Button_Pushed_Image.clip_draw(0, 0, 1307, 598, back_button.x, back_button.y, 500, 100)

    UI_font.draw(back_button.x - (back_button.width / 2), back_button.y, 'Back To Title', (120, 230, 120))
    update_canvas()


def update(frame_time):
    global Mouse_Trigger, Loading_Trigger
    if button_process_mouse_collide(back_button, mouseCoord) is True:
        if Mouse_Trigger is True:
            back_button.Trigger = 2
        else:
            back_button.Trigger = 1
    else:
        back_button.Trigger = 0


def pause():
    pass


def resume():
    pass


def button_process_mouse_collide(button, mouse_event):
    left_button, bottom_button, right_button, top_button = button.get_bb()

    if left_button > mouse_event.x:
        return False
    if right_button < mouse_event.x:
        return False
    if top_button < mouse_event.y:
        return False
    if bottom_button > mouse_event.y:
        return False
    return True