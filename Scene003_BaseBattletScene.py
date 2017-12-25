from pico2d import *
import Project_SceneFrameWork
import Scene002_Interface
import ObjectData002_SwordMan


name = "TestField"
user = None
death_sound = None


def enter():
    global user
    global death_sound
    user = ObjectData002_SwordMan.SwordMan(2000, 32)
    user.dir = 8
    if death_sound is None:
        death_sound = load_wav('Resource_Sound\\Effect_Sound\\Destroy.wav')
        death_sound.set_volume(128)


def exit():
    global user
    global death_sound
    del user
    del death_sound


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


def draw(frame_time):
    clear_canvas()
    draw_scene(frame_time)
    update_canvas()


def draw_scene(frame_time):
    user.draw()
    if user.box_draw_Trigger:
        user.draw_bb()


def update(frame_time, monsters, others):
    global death_sound
    user.update(frame_time, others)
    for monster in monsters:
        monster.update(frame_time, user, others)
        if collide(user, monster):
            user.hit_by_str(monster.STR, monster.dir, others)
        if user.melee_atk_collide(monster):
            monster.hit_by_str(user.STR, user.dir, others)
        if monster.exp_pay:  # 몬스터가 쓰러져서 경험치를 지급했는가?
            if monster.death():
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
