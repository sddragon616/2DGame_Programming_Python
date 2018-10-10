from pico2d import *
import Project_SceneFrameWork
import Scene002_Interface
import Scene004_GameOver
import ObjectData002_SwordMan


name = "TestField"
user = None
death_sound = None
ui_bar_image = None
light_quick_slot_image = None
dark_quick_slot_image = None
UI_font = None
Message_font = None

melee_atk_flag = False  # 1 모션에 1회의 공격판정만 검사하기 위한 플래그

fly_image = None
crab_image = None
skull_golem_image = None
spear_image = None
slasher_image = None

fly_hit_sound = None
crab_hit_sound = None
skull_golem_hit_sound = None
spear_hit_sound = None
slasher_hit_sound = None


def enter():
    global user
    global death_sound
    global ui_bar_image, light_quick_slot_image, dark_quick_slot_image
    global UI_font, Message_font
    global fly_image, crab_image, skull_golem_image, spear_image, slasher_image
    global fly_hit_sound, crab_hit_sound, skull_golem_hit_sound, spear_hit_sound, slasher_hit_sound

    if ui_bar_image is None:
        ui_bar_image = load_image('Resource_Image\\User_Interface\\Gauge_bar.png')

    if light_quick_slot_image is None:
        light_quick_slot_image = load_image('Resource_Image\\User_Interface\\QuickSlotLight_by_JHL.png')
    if dark_quick_slot_image is None:
        dark_quick_slot_image = load_image('Resource_Image\\User_Interface\\QuickSlotDark_by_JHL.png')

    if UI_font is None:
        UI_font = load_font('Resource_Font\\Cornerstone.ttf', 15)
    if Message_font is None:
        Message_font = load_font('Resource_Font\\DungGeunMo.otf', 25)

    if user is None:
        user = ObjectData002_SwordMan.SwordMan(2000, 32)
        user.dir = 8
    if death_sound is None:
        death_sound = load_wav('Resource_Sound\\Effect_Sound\\Destroy.wav')
        death_sound.set_volume(64)

    # image pre load
    if fly_image is None:
        fly_image = load_image('Resource_Image\\Monster001_fly.png')
    if crab_image is None:
        crab_image = load_image('Resource_Image\\Monster002_crab.png')
    if skull_golem_image is None:
        skull_golem_image = load_image('Resource_Image\\Monster003_SkullGolem.png')
    if spear_image is None:
        spear_image = load_image('Resource_Image\\Monster004_Spear.png')
    if slasher_image is None:
        slasher_image = load_image('Resource_Image\\Monster005_Slasher.png')

    # wav sound pre load
    if fly_hit_sound is None:
        fly_hit_sound = load_wav('Resource_Sound\\Effect_Sound\\Damage1.wav')
        fly_hit_sound.set_volume(64)
    if crab_hit_sound is None:
        crab_hit_sound = load_wav('Resource_Sound\\Effect_Sound\\Slash12.wav')
        crab_hit_sound.set_volume(64)
    if skull_golem_hit_sound is None:
        skull_golem_hit_sound = load_wav('Resource_Sound\\Effect_Sound\\Slash11.wav')
        skull_golem_hit_sound.set_volume(64)
    if spear_hit_sound is None:
        spear_hit_sound = load_wav('Resource_Sound\\Effect_Sound\\Slash11.wav')
        spear_hit_sound.set_volume(64)
    if slasher_hit_sound is None:
        slasher_hit_sound = load_wav('Resource_Sound\\Effect_Sound\\Slash10.wav')
        slasher_hit_sound.set_volume(128)



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
                # Project_SceneFrameWork.quit()
                pass
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
    # HP bar
    ui_bar_image.clip_draw(9, 36, 1, 8, 100, Project_SceneFrameWork.Window_H - 15, 100, 16)
    ui_bar_image.clip_draw(0, 36, 9, 8,
                           100 - (100 * ((user.MAX_HP - user.HP) / (user.MAX_HP * 2))),
                           Project_SceneFrameWork.Window_H - 15,
                           int(100 * (user.HP / user.MAX_HP)), 16)
    # MP bar
    ui_bar_image.clip_draw(9, 28, 1, 8, 100, Project_SceneFrameWork.Window_H - 45, 100, 16)
    ui_bar_image.clip_draw(0, 28, 9, 8,
                           100 - (100 * ((user.MAX_MP - user.MP) / (user.MAX_MP * 2))),
                           Project_SceneFrameWork.Window_H - 45,
                           int(100 * (user.MP / user.MAX_MP)), 16)
    # SP bar
    ui_bar_image.clip_draw(9, 20, 1, 8, 100, Project_SceneFrameWork.Window_H - 75, 100, 16)
    ui_bar_image.clip_draw(0, 20, 9, 8,
                           100 - (100 * ((user.MAX_STAMINA - user.STAMINA) / (user.MAX_STAMINA * 2))),
                           Project_SceneFrameWork.Window_H - 75,
                           int(100 * (user.STAMINA / user.MAX_STAMINA)), 16)
    # Exp bar
    ui_bar_image.clip_draw(9, 12, 1, 8, 100, Project_SceneFrameWork.Window_H - 105, 100, 16)
    ui_bar_image.clip_draw(0, 12, 9, 8,
                           100 - (100 * ((user.Max_Experience - user.Experience) / (user.Max_Experience * 2))),
                           Project_SceneFrameWork.Window_H - 105,
                           int(100 * (user.Experience / user.Max_Experience)), 16)

    # 수치값 표시하기
    UI_font.draw(165, Project_SceneFrameWork.Window_H - 15,
                 '%d / %d' % (user.HP, user.MAX_HP), (225, 25, 25))
    UI_font.draw(165, Project_SceneFrameWork.Window_H - 45,
                 '%d / %d' % (user.MP, user.MAX_MP), (25, 25, 225))
    UI_font.draw(165, Project_SceneFrameWork.Window_H - 75,
                 '%d / %d' % (user.STAMINA, user.MAX_STAMINA), (195, 125, 75))
    UI_font.draw(165, Project_SceneFrameWork.Window_H - 105,
                 '%d / %d' % (user.Experience, user.Max_Experience), (25, 225, 25))

    # 스킬 퀵 슬롯
    dark_quick_slot_image.clip_draw(0, 0, 32, 32, 64, 128, 64, 64)
    UI_font.draw(44, 144, 'A', (225, 225, 225))
    if user.class_num == 2 and user.Typhoon_Slash.Level > 0:
        user.skill_image.clip_draw(7 * 32, 8 * 32, 32, 32, 64, 128, 32, 32)
        UI_font.draw(44, 108, '%d' % user.Typhoon_Slash.Level, (225, 225, 225))
        UI_font.draw(78, 108, '%d' % user.Typhoon_Slash.use_sp, (195, 125, 75))
    dark_quick_slot_image.clip_draw(0, 0, 32, 32, 128, 128, 64, 64)
    UI_font.draw(108, 144, 'S', (225, 225, 225))
    if user.class_num == 2 and user.Air_split.Level > 0:
        user.skill_image.clip_draw(2 * 32, 14 * 32, 32, 32, 128, 128, 32, 32)
        UI_font.draw(108, 108, '%d' % user.Air_split.Level, (225, 225, 225))
        UI_font.draw(142, 124, '%d' % user.Air_split.use_mp, (35, 155, 225))
        UI_font.draw(142, 108, '%d' % user.Air_split.use_sp, (195, 125, 75))
    dark_quick_slot_image.clip_draw(0, 0, 32, 32, 192, 128, 64, 64)

    # 포션 퀵 슬롯
    light_quick_slot_image.clip_draw(0, 0, 32, 32, 64, 64, 64, 64)
    user.HpPotion.image.clip_draw(0, 0, 32, 32, 64, 64, 64, 64)
    UI_font.draw(44, 84, 'H', (225, 225, 225))
    UI_font.draw(78, 40, '%d' % user.HpPotion.number, (225, 35, 35))
    light_quick_slot_image.clip_draw(0, 0, 32, 32, 128, 64, 64, 64)
    user.MpPotion.image.clip_draw(0, 0, 32, 32, 128, 64, 64, 64)
    UI_font.draw(108, 84, 'J', (225, 225, 225))
    UI_font.draw(142, 40, '%d' % user.MpPotion.number, (35, 155, 225))
    light_quick_slot_image.clip_draw(0, 0, 32, 32, 192, 64, 64, 64)
    user.StaminaPotion.image.clip_draw(0, 0, 32, 32, 192, 64, 64, 64)
    UI_font.draw(172, 84, 'K', (225, 225, 225))
    UI_font.draw(206, 40, '%d' % user.StaminaPotion.number, (195, 125, 75))


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
            user.invincibility = True

        # 평타 검사
        if user.state == ObjectData002_SwordMan.MELEE_ATTACK:
            if user.melee_atk_collide(monster) and monster.invincibility is False:
                monster.hit_by_str(user.STR, user.dir, others)
                monster.invincibility = True

        # 플레이어가 소드맨인 경우의 스킬 검사
        if user.class_num == 2:
            if user.state == 4:
                if collide(user.Typhoon_Slash, monster):
                    knock_back_dir = 0
                    if monster.dir == 2:
                        knock_back_dir = 8
                    elif monster.dir == 8:
                        knock_back_dir = 2
                    elif monster.dir == 4:
                        knock_back_dir = 6
                    elif monster.dir == 6:
                        knock_back_dir = 4
                    elif monster.dir == 1:
                        knock_back_dir = 9
                    elif monster.dir == 3:
                        knock_back_dir = 7
                    elif monster.dir == 7:
                        knock_back_dir = 3
                    elif monster.dir == 9:
                        knock_back_dir = 1
                    monster.hit_by_str((0.9 * user.STR) + (1.5 * user.Typhoon_Slash.Level), knock_back_dir, others)
                    monster.invincibility = True
            if user.air_splitter_collide(monster):
                monster.hit_by_mag((1.25 * user.INT) + (1.25 * user.Air_split.Level), 0, [])
                monster.invincibility = True

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
