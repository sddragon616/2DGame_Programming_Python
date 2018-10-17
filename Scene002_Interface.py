from pico2d import *
import Project_SceneFrameWork
import Scene003_BaseBattletScene

name = "PauseState"
image = None
status_font = None
cursor = 0
cursor_image = None


def enter():
    global image
    global cursor_image
    global status_font
    image = load_image('Resource_Image\\User_Interface\\UI_Window_1024x768.png')
    # status_font = load_font('Resource_Font\\league_ghotic_extended_italic_by_dannci.ttf', 50)
    status_font = load_font('Resource_Font\\DungGeunMo.otf', 50)
    cursor_image = load_image('Resource_Image\\User_Interface\\Select_Cursor.png')


def exit():
    global image
    global status_font
    image = None
    status_font = None


def handle_events(frame_time):
    global cursor
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            Project_SceneFrameWork.quit()
        else:
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
                Project_SceneFrameWork.scene_pop()
            elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_u):
                Project_SceneFrameWork.scene_pop()
            elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_UP):
                if cursor > 0:
                    cursor -= 1
                else:
                    cursor = 6
            elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_DOWN):
                if cursor < 7:
                    cursor += 1
                else:
                    cursor = 0
            elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE):
                if Scene003_BaseBattletScene.user.Ability_Point > 0 and cursor < 6:
                    if cursor == 0:
                        Scene003_BaseBattletScene.user.HP += 3
                        Scene003_BaseBattletScene.user.MAX_HP += 3
                    elif cursor == 1:
                        Scene003_BaseBattletScene.user.MP += 1
                        Scene003_BaseBattletScene.user.MAX_MP += 1
                    elif cursor == 2:
                        Scene003_BaseBattletScene.user.STAMINA += 1
                        Scene003_BaseBattletScene.user.MAX_STAMINA += 1
                    elif cursor == 3:
                        Scene003_BaseBattletScene.user.STR += 1
                    elif cursor == 4:
                        Scene003_BaseBattletScene.user.INT += 1
                    elif cursor == 5:
                        Scene003_BaseBattletScene.user.DEF += 1
                    # elif cursor == 6:
                        # Scene003_BaseBattletScene.user.MR += 1
                    Scene003_BaseBattletScene.user.Ability_Point -= 1
                if Scene003_BaseBattletScene.user.Skill_Point > 0 and cursor > 5:
                    if Scene003_BaseBattletScene.user.class_num == 2:
                        if cursor == 6:
                            Scene003_BaseBattletScene.user.Typhoon_Slash.Level += 1
                        elif cursor == 7:
                            Scene003_BaseBattletScene.user.Air_split.Level += 1
                    Scene003_BaseBattletScene.user.Skill_Point -= 1


