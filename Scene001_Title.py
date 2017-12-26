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
    if image is None:
        image = load_image('Resource_Image\\TITLE_1024x806.png')
    if Title_font is None:
        Title_font = load_font('Resource_Font\\claws.ttf', 250)
    if UI_font is None:
        UI_font = load_font('Resource_Font\\Cornerstone.ttf', 50)
    if Title_BGM is None:
        Title_BGM = TitleBGM()


def exit():
    global image
    global Title_font
    global UI_font
    global Title_BGM
    del image
    del Title_font
    del UI_font
    del Title_BGM


def handle_events(frame_time):
    global Loading_Trigger
    global Help
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            Project_SceneFrameWork.quit()
        else:
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
                Project_SceneFrameWork.quit()
            elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE):
                Loading_Trigger = True
                draw(frame_time)
                Project_SceneFrameWork.scene_push(Scene011_Stage01)
                Loading_Trigger = False
            elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_h):
                Project_SceneFrameWork.scene_push(Scene002_Hint_Interface)


def draw(frame_time):
    global Loading_Trigger
    clear_canvas()
    image.draw(Project_SceneFrameWork.Window_W/2, Project_SceneFrameWork.Window_H/2)
    Title_font.draw(50, Project_SceneFrameWork.Window_H - 100, "Lord of", (255, 215, 0))
    Title_font.draw(50, Project_SceneFrameWork.Window_H - 300, '          Dungeon', (255, 215, 0))
    UI_font.draw(150, Project_SceneFrameWork.Window_H - 500, 'Press Space -> Game Start', (120, 230, 120))
    UI_font.draw(150, Project_SceneFrameWork.Window_H - 550, 'Press H -> Hot Key Help', (220, 130, 120))
    if Loading_Trigger:
        UI_font.draw(150, Project_SceneFrameWork.Window_H - 650, 'NOW LOADING.....Please Wait...', (255, 0, 0))
    update_canvas()


def update(frame_time): pass


def pause(): pass


def resume(): pass


if __name__ == '__main__':
    print("This is Wrong Playing.\n")