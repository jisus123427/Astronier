import os
import pygame
import sys
import random


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def load_level(filename):
    filename = "data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: list(x.ljust(max_width, '.')), level_map))


def generate_level(level):
    new_eneny, new_player, x, y = None, None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                new_enemy = Enemy(x, y)
            elif level[y][x] == '@':
                new_player = Player(x, y)
    return new_player, x, y


def terminate():
    pygame.quit()
    sys.exit()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(fps)


pygame.init()
pygame.display.set_caption('Перемещение героя')
size = width, height = 400, 800
screen = pygame.display.set_mode(size)
all_sprites = pygame.sprite.Group()
fps = 50
clock = pygame.time.Clock()

enemy_image = load_image(random.choice(['invader_1', 'invader_2', 'invader_3', 'invader_4', 'invader_5']))
player_image = load_image('mar.png')
tile_width = tile_height = 50
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, pos_y)

    def move(self, pos_x, pos_y):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, pos_y)


def move_in_map(player, dx, dy, level_map, level_x, level_y):
    pos_x = player.pos_x + dx
    pos_y = player.pos_y + dy
    if 0 <= pos_x <= level_x and 0 <= pos_y <= level_y and level_map[pos_y][pos_x] == '.':
        player.move(pos_x, pos_y)
        level_map[pos_y][pos_x] = '@'
        level_map[pos_y - dy][pos_x - dx] = '.'


if __name__ == '__main__':
    level_map = load_level('map.txt')
    player, level_x, level_y = generate_level(load_level('map.txt'))
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN == pygame.K_LEFT:
                move_in_map(player, -1, 0, level_map, level_x, level_y)
            if event.type == pygame.KEYDOWN == pygame.K_RIGHT:
                move_in_map(player, 1, 0, level_map, level_x, level_y)

        screen.fill((0, 0, 0))
        tiles_group.draw(screen)
        player_group.draw(screen)
        pygame.display.flip()
        clock.tick(fps)
    pygame.quit()
