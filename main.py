import pygame
import sys
from logics import *
from database import get_best, cur, inser_result
import json
import os

gamers_db = get_best()


def draw_top_games():
    font_top = pygame.font.SysFont("comicsanms", 30)
    font_gamer = pygame.font.SysFont("comicsanms", 26)
    text_head = font_top.render("Best tries", True, color_text)
    screen.blit(text_head, (240, 0))
    for index, gamer in enumerate(gamers_db):
        name, score = gamer
        s = f'{index + 1}.{name} - {score}'
        text_gamer = font_gamer.render(s, True, color_text)
        screen.blit(text_gamer, (240, 25 + 20 * index))
        print(index, name, score)


def draw_interface(score, delta=0):
    pygame.draw.rect(screen, white, title_rec)
    font = pygame.font.SysFont('comicsanms', 70)
    font_score = pygame.font.SysFont("comicsanms", 35)
    font_delta = pygame.font.SysFont("comicsanms", 30)
    text_score = font_score.render("Score: ", True, color_text)
    text_score_value = font_score.render(f"{score}", True, color_text)
    screen.blit(text_score, (20, 35))
    screen.blit(text_score_value, (120, 35))
    if delta > 0:
        text_delta = font_delta.render(f"+{delta}", True, color_text)
        screen.blit(text_delta, (120, 65))
    pretty_print(mas)
    draw_top_games()
    for row in range(blocks):
        for colow in range(blocks):
            value = mas[row][colow]
            text = font.render(f'{value}', True, black)
            w = colow * size_block + (colow + 1) * margin
            h = row * size_block + (row + 1) * margin + size_block
            pygame.draw.rect(screen, colors[value], (w, h, size_block, size_block))
            if value != 0:
                font_w, font_h = text.get_size()
                text_x = w + (size_block - font_w) / 2
                text_y = h + (size_block - font_h) / 2
                screen.blit(text, (text_x, text_y))


color_text = (255, 127, 0)
colors = {
    0: (130, 130, 130),
    2: (255, 255, 255),
    4: (255, 255, 128),
    8: (255, 255, 0),
    16: (255, 235, 255),
    32: (255, 235, 128),
    64: (255, 235, 0),
    128: (255, 215, 255),
    256: (255, 215, 128),
    512: (255, 215, 0),
}

black = (0, 0, 0)
white = (255, 255, 255)
gray = (130, 130, 130)
blocks = 4
size_block = 110
margin = 10
width = blocks * size_block + margin * (blocks + 1)
height = width + 110
title_rec = pygame.Rect(0, 0, width, 100)


def init_conat():
    global score, mas
    mas = [
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
    ]
    empty = get_empty_list(mas)
    random.shuffle(empty)
    random_num1 = empty.pop()
    random_num2 = empty.pop()
    x1, y1 = get_index_from_number(random_num1)
    mas = insert_2_or_4(mas, x1, y1)
    x2, y2 = get_index_from_number(random_num2)
    mas = insert_2_or_4(mas, x2, y2)
    score = 0


mas = None
score = None
username = None
path = os.getcwd()
if "data.txt" in os.listdir():
    with open("data.txt") as file:
        data = json.load(file)
        mas = data["mas"]
        score = data["score"]
        username = data["user"]
    fuul_path = os.path.join(path, "data.txt")
    os.remove(fuul_path)
else:
    init_conat()



print(get_empty_list(mas))
pretty_print(mas)

pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("2048")


def draw_intro():
    ing2048 = pygame.image.load('2048_logo.png')
    font = pygame.font.SysFont('comicsanms', 70)
    text_welcome = font.render("Welcome!", True, white)
    name = "Введите имя"
    is_find_name = False

    while not is_find_name:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            elif event.type == pygame.KEYDOWN:
                if event.unicode.isalpha():
                    if name == "Введите имя":
                        name = event.unicode
                    else:
                        name += event.unicode
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                elif event.key == pygame.K_RETURN:
                    if len(name) > 2:
                        global username
                        username = name
                        is_find_name = True
                        break

        screen.fill(black)
        text_name = font.render(name, True, white)
        rect_name = text_name.get_rect()
        rect_name.center = screen.get_rect().center
        screen.blit(pygame.transform.scale(ing2048, [200, 200]), [10, 10])
        screen.blit(text_welcome, (240, 85))
        screen.blit(text_name, rect_name)
        pygame.display.update()
    screen.fill(black)


def draw_game_over():
    global username, mas, score, gamers_db
    ing2048 = pygame.image.load('2048_logo.png')
    font = pygame.font.SysFont('comicsanms', 60)
    text_game_over = font.render("Game over!", True, white)
    text_score = font.render(f"Вы набрали: {score}", True, white)
    best_score = gamers_db[0][1]
    if score > best_score:
        text = "Рекорд побит"
    else:
        text = f"Рекорд {best_score}"
    text_record = font.render(text, True, white)
    inser_result(username, score)
    gamers_db = get_best()
    make_disicion = False
    while not make_disicion:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    make_disicion = True
                    init_conat()
                elif event.key == pygame.K_RETURN:
                    username = None
                    make_disicion = True
                    init_conat()
        screen.fill(black)
        screen.blit(text_game_over, (230, 85))
        screen.blit(text_score, (50, 250))
        screen.blit(text_record, (50, 290))
        screen.blit(pygame.transform.scale(ing2048, [200, 200]), [10, 10])
        pygame.display.update()
    screen.fill(black)


def save_game():
    data = {
        "user": username,
        "score": score,
        "mas": mas
    }
    with open("data.txt", "w") as outfile:
        json.dump(data, outfile)


def game_loop():
    global score, mas
    draw_interface(score)
    pygame.display.update()
    is_mas_move = False
    while is_zero_in_mas(mas) or can_move(mas):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_game()
                pygame.quit()
                sys.exit(0)
            elif event.type == pygame.KEYDOWN:
                delta = 0
                if event.key == pygame.K_LEFT:
                    mas, delta, is_mas_move = move_left(mas)
                elif event.key == pygame.K_RIGHT:
                    mas, delta, is_mas_move = move_right(mas)
                elif event.key == pygame.K_UP:
                    mas, delta, is_mas_move = move_up(mas)
                elif event.key == pygame.K_DOWN:
                    mas, delta, is_mas_move = move_down(mas)
                score += delta

                if is_zero_in_mas(mas) and is_mas_move:
                    empty = get_empty_list(mas)
                    random.shuffle(empty)
                    random_num = empty.pop()
                    x, y = get_index_from_number(random_num)
                    mas = insert_2_or_4(mas, x, y)
                    print(f"Мы заполнили элемент под номером {random_num}")
                    is_mas_move = False
                draw_interface(score, delta)
                pygame.display.update()


while True:
    if username is None:
        draw_intro()
    game_loop()
    draw_game_over()
