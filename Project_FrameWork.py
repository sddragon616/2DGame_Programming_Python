running = None
stack = None
Window_W = 1024
Window_H = 768


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


def run(start_scene):
    global running, stack
    running = True
    stack = [start_scene]
    start_scene.enter()
    while running:
        stack[-1].handle_events()
        stack[-1].update()
        stack[-1].draw()
    while len(stack) > 0:
        stack[-1].exit()
        stack.pop()


def quit():
    global running
    running = False


if __name__ == '__main__':
    print("This is Wrong Playing.\n")