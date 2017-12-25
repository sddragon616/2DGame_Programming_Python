import json
from pico2d import *


class TileSet:

    def __init__(self):
        self.firstgid = 0

    def load(self, file_name):
        f = open(file_name)
        data = json.load(f)
        f.close()
        self.__dict__.update(data)
        # print(self.__dict__)
        self.base_image = load_image(self.image)
        self.tile_images = []
        for i in range(self.tilecount):
            col, row = i % self.columns, i // self.columns
            left = col * self.tilewidth
            bottom = self.base_image.h - (row + 1) * self.tileheight
            image = self.base_image.clip_image(left, bottom, self.tilewidth, self.tileheight)
            self.tile_images.append(image)


def load_tile_set(file_name):
    tile_set = TileSet()
    tile_set.load(file_name)

    return tile_set


class TileMap:

    def load(self, name):
        f = open(name)
        info = json.load(f)
        f.close()

        self.__dict__.update(info)
        self.tile_set = load_tile_set(self.tilesets[0]['source'])
        self.firstgid = self.tilesets[0]['firstgid']
        self.data = self.layers[0]['data']
        self.ground_data = self.layers[2]['data']

        new_data = []
        for row in reversed(range(self.height)):    # 2차원 배열 형태로 행의 순서를 바꿔서 저장한다.
            new_data.append(self.data[row * self.width: row * self.width + self.width])
        self.data = new_data

        new_ground_data = []
        for row in reversed(range(self.height)):  # 2차원 배열 형태로 행의 순서를 바꿔서 저장한다.
            new_ground_data.append(self.ground_data[row * self.width: row * self.width + self.width])
        self.ground_data = new_ground_data


    def clip_draw_to_origin(self, left, bottom, width, height, dx, dy):
        tile_left = left // self.tilewidth
        tile_bottom = bottom // self.tileheight
        tile_width = (left + width) // self.tilewidth - tile_left + 1
        tile_height = (bottom + height) // self.tileheight - tile_bottom + 1

        left_origin = left % self.tilewidth
        bottom_origin = bottom % self.tileheight

        for x in range(tile_left, min(tile_left + tile_width, self.width)):
            for y in range(tile_bottom, min(tile_bottom + tile_height, self.height)):
                self.tile_set.tile_images[self.data[y][x] - self.firstgid]. \
                    clip_draw_to_origin(0, 0, self.tilewidth, self.tileheight,
                                        (x - tile_left) * self.tilewidth - left_origin,
                                        (y - tile_bottom) * self.tileheight - bottom_origin)
                self.tile_set.tile_images[self.ground_data[y][x] - self.firstgid]. \
                    draw_to_origin((x - tile_left) * self.tilewidth - left_origin,
                                    (y - tile_bottom) * self.tileheight - bottom_origin)


def load_tile_map(name):
    tile_map = TileMap()
    tile_map.load(name)

    return tile_map


class BackGround_Tilemap:
    def __init__(self):
        self.tile_map = load_tile_map('Map\\Mapdata\\Forest_Shining.json')
        self.canvas_width = get_canvas_width()
        self.canvas_height = get_canvas_height()
        self.w = self.tile_map.width * self.tile_map.tilewidth
        self.h = self.tile_map.height * self.tile_map.tileheight
        self.center_object = None
        self.max_window_left = 0
        self.max_window_bottom = 0
        self.window_left = 0
        self.window_bottom = 0

    def set_center_object(self, user):
        self.center_object = user
        self.max_window_left = self.w - self.canvas_width
        self.max_window_bottom = self.h - self.canvas_height

    def draw(self):
        self.tile_map.clip_draw_to_origin(self.window_left, self.window_bottom, self.canvas_width, self.canvas_height,
                                          0, 0)

    def update(self, frame_time):
        self.window_left = clamp(0, int(self.center_object.x) - self.canvas_width//2, self.max_window_left)
        self.window_bottom = clamp(0, int(self.center_object.y) - self.canvas_height//2, self.max_window_bottom)