def draw(frame_time):
    clear_canvas()
    Scene003_BaseBattletScene.draw_scene(frame_time)
    image.draw(Project_SceneFrameWork.Window_W / 2, Project_SceneFrameWork.Window_H / 2)
    status_font.draw(15, Project_SceneFrameWork.Window_H - 31,
                     '직업 %s' % Scene003_BaseBattletScene.user.name, (255, 215, 0))
    status_font.draw(15, Project_SceneFrameWork.Window_H - 70,
                     'LEVEL %d' % Scene003_BaseBattletScene.user.LEVEL, (195, 215, 130))
    status_font.draw(15, Project_SceneFrameWork.Window_H - 110, 'HP %d/%d' %
                     (Scene003_BaseBattletScene.user.HP, Scene003_BaseBattletScene.user.MAX_HP), (255, 0, 0))
    status_font.draw(15, Project_SceneFrameWork.Window_H - 150, 'MP %d/%d' %
                     (Scene003_BaseBattletScene.user.MP, Scene003_BaseBattletScene.user.MAX_MP), (0, 0, 255))
    status_font.draw(15, Project_SceneFrameWork.Window_H - 190, 'Stamina %d/%d' %
                     (Scene003_BaseBattletScene.user.STAMINA, Scene003_BaseBattletScene.user.MAX_STAMINA), (255, 255, 0))
    status_font.draw(15, Project_SceneFrameWork.Window_H - 235,
                     '물리 공격력 %d' % Scene003_BaseBattletScene.user.STR, (128, 0, 0))
    status_font.draw(15, Project_SceneFrameWork.Window_H - 275,
                     '마법 공격력 %d' % Scene003_BaseBattletScene.user.INT, (0, 0, 128))
    status_font.draw(15, Project_SceneFrameWork.Window_H - 315,
                     '방어력 %d' % Scene003_BaseBattletScene.user.DEF, (128, 35, 35))
    #status_font.draw(15, Project_SceneFrameWork.Window_H - 355,
    #                 '마법 저항력 %d' % Scene003_BaseBattletScene.user.MR, (35, 35, 128))
    status_font.draw(15, Project_SceneFrameWork.Window_H - 410,
                     'Ability Point %d' % Scene003_BaseBattletScene.user.Ability_Point, (0, 255, 255))
    status_font.draw(15, Project_SceneFrameWork.Window_H - 455,
                     'Skill Point %d' % Scene003_BaseBattletScene.user.Skill_Point, (255, 0, 255))
    status_font.draw(15, Project_SceneFrameWork.Window_H - 550,
                     '경험치 %d/%d' % (Scene003_BaseBattletScene.user.Experience,
                                    Scene003_BaseBattletScene.user.Max_Experience), (35, 255, 35))
    status_font.draw(15, Project_SceneFrameWork.Window_H - 650,
                     '↑↓키로 항목 선택', (235, 255, 235))
    status_font.draw(15, Project_SceneFrameWork.Window_H - 710,
                     'Space 키로 육성.', (235, 255, 235))

    Scene003_BaseBattletScene.user.HpPotion.image.draw(527, Project_SceneFrameWork.Window_H - 600)
    status_font.draw(570, Project_SceneFrameWork.Window_H - 600,
                     'x %d' % Scene003_BaseBattletScene.user.HpPotion.number, (35, 255, 155))
    Scene003_BaseBattletScene.user.MpPotion.image.draw(527, Project_SceneFrameWork.Window_H - 650)
    status_font.draw(570, Project_SceneFrameWork.Window_H - 650,
                     'x %d' % Scene003_BaseBattletScene.user.MpPotion.number, (35, 255, 155))
    Scene003_BaseBattletScene.user.StaminaPotion.image.draw(527, Project_SceneFrameWork.Window_H - 700)
    status_font.draw(570, Project_SceneFrameWork.Window_H - 700,
                     'x %d' % Scene003_BaseBattletScene.user.StaminaPotion.number, (35, 255, 155))

    if Scene003_BaseBattletScene.user.class_num == 2:
        Scene003_BaseBattletScene.user.skill_image.clip_draw(
            7 * 32, 8 * 32, 32, 32, 527, Project_SceneFrameWork.Window_H - 70, 32, 32)
        status_font.draw(570, Project_SceneFrameWork.Window_H - 70,
                         '회전베기 Lv.%d' % Scene003_BaseBattletScene.user.Typhoon_Slash.Level, (255, 255, 255))
        Scene003_BaseBattletScene.user.skill_image.clip_draw(
            2 * 32, 14 * 32, 32, 32, 527, Project_SceneFrameWork.Window_H - 110, 32, 32)
        status_font.draw(570, Project_SceneFrameWork.Window_H - 110,
                         '바람 쪼개기 Lv.%d' % Scene003_BaseBattletScene.user.Air_split.Level, (255, 255, 255))

    if cursor == 0:
        cursor_image.draw(450, Project_SceneFrameWork.Window_H - 110)
    elif cursor == 1:
        cursor_image.draw(450, Project_SceneFrameWork.Window_H - 150)
    elif cursor == 2:
        cursor_image.draw(450, Project_SceneFrameWork.Window_H - 190)
    elif cursor == 3:
        cursor_image.draw(450, Project_SceneFrameWork.Window_H - 235)
    elif cursor == 4:
        cursor_image.draw(450, Project_SceneFrameWork.Window_H - 275)
    elif cursor == 5:
        cursor_image.draw(450, Project_SceneFrameWork.Window_H - 315)
    # elif cursor == 6:
    #   cursor_image.draw(450, Project_SceneFrameWork.Window_H - 355)
    elif cursor == 6:
        cursor_image.draw(Project_SceneFrameWork.Window_W - 50, Project_SceneFrameWork.Window_H - 70)
    elif cursor == 7:
        cursor_image.draw(Project_SceneFrameWork.Window_W - 50, Project_SceneFrameWork.Window_H - 110)

    update_canvas()


def update(frame_time):
    pass


def pause():
    pass


def resume():
    pass