from pico2d import *
import Project_SceneFrameWork
import Scene011_Stage01
import Scene012_Stage02
import Scene014_Boss_Stage
import Scene002_Hint_Interface

name = "Title_Scene"
image = None
Title_font = None

UI_font = None
Help = False
Title_BGM = None
Loading_Trigger = False


Game_Start_Button = None
Help_Button = None
mouseCoord = None
Mouse_Trigger = False


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


class TitleBGM:
    def __init__(self):
        self.bgm = load_music('Resource_Sound\\BGM\\Title.mp3')
        self.bgm.set_volume(128)
        self.bgm.repeat_play()


def enter():
    global image
    global Title_font
    global UI_font
    global Title_BGM
    global Game_Start_Button, Help_Button
    global mouseCoord
    if image is None:
        image = load_image('Resource_Image\\TITLE_1024x806.png')
    if Title_font is None:
        Title_font = load_font('Resource_Font\\claws.ttf', 250)
    if UI_font is None:
        UI_font = load_font('Resource_Font\\Cornerstone.ttf', 50)
    if Title_BGM is None:
        Title_BGM = TitleBGM()

    if mouseCoord is None:
        mouseCoord = Coordinates(0, 0)

    button_image = load_image('Resource_Image\\User_Interface\\Button_by_JHL.png')
    button_on_image = load_image('Resource_Image\\User_Interface\\ButtonOn_by_JHL.png')
    button_pushed_image = load_image('Resource_Image\\User_Interface\\ButtonPush_by_JHL.png')

    Game_Start_Button = Button(button_image, button_on_image, button_pushed_image)
    Game_Start_Button.x, Game_Start_Button.y = \
        Project_SceneFrameWork.Window_W / 2, Project_SceneFrameWork.Window_H - 450
    Help_Button = Button(button_image, button_on_image, button_pushed_image)
    Help_Button.x, Help_Button.y = Project_SceneFrameWork.Window_W / 2, Project_SceneFrameWork.Window_H - 565


def exit():
    global image
    global Title_font
    global UI_font
    global Title_BGM
    image = None
    Title_font = None
    UI_font = None
    Title_BGM = None


def handle_events(frame_time):
    global Loading_Trigger
    global Help
    global mouseCoord, Mouse_Trigger, Game_Start_Button
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            Project_SceneFrameWork.quit()
        else:
            # if (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
                #Project_SceneFrameWork.quit()
            # if (event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE):
                # Loading_Trigger = True
                # draw(frame_time)
                # Project_SceneFrameWork.scene_push(Scene011_Stage01)
                # Loading_Trigger = False
            # if (event.type, event.key) == (SDL_KEYDOWN, SDLK_h):
                # Project_SceneFrameWork.scene_push(Scene002_Hint_Interface)
            if event.type == SDL_MOUSEMOTION:
                mouseCoord.x, mouseCoord.y = event.x, Project_SceneFrameWork.Window_H - event.y
            if (event.type, event.button) == (SDL_MOUSEBUTTONDOWN, SDL_BUTTON_LEFT):
                Mouse_Trigger = True
            if (event.type, event.button) == (SDL_MOUSEBUTTONUP, SDL_BUTTON_LEFT):
                Mouse_Trigger = False
                if Game_Start_Button.Trigger == 2:
                    Loading_Trigger = True
                    draw(frame_time)
                    Project_SceneFrameWork.scene_push(Scene011_Stage01)
                    Loading_Trigger = False
                if Help_Button.Trigger == 2:
                    Project_SceneFrameWork.scene_push(Scene002_Hint_Interface)


def draw(frame_time):
    global Loading_Trigger, Button_Image, Button_On_Image, Button_Pushed_Image
    clear_canvas()
    image.draw(Project_SceneFrameWork.Window_W/2, Project_SceneFrameWork.Window_H/2)
    Title_font.draw(50, Project_SceneFrameWork.Window_H - 100, "   Dungeon", (255, 215, 0))
    Title_font.draw(50, Project_SceneFrameWork.Window_H - 300, '             Slayer', (255, 215, 0))

    if Game_Start_Button.Trigger == 0:
        Game_Start_Button.Button_Image.clip_draw(0, 0, 1307, 598, Game_Start_Button.x, Game_Start_Button.y, 375, 100)
    elif Game_Start_Button.Trigger == 1:
        Game_Start_Button.Button_On_Image.clip_draw(0, 0, 1413, 704, Game_Start_Button.x, Game_Start_Button.y, 405, 117)
    elif Game_Start_Button.Trigger == 2:
        Game_Start_Button.Button_Pushed_Image.clip_draw(0, 0, 1307, 598,
                                                        Game_Start_Button.x, Game_Start_Button.y, 375, 100)

    if Help_Button.Trigger == 0:
        Help_Button.Button_Image.clip_draw(0, 0, 1307, 598, Help_Button.x, Help_Button.y, 375, 100)
    elif Help_Button.Trigger == 1:
        Help_Button.Button_On_Image.clip_draw(0, 0, 1413, 704, Help_Button.x, Help_Button.y, 405, 117)
    elif Help_Button.Trigger == 2:
        Help_Button.Button_Pushed_Image.clip_draw(0, 0, 1307, 598, Help_Button.x, Help_Button.y, 375, 100)

    UI_font.draw(375, Project_SceneFrameWork.Window_H - 450, 'Game Start', (120, 230, 120))
    UI_font.draw(350, Project_SceneFrameWork.Window_H - 565, 'How to Play', (220, 130, 120))
    if Loading_Trigger:
        UI_font.draw(150, Project_SceneFrameWork.Window_H - 650, 'NOW LOADING.....Please Wait...', (255, 0, 0))
    update_canvas()


def update(frame_time):
    global Mouse_Trigger, Loading_Trigger
    if button_process_mouse_collide(Game_Start_Button, mouseCoord) is True:
        if Mouse_Trigger is True:
            Game_Start_Button.Trigger = 2
        else:
            Game_Start_Button.Trigger = 1
    else:
        Game_Start_Button.Trigger = 0
    if button_process_mouse_collide(Help_Button, mouseCoord) is True:
        if Mouse_Trigger is True:
            Help_Button.Trigger = 2
        else:
            Help_Button.Trigger = 1
    else:
        Help_Button.Trigger = 0


def pause(): pass


def resume():
    enter()


if __name__ == '__main__':
    print("This is Wrong Playing.\n")


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
