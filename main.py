import pygame
import random
import sqlite3
import inputbox
from player import Player
from enemy import Enemy
from button import Button
from text import Text
from constants import *
pygame.init()


player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT - PLAYER_HEIGHT)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Игра")


log_file = open("log.txt", "w")


conn = sqlite3.connect("highscores.db")
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS highscores (name text, score integer)")

player_name = inputbox.ask(screen, "Введите ваш никнейм:")

all_sprites_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()


player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT - PLAYER_HEIGHT)
all_sprites_group.add(player)

score_text = Text("Score: 0", 10, 10)
all_sprites_group.add(score_text)
game_over_text = Text("Game Over", SCREEN_WIDTH / 2 - 50, SCREEN_HEIGHT / 2)
you_win_text = Text("You Win!", SCREEN_WIDTH / 2 - 50, SCREEN_HEIGHT / 2)

def draw_rules(screen):
    font = pygame.font.Font(None, 18)
    rules_lines = [
        "Правила:",
        "1. Управляйте персонажем с помощью стрелок клавиатуры.",
        "2. Уклоняйтесь от врагов, падающих сверху.",
        "3. Наберите 10 очков, чтобы победить."
    ]
	
    y_pos = (SCREEN_HEIGHT // 2) - (len(rules_lines) * font.get_height()) // 2
	
    for line in rules_lines:
        text_surface = font.render(line, True, BLACK)
        rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, y_pos))
        screen.blit(text_surface, rect)
        y_pos += font.get_height()


def menu_scene():
    menu_sprites = pygame.sprite.Group()
    play_button = Button("Играть", SCREEN_WIDTH // 2 - 75, SCREEN_HEIGHT // 2 + 50, 150, 50)
    menu_sprites.add(play_button)
	
    running = True
    while running:
        screen.fill(WHITE)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if play_button.rect.collidepoint(mouse_pos):
                    running = False
            
        menu_sprites.draw(screen)
        draw_rules(screen)
        pygame.display.flip()
		
    return True

def show_highscores(screen):
    conn = sqlite3.connect("highscores.db")
    c = conn.cursor()
    c.execute("SELECT * FROM highscores ORDER BY score DESC LIMIT 5")
    highscores = c.fetchall()
    conn.close()

    font = pygame.font.Font(None, 36)
    y_pos = 100

    for idx, row in enumerate(highscores):
        name, score = row
        text_surface = font.render(f"{idx + 1}. {name}: {score}", True, BLACK)
        text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, y_pos))
        screen.blit(text_surface, text_rect)
        y_pos += 50


score = 0
game_over = False
you_win = False

if not menu_scene():
    game_over = True
    you_win = False
    
clock = pygame.time.Clock()
while not game_over and not you_win:
   
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True

    if random.randint(1, 100) == 1:
        enemy = Enemy()
        all_sprites_group.add(enemy)
        enemy_group.add(enemy)

    enemy_hits = pygame.sprite.spritecollide(player, enemy_group, False)
    for enemy in enemy_hits:
        game_over = True
        log_file.write(player_name + " проиграл, счет: " + str(score) + "\n")
        c.execute("INSERT INTO highscores VALUES ('" + player_name + "', " + str(score) + ")")
        conn.commit()

    
    all_sprites_group.update()


    for enemy in enemy_group:
        if enemy.rect.y > SCREEN_HEIGHT:
            enemy.kill()

    for enemy in enemy_group:
        if enemy.rect.y > SCREEN_HEIGHT - ENEMY_HEIGHT:
            score += 1
            enemy.kill()
            log_file.write(player_name + " получил 1 очко, счет: " + str(score) + "\n")
            score_text.image = score_text.font.render("Score: " + str(score), True, BLACK)


    if score>=10:
        you_win = True
        log_file.write(player_name + " выиграл, счет: " + str(score) + "\n")
        c.execute("INSERT INTO highscores VALUES ('" + player_name + "', " + str(score) + ")")
        conn.commit()

    screen.fill(WHITE)
    all_sprites_group.draw(screen)
    if game_over:
        all_sprites_group.add(game_over_text)
        all_sprites_group.remove(score_text)
    if you_win:
        all_sprites_group.add(you_win_text)
        all_sprites_group.remove(score_text)
    if game_over or you_win:
        show_highscores(screen)
    pygame.display.flip()

    clock.tick(60)

log_file.close()
conn.close()


conn = sqlite3.connect("highscores.db")
c = conn.cursor()
c.execute("SELECT * FROM highscores ORDER BY score DESC LIMIT 5")
highscores = c.fetchall()
print("Топ-5 игроков:")
for row in highscores:
    print(row[0], row[1])
conn.close()

pygame.quit()