import pygame 
import sys 
import random 
import psycopg2
import time

conn = psycopg2.connect(dbname='lab10', user='postgres', password='1', host='localhost', port='5432') 
cur = conn.cursor()

player_name = str(input("your name: "))

cur.execute("SELECT * from snake_game_scores WHERE player_name =  %s", (player_name,))
rows = cur.fetchall()
if rows:
    print(f"{rows[0][1]} score:{rows[0][2]}, level:{rows[0][3]}")
    cur.close()
    conn.close()
    sys.exit()

pygame.init()
pygame.mixer.init()
 
pygame.mixer.music.load('music.ogg')
pygame.mixer.music.play(-1)
 
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()
 
#Game Font
font = pygame.font.Font(None,30)
 
# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
PURPLE = (137, 3, 171)
YELLOW = (255,255,0)
 
# Snake Settings
snake_pos = [100, 50]
snake_body = [[100, 50], [90, 50], [80, 50]]
snake_direction = "RIGHT"
change_to = snake_direction
speed = 15
 
# Food settings
food_pos = [random.randrange(1, (WIDTH // 10)) * 10, random.randrange(1, (HEIGHT // 10)) * 10]
food_spawn = False
game_score = 0
food_timers = {}
food_colors = {1: RED, 2: PURPLE, 3: YELLOW}

runing = True

rect1 = pygame.Rect(90, 140, 80, 80)
rect2 = pygame.Rect(260, 140, 80, 80)
rect3 = pygame.Rect(430, 140, 80, 80)
level = 0
font_levels=pygame.font.Font(None,130)


while runing:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            runing = False
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if rect1.collidepoint(event.pos):
                level = 1
                runing = False
            if rect2.collidepoint(event.pos):
                level = 2
                runing = False
            if rect3.collidepoint(event.pos):
                level = 3
                runing = False

    screen.fill((BLACK))

    pygame.draw.rect(screen, GREEN, rect1)
    level1 = font_levels.render("1", True, WHITE)
    screen.blit(level1,(108,140))

    pygame.draw.rect(screen, GREEN, rect2)
    level2 = font_levels.render("2", True, WHITE)
    screen.blit(level2,(278,140))

    pygame.draw.rect(screen, GREEN, rect3)
    level3 = font_levels.render("3", True, WHITE)
    screen.blit(level3,(448,140))

    pygame.display.update()
    clock.tick(speed)


def spawn_food():
    while True:
        new_food = [random.randrange(1, (WIDTH // 10)) * 10,
                    random.randrange(1, (HEIGHT // 10)) * 10]
        if new_food not in snake_body:
            weight = random.choice([1, 2, 3])
            food_timers[tuple(new_food)] = time.time()
            return new_food, weight

def update_food():
    global food_list
    current_time = time.time()
    food_list[:] = [food for food in food_list if current_time - food_timers.get(tuple(food[0]), 0) < 5]
    if level == 2:
        while len(food_list) < 4:
            food_list.append(spawn_food())
    else:
        if not food_list:
            food_list.append(spawn_food())

isRunning = True
paused = False

INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)

if level == 2:
    food_list = [spawn_food() for _ in range(4)]
else:
    food_list = [spawn_food()]

while isRunning:
    for event in pygame.event.get():
        if event.type == INC_SPEED and level == 1:
            speed += 0.5
        if event.type == pygame.QUIT:
            isRunning = False
            sys.exit()  # Fixed sys.quit() to sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                paused = not paused
            if event.key == pygame.K_UP and snake_direction != "DOWN":
                change_to = "UP"
            if event.key == pygame.K_DOWN and snake_direction != "UP":
                change_to = "DOWN"
            if event.key == pygame.K_LEFT and snake_direction != "RIGHT":
                change_to = "LEFT"
            if event.key == pygame.K_RIGHT and snake_direction != "LEFT":
                change_to = "RIGHT"    
            
    if paused:
        pause_text = font.render("PAUSED", True, WHITE)
        screen.blit(pause_text, (WIDTH // 2 -10, HEIGHT // 2))
        pygame.display.update()
        clock.tick(5)
        continue
 
    # Move snake based on direction
    snake_direction = change_to
    if snake_direction == "UP":
        snake_pos[1] -= 10
    elif snake_direction == "DOWN":
        snake_pos[1] += 10
    elif snake_direction == "LEFT":
        snake_pos[0] -= 10
    elif snake_direction == "RIGHT":
        snake_pos[0] += 10
 
 
    # Insert new position
    snake_body.insert(0, list(snake_pos))  
   
    # Check if food is eaten

    
    for food in food_list[:]:
        if snake_pos == food[0]:
            game_score += food[1]
            food_list.remove(food)
            food_timers.pop(tuple(food[0]), None)
            break
    else:
        snake_body.pop()

    update_food()

        

    # Check for collision with walls
    if (snake_pos[0] < 0 or snake_pos[0] >= WIDTH or snake_pos[1] < 0 or snake_pos[1] >= HEIGHT) and level !=3:
        isRunning = False
    if snake_pos[0] < 10 and level == 3:
        snake_pos[0] = WIDTH -10
    if snake_pos[0] > WIDTH -10 and level == 3:
        snake_pos[0] = 0
    if snake_pos[1] < 10 and level == 3:
        snake_pos[1] = HEIGHT -10
    if snake_pos[1] > HEIGHT-10 and level == 3:
        snake_pos[1] = 0
 
    # Check for collision with itself
    for block in snake_body[1:]:
        if snake_pos == block:
            isRunning = False
   
   
    # Update screen
    screen.fill(BLACK)
    for p in snake_body:
        pygame.draw.rect(screen, GREEN, pygame.Rect(p[0], p[1], 10, 10))
    for food in food_list:
        pygame.draw.rect(screen,food_colors[food[1]], pygame.Rect(food[0][0], food[0][1], 10, 10))

    game_score_text = font.render(f"""Your score: {game_score}  level: {level}""",True,WHITE)
    screen.blit(game_score_text,(20,20))
    pygame.display.update()
 
    pygame.display.flip()
    clock.tick(speed)
   
 
 
game_over_text = font.render("GAME OVER", True, WHITE)
game_over_rectangle = game_over_text.get_rect()
game_over_rectangle.center = (WIDTH / 2, HEIGHT / 2)
screen.blit(game_over_text,game_over_rectangle)
pygame.display.update()
pygame.time.wait(1000)
pygame.mixer

cur.execute("INSERT INTO snake_game_scores (player_name, score, level) VALUES (%s, %s, %s)", (player_name, game_score, level))
conn.commit()
cur.close()
conn.close()