from pico2d import *
import Project_SceneFrameWork
import ObjectData002_SwordMan
import ObjectData003_Monster
import Scene002_TestField

name = "PauseState"
image = None
status_font = None


def enter():
    global image
    global status_font
    image = load_image('Resource_Image\\User_Interface\\UI_Window_1024x768.png')
    status_font = load_font('Resource_Font\\league_ghotic_extended_italic_by_dannci.ttf', 50)


def exit():
    global image
    global status_font
    del image
    del status_font


def handle_events(frame_time):
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            Project_SceneFrameWork.quit()
        else:
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
                Project_SceneFrameWork.quit()
            elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE):
                Project_SceneFrameWork.scene_change(Scene002_TestField)
            elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_u):
                Project_SceneFrameWork.scene_pop()


def draw(frame_time):
    clear_canvas()
    Scene002_TestField.draw_scene(frame_time)
    image.draw(Project_SceneFrameWork.Window_W / 2, Project_SceneFrameWork.Window_H / 2)
    status_font.draw(15, Project_SceneFrameWork.Window_H - 31,
                     'Name : %s' % Scene002_TestField.user.name,  (255, 215, 0))
    status_font.draw(15, Project_SceneFrameWork.Window_H - 70,
                     'LEVEL : %d' % Scene002_TestField.user.LEVEL, (195, 215, 130))
    status_font.draw(15, Project_SceneFrameWork.Window_H - 110, 'HP : %d / %d' %
                     (Scene002_TestField.user.HP, Scene002_TestField.user.MAX_HP), (255, 0, 0))
    status_font.draw(15, Project_SceneFrameWork.Window_H - 150, 'MP : %d / %d' %
                     (Scene002_TestField.user.MP, Scene002_TestField.user.MAX_MP), (0, 0, 255))
    status_font.draw(15, Project_SceneFrameWork.Window_H - 190, 'SP : %d / %d' %
                     (Scene002_TestField.user.STAMINA, Scene002_TestField.user.MAX_STAMINA), (255, 255, 0))
    status_font.draw(15, Project_SceneFrameWork.Window_H - 235,
                     'STRENGTH : %d' % Scene002_TestField.user.STR, (128, 0, 0))
    status_font.draw(15, Project_SceneFrameWork.Window_H - 275,
                     'INTELLIGENCE : %d' % Scene002_TestField.user.INT, (0, 0, 128))
    status_font.draw(15, Project_SceneFrameWork.Window_H - 315,
                     'DEFENCE : %d' % Scene002_TestField.user.DEF, (128, 35, 35))
    status_font.draw(15, Project_SceneFrameWork.Window_H - 355,
                     'MAGIC RESIST : %d' % Scene002_TestField.user.MR, (35, 35, 128))
    status_font.draw(15, Project_SceneFrameWork.Window_H - 410,
                     'Ability Point : %d' % Scene002_TestField.user.Ability_Point, (0, 255, 255))
    status_font.draw(15, Project_SceneFrameWork.Window_H - 450,
                     'Skill Point : %d' % Scene002_TestField.user.Skill_Point, (255, 0, 255))
    status_font.draw(15, Project_SceneFrameWork.Window_H - 500,
                     'EXPERIENCE : %d / %d' % (Scene002_TestField.user.Experience, Scene002_TestField.user.LEVEL * 10),
                     (35, 255, 35))
    status_font.draw(527, Project_SceneFrameWork.Window_H - 600,
                     'Number of HP Potion : %d' % Scene002_TestField.user.HpPotion.number, (35, 255, 155))
    update_canvas()


def update(frame_time):
    pass


def pause():
    pass


def resume():
    pass