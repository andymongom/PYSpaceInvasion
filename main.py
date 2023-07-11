"""
    This is a game with "space invader" theme
"""
import pygame
import random # para que aparescan las variables aleatorias
# Initialize pygamep
import math
pygame.init()
# Create game screen
screen = pygame.display.set_mode((800, 600))
# Create background
# pygame.display.set_caption()
# Set icon and tittle
pygame.display.set_caption("Cat Invaders")
icon = pygame.image.load("gato.png")
pygame.display.set_icon(icon)
background = pygame.image.load("galaxy.png")

# add player
img_player = pygame.image.load("Mouse.png")
player_x = 368
player_y = 536
player_x_change = 0

# Enemy variables
img_enemy = []
enemy_x = []  # hacemos listas para los enemigos
enemy_y = []
enemy_x_change = []
enemy_y_change = []
number_of_enemies = 5

for i in range(number_of_enemies):
    img_enemy.append(pygame.image.load("Gatos.png"))
    enemy_x.append(random.randint(0, 736))# aparecen en lugares random
    enemy_y.append(random.randint(30, 200))
    enemy_x_change = 5
    enemy_y_change = 1

# Bullet variables
img_bullet = pygame.image.load("yarn.png")
bullet_x = 0
bullet_y = 536
bullet_x_change = 0
bullet_y_change = 9
bullet_visible = False


# Score variables
score = 0
score_font = pygame.font.Font("freesansbold.ttf", 32)
score_text_x = 10
score_text_y = 10

# End game
end_font = pygame.font.Font("freesansbold.ttf", 64)

# End mesage


def final_message():
    final_text = end_font.render(f"GAME OVER", True, (255, 255, 255))
    screen.blit(final_text, (200, 200))

# Show score
def show_score(x, y):
    text = score_font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(text, (x, y))


# Mostrar jugador de pantalla
def player(x, y):
    screen.blit(img_player, (x, y))


def enemy(x, y, enemy_index):
    screen.blit(img_enemy[enemy_index], (x, y))


# Shoot bullet
def shoot_bullet(x, y):
    global bullet_visible  # hacemos la variable global y la podemos acceder de cualquier lado
    bullet_visible = True  # para que sea vivible
    screen.blit(img_bullet, (x + 16, y + 10))


# Detect collision
def detect_collision(x_1, y_1, x_2, y_2):
    x_sub = x_2 - x_1
    y_sub = y_2 - y_1
    distance = math.sqrt(math.pow(x_sub, 2) + math.pow(y_sub, 2))
    if distance < 27:
        return True
    else:
        return False


# Game loop
is_running = True
while is_running:
    # Backgound
    screen.blit(background, (0, 0))

# player_x += 0.1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
        if event.type == pygame.KEYDOWN:
            # print("A key was pressed")
            if event.key == pygame.K_LEFT: # si se apreda la tecla izquierda
                # print("Left arrow pressed")
                player_x_change -= 2
            if event.key == pygame.K_RIGHT:  # si se apreda la tecla izquierda
                # print("Right arrow pressed")
                player_x_change += 2
            if event.key == pygame.K_SPACE:
                if not bullet_visible:
                    bullet_x = player_x
                    shoot_bullet(player_x, bullet_y)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or pygame.K_RIGHT:
                # print("Arrow keys was release")
                player_x_change = 0

    # Update player location
    player_x += player_x_change
    # Keep player inside the screen
    if player_x <= 0:
        player_x = 0
    elif player_x >= 736:
        player_x = 736

    for i in range(number_of_enemies):
        # End of game
        if enemy_y[i] > 450: #cuando rebase este punto pierdes
            for j in range(number_of_enemies):
                enemy_y[j] = 1000 #que vaya hasta abajo de la pantalla como si desapareciera
            final_message()
            break

        # Update enemy location
        enemy_x[i] += enemy_x_change[i]

        # Keep the enemy inside the screen
        if enemy_x[i] <= 0:
            enemy_x_change[i] += 0.3
            enemy_y[i] += enemy_y_change[i]
        elif enemy_x[i] >= 736:
            enemy_x_change[i] -= 0.3  # si llega hasta la derecha se pone a restar para moverse a la izquierda
            enemy_y[i] += enemy_y_change[i]

        # Detect collision
        collision = detect_collision(enemy_x[i], enemy_y[i], bullet_x, bullet_y)
        if collision:
            enemy_x[i] = random.randint(0, 736)  # Aparecen en lugares random
            enemy_y[i] = random.randint(30, 200)
            bullet_visible = False
            score += 1
            bullet_y = 500
            print(score)

        # show enemy
        enemy(enemy_x[i], enemy_y[i], i)

    # Shoot bullet
    if bullet_y <= -64:
        bullet_y = 500
        bullet_visible = False  # cada vez que desaparece se hace falso para que inicie otra vez el loop de arriba
    if bullet_visible:
        shoot_bullet(player_x, bullet_y)
        bullet_y -= bullet_y_change

    # Show player
    player(player_x, player_y)

    # Show score
    show_score(score_text_x, score_text_y)

    # Update screen
    pygame.display.update()
