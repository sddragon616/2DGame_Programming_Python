from pico2d import *
import Project_SceneFrameWork
import Scene002_Interface
import Scene004_GameOver
import ObjectData002_SwordMan


name = "TestField"
user = None
death_sound = None
ui_bar_image = None
UI_font = None
monster_hp_bar = None

melee_atk_flag = False  # 1 모션에 1회의 공격판정만 검사하기 위한 플래그


def enter():
    global user
    global death_sound
    global ui_bar_image
    global UI_font
    global monster_hp_bar
    if ui_bar_image is None:
        ui_bar_image = load_image('Resource_Image\\User_Interface\\Gauge_bar.png')
    if UI_font is None:
        UI_font = load_font('Resource_Font\\Cornerstone.ttf', 15)
    if user is None:
        user = ObjectData002_SwordMan.SwordMan(2000, 32)
        user.dir = 8
    if death_sound is None:
        death_sound = load_wav('Resource_Sound\\Effect_Sound\\Destroy.wav')
        death_sound.set_volume(64)


def exit():
    global user
    global death_sound
    user = None
    death_sound = None


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
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_u):
                Project_SceneFrameWork.scene_push(Scene002_Interface)
                user.state = 0


def draw(frame_time):
    clear_canvas()
    draw_scene(frame_time)
    update_canvas()


def draw_scene(frame_time):
    user.draw()
    if user.box_draw_Trigger:
        user.draw_bb()

    # HP, MP, SP, EXP
    UI_font.draw(15, Project_SceneFrameWork.Window_H - 15, 'HP', (225, 25, 25))
    UI_font.draw(15, Project_SceneFrameWork.Window_H - 45, 'MP', (25, 25, 225))
    UI_font.draw(15, Project_SceneFrameWork.Window_H - 75, 'SP', (195, 125, 75))
    UI_font.draw(15, Project_SceneFrameWork.Window_H - 105, 'EXP', (25, 225, 25))

    # 게이지 그리기
    ui_bar_image.clip_draw(0, 36, 10, 7,
                           100 - (100 * ((user.MAX_HP-user.HP) / (user.MAX_HP * 2))),
                           Project_SceneFrameWork.Window_H - 15,
                           int(100*(user.HP/user.MAX_HP)), 16)
    ui_bar_image.clip_draw(0, 28, 10, 7,
                           100 - (100 * ((user.MAX_MP - user.MP) / (user.MAX_MP * 2))),
                           Project_SceneFrameWork.Window_H - 45,
                           int(100 * (user.MP / user.MAX_MP)), 16)
    ui_bar_image.clip_draw(0, 20, 10, 7,
                           100 - (100 * ((user.MAX_STAMINA - user.STAMINA) / (user.MAX_STAMINA * 2))),
                           Project_SceneFrameWork.Window_H - 75,
                           int(100 * (user.STAMINA / user.MAX_STAMINA)), 16)
    ui_bar_image.clip_draw(0, 12, 10, 7,
                           100 - (100 * ((user.Max_Experience - user.Experience) / (user.Max_Experience * 2))),
                           Project_SceneFrameWork.Window_H - 105,
                           int(100 * (user.Experience / user.Max_Experience)), 16)

    # 수치값 표시하기
    UI_font.draw(155, Project_SceneFrameWork.Window_H - 15,
                 '%d / %d' % (user.HP, user.MAX_HP), (225, 25, 25))
    UI_font.draw(155, Project_SceneFrameWork.Window_H - 45,
                 '%d / %d' % (user.MP, user.MAX_MP), (25, 25, 225))
    UI_font.draw(155, Project_SceneFrameWork.Window_H - 75,
                 '%d / %d' % (user.STAMINA, user.MAX_STAMINA), (195, 125, 75))
    UI_font.draw(155, Project_SceneFrameWork.Window_H - 105,
                 '%d / %d' % (user.Experience, user.Max_Experience), (25, 225, 25))


def update(frame_time, monsters, others):
    global death_sound

    if user.death():
        Project_SceneFrameWork.scene_push(Scene004_GameOver)

    user.update(frame_time, others)

    for monster in monsters:
        monster.update(frame_time, user, others)

        # 몬스터와 플레이어의 몸 충돌 검사
        if collide(user, monster) and user.invincibility is False:
            user.hit_by_str(monster.STR, monster.dir, others)

        # 평타 검사
        if user.state == ObjectData002_SwordMan.MELEE_ATTACK:
            if user.melee_atk_collide(monster) and monster.invincibility is False:
                monster.hit_by_str(user.STR, user.dir, others)
                monster.invincibility = True

        # 플레이어가 소드맨인 경우의 스킬 검사
        if user.class_num == 2:
            if user.air_splitter_collide(monster):
                monster.hit_by_mag(0.1 * user.INT * user.air_splitter_level, 0, [])

        if monster.death():
            if monster.exp_pay is True:  # 몬스터가 쓰러져서 경험치를 지급했는가?
                death_sound.play()
                monsters.remove(monster)


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
