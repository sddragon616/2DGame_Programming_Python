import time
from pico2d import *

running = None
stack = None
Window_W = 1024
Window_H = 768
current_time = get_time()


def scene_change(scene):
    global stack
    scene_pop()
    stack.append(scene)
    scene.enter()


def scene_push(scene):
    global stack
    if len(stack) > 0:
        stack[-1].pause()
    stack.append(scene)
    scene.enter()


def scene_pop():
    global stack
    if len(stack) > 0:
        stack[-1].exit()
        stack.pop()
    if len(stack) > 0:
        stack[-1].resume()


def get_frame_time():
    global current_time

    frame_time = get_time() - current_time
    current_time += frame_time
    return frame_time


def run(start_scene):
    global running, stack
    running = True
    stack = [start_scene]
    start_scene.enter()
    current_time = time.clock()
    while running:
        frame_time = time.clock() - current_time
        current_time += frame_time
        stack[-1].handle_events(frame_time)
        stack[-1].update(frame_time)
        stack[-1].draw(frame_time)
    while len(stack) > 0:
        stack[-1].exit()
        stack.pop()


def reset_time():
    global current_time
    current_time = time.clock()


def quit():
    global running
    running = False




if __name__ == '__main__':
    print("This is Wrong Playing.\n")