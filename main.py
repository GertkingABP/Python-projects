import pygame
import random

pygame.init()
# Инициализируем Pygame.mixer
pygame.mixer.init()
sound_main = pygame.mixer.Sound('sounds/Resident Evil - ost (www.hotplayer.ru).mp3')
sound_main.play()
clock = pygame.time.Clock()

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

# Цвета,шрифты
background_color = (255, 255, 255)
text_color1 = (0, 0, 0)
text_color2 = (64, 64, 64)
text_color3 = (210, 20, 30)
counter_font = pygame.font.Font(("fonts/DS Stamper.ttf"), 28)
game_over_font = pygame.font.Font(("fonts/Plasma Drip (BRK).ttf"), 56)

game_over = False   # флаг, обозначающий статус завершения игры. Для избегания ошибки с обновлением экрана

#Создание окна
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("ZombieShooter2D")
background = pygame.image.load("background1.png")

#--------------------------------------------------------ВРАГИ---------------------------------------------------------#
ENEMY_SIZE_WIDTH = 100
ENEMY_SIZE_HEIGHT = 50
ENEMY_SPEED = 1
ENEMY_SPAWN_INTERVAL = 5000
ENEMY_SPAWN_TIMER = pygame.time.get_ticks() + ENEMY_SPAWN_INTERVAL
enemies = []
enemy_images = {

    "right": [
        pygame.transform.scale(pygame.image.load("enemy_sprites/enemy_right1.png"),
                               (ENEMY_SIZE_WIDTH, ENEMY_SIZE_HEIGHT)),
        pygame.transform.scale(pygame.image.load("enemy_sprites/enemy_right2.png"),
                               (ENEMY_SIZE_WIDTH, ENEMY_SIZE_HEIGHT)),
        pygame.transform.scale(pygame.image.load("enemy_sprites/enemy_right3.png"),
                               (ENEMY_SIZE_WIDTH, ENEMY_SIZE_HEIGHT)),
        pygame.transform.scale(pygame.image.load("enemy_sprites/enemy_right4.png"),
                               (ENEMY_SIZE_WIDTH, ENEMY_SIZE_HEIGHT))
    ],

    "down": [
        pygame.transform.scale(pygame.image.load("enemy_sprites/enemy_down1.png"),
                               (ENEMY_SIZE_WIDTH, ENEMY_SIZE_HEIGHT)),
        pygame.transform.scale(pygame.image.load("enemy_sprites/enemy_down2.png"),
                               (ENEMY_SIZE_WIDTH, ENEMY_SIZE_HEIGHT)),
        pygame.transform.scale(pygame.image.load("enemy_sprites/enemy_down3.png"),
                               (ENEMY_SIZE_WIDTH, ENEMY_SIZE_HEIGHT)),
        pygame.transform.scale(pygame.image.load("enemy_sprites/enemy_down4.png"),
                               (ENEMY_SIZE_WIDTH, ENEMY_SIZE_HEIGHT))
    ],

    "left": [
        pygame.transform.scale(pygame.image.load("enemy_sprites/enemy_left1.png"),
                               (ENEMY_SIZE_WIDTH, ENEMY_SIZE_HEIGHT)),
        pygame.transform.scale(pygame.image.load("enemy_sprites/enemy_left2.png"),
                               (ENEMY_SIZE_WIDTH, ENEMY_SIZE_HEIGHT)),
        pygame.transform.scale(pygame.image.load("enemy_sprites/enemy_left3.png"),
                               (ENEMY_SIZE_WIDTH, ENEMY_SIZE_HEIGHT)),
        pygame.transform.scale(pygame.image.load("enemy_sprites/enemy_left4.png"),
                               (ENEMY_SIZE_WIDTH, ENEMY_SIZE_HEIGHT))
    ],

    "up": [
        pygame.transform.scale(pygame.image.load("enemy_sprites/enemy_up1.png"),
                               (ENEMY_SIZE_WIDTH, ENEMY_SIZE_HEIGHT)),
        pygame.transform.scale(pygame.image.load("enemy_sprites/enemy_up2.png"),
                               (ENEMY_SIZE_WIDTH, ENEMY_SIZE_HEIGHT)),
        pygame.transform.scale(pygame.image.load("enemy_sprites/enemy_up3.png"),
                               (ENEMY_SIZE_WIDTH, ENEMY_SIZE_HEIGHT)),
        pygame.transform.scale(pygame.image.load("enemy_sprites/enemy_up4.png"),
                               (ENEMY_SIZE_WIDTH, ENEMY_SIZE_HEIGHT))
    ]
}

# Для каждого направления анимации, инициализировать список изображений врага
for direction_enemy, images in enemy_images.items():
    for i in range(len(images)):
        enemy_images[direction_enemy][i] = pygame.transform.scale(images[i], (ENEMY_SIZE_WIDTH, ENEMY_SIZE_HEIGHT))

# Для каждого направления инициализировать индекс текущего изображения врага и таймер анимации
enemy_image_index = { "up": 0, "right": 0, "down": 0, "left": 0 }
enemy_image_timer = pygame.time.get_ticks()

# Функция для получения следующего изображения врага в зависимости от его направления и таймера
def next_enemy_image(direction_enemy):
    global enemy_image_index, enemy_image_timer
    if pygame.time.get_ticks() - enemy_image_timer > 10000:
        enemy_image_index[direction_enemy] = (enemy_image_index[direction_enemy] + 1) % len(enemy_images[direction_enemy])
        enemy_image_timer = pygame.time.get_ticks()

# Функция для обновления изображения врага в зависимости от его скорости и направления
def update_enemy_image(enemy):
    if abs(enemy["velocity"][0]) > abs(enemy["velocity"][1]):  # движение горизонтальное
        if enemy["velocity"][0] > 0:
            direction_enemy = "right"
        else:
            direction_enemy = "left"

    else:  # движение вертикальное
        if enemy["velocity"][1] > 0:
            direction_enemy = "down"
        else:
            direction_enemy = "up"

    enemy["image"] = enemy_images[direction_enemy][enemy_image_index[direction_enemy]]

# Функция для создания нового врага со случайными координатами и скоростью
def spawn_enemy():
    x = random.randint(0, SCREEN_WIDTH - ENEMY_SIZE_WIDTH)
    y = random.randint(0, SCREEN_HEIGHT - ENEMY_SIZE_HEIGHT)
    enemy_rect = pygame.Rect(x, y, ENEMY_SIZE_WIDTH, ENEMY_SIZE_HEIGHT)
    enemy = {
        "rect": enemy_rect,
        "velocity": [random.randint(-ENEMY_SPEED, ENEMY_SPEED), random.randint(-ENEMY_SPEED, ENEMY_SPEED)],
        "image": enemy_images["right"][0]
    }
    enemies.append(enemy)

sound_kiil_enemy = pygame.mixer.Sound('sounds/zvuk-krika-zombi-s-effektom-eho-2-24541.mp3')

#---------------------------------------------------------ИГРОК--------------------------------------------------------#
character_width = 100
character_height = 50
character_x = SCREEN_WIDTH // 2
character_y = SCREEN_HEIGHT // 2
character_speed = 2
character_direction = "right"

#загрузка спрайтов персонажа
character_sprites = {
    "down": [
        pygame.transform.scale(pygame.image.load("character_sprites2/character_down1.png"), (character_width, character_height)),
        pygame.transform.scale(pygame.image.load("character_sprites2/character_down2.png"), (character_width, character_height)),
        pygame.transform.scale(pygame.image.load("character_sprites2/character_down3.png"), (character_width, character_height)),
        pygame.transform.scale(pygame.image.load("character_sprites2/character_down4.png"), (character_width, character_height)),
    ],
    "up": [
        pygame.transform.scale(pygame.image.load("character_sprites2/character_up1.png"), (character_width, character_height)),
        pygame.transform.scale(pygame.image.load("character_sprites2/character_up2.png"), (character_width, character_height)),
        pygame.transform.scale(pygame.image.load("character_sprites2/character_up3.png"), (character_width, character_height)),
        pygame.transform.scale(pygame.image.load("character_sprites2/character_up4.png"), (character_width, character_height)),
    ],
    "left": [
        pygame.transform.scale(pygame.image.load("character_sprites2/character_left1.png"), (character_width, character_height)),
        pygame.transform.scale(pygame.image.load("character_sprites2/character_left2.png"), (character_width, character_height)),
        pygame.transform.scale(pygame.image.load("character_sprites2/character_left3.png"), (character_width, character_height)),
        pygame.transform.scale(pygame.image.load("character_sprites2/character_left4.png"), (character_width, character_height)),
    ],
    "right": [
        pygame.transform.scale(pygame.image.load("character_sprites2/character_right1.png"), (character_width, character_height)),
        pygame.transform.scale(pygame.image.load("character_sprites2/character_right2.png"), (character_width, character_height)),
        pygame.transform.scale(pygame.image.load("character_sprites2/character_right3.png"), (character_width, character_height)),
        pygame.transform.scale(pygame.image.load("character_sprites2/character_right4.png"), (character_width, character_height)),
    ],
}

character_sprite_index = 0
character_sprite_timer = 0
score = 0
score_font = pygame.font.SysFont("", 36)
total_score_font = pygame.font.SysFont("fonts/a MonumentoTitulNr Bold.ttf", 36)
sound_dead_character = pygame.mixer.Sound('sounds/death1.mp3')
sound_say1 = pygame.mixer.Sound('sounds/player_say_kontakt.mp3')
sound_say2 = pygame.mixer.Sound('sounds/player_say_kros.mp3')

#-------------------------------------------------------ВЫСТРЕЛЫ-------------------------------------------------------#
# Загрузка спрайтов
bullet_up = pygame.image.load("bullet_sprites/bullet_up.png")
bullet_right = pygame.image.load("bullet_sprites/bullet_right.png")
bullet_down = pygame.image.load("bullet_sprites/bullet_down.png")
bullet_left = pygame.image.load("bullet_sprites/bullet_left.png")

# Определение пуль
bullets = []
sound_shoot = pygame.mixer.Sound('sounds/spas.wav')
sound_ready_to_shoot = pygame.mixer.Sound('sounds/ready_to_shot.mp3')
sound_ready_to_shoot.play()
sound_empty_gun = pygame.mixer.Sound('sounds/empty_gun2.mp3')
sound_reload1 = pygame.mixer.Sound('sounds/reload_clipout.wav')
sound_reload2 = pygame.mixer.Sound('sounds/reload_clipin.wav')
sound_reload3 = pygame.mixer.Sound('sounds/reload_boltpull.wav')
sound_reload4 = pygame.mixer.Sound('sounds/shotgun_reload_p1.wav')
sound_reload5 = pygame.mixer.Sound('sounds/shotgun_reload_p2.wav')

sound_reload_mas = [sound_reload1, sound_reload2, sound_reload3, sound_reload4, sound_reload5]

shoot_interval = 500  # Задержка между выстрелами в миллисекундах
last_shot_time = 0    # Время последнего выстрела
reload_interval = 750 # задержка между перезарядками (в миллисекундах)
reload_delay = 500 # задержка между добавлением патронов после перезарядки (в миллисекундах)

last_reload_time = 0 # время последней перезарядки
reload_countdown = 0 # обратный отсчет до следующего добавления патрона


#Отображение количества патронов
ammo_font = pygame.font.SysFont("fonts/Balloon Light TL.ttf", 32)
ammo_count = 8
shooted_bullets = 0

#--------------------------------------------------------------ГЕЙМПАД--------------------------------------------------------------#
#Инициализация геймпада
pygame.joystick.init()
joystick_count = pygame.joystick.get_count()

#Если геймпад подключен
if joystick_count > 0:
    joystick = pygame.joystick.Joystick(0)
    print("Геймпад подключен")
    joystick.init()
    hat = joystick.get_hat(0) #для крестовины
else:
    print("Геймпад не обнаружен")
    hat = False

#-------------------------------------------------------Основной игровой цикл-------------------------------------------------------#
while not game_over:
    # Обработка событий мыши и клавиатуры
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE) or (event.type == pygame.JOYBUTTONDOWN and joystick.get_button(6)):
            pygame.quit()
            exit()
        elif event.type == pygame.VIDEORESIZE:
            # изменяем размеры окна
            SCREEN_WIDTH, SCREEN_HEIGHT = event.size
            screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)

    #Воспроизведение случайной реплики героя
    #choise_say = random.randint(1, 2)
    '''time_to_play_sound = random.randint(1, 3000)
    time_to_choise_say = random.randint(1, 2)
    if time_to_play_sound == 1:
        if time_to_choise_say == 1: sound_say1.play()
        elif time_to_choise_say == 2: sound_say2.play()'''

    #Игрок(управление на клавиатуре и геймпаде)
    moving = False
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] or keys[pygame.K_w] or (hat == (0, 1)):
        character_y -= character_speed
        character_direction = "down"
        moving = True
    elif keys[pygame.K_DOWN] or keys[pygame.K_s] or (hat == (0, -1)):
        character_y += character_speed
        character_direction = "up"
        moving = True
    if keys[pygame.K_LEFT] or keys[pygame.K_a] or (hat == (-1, 0)):
        character_x -= character_speed
        character_direction = "left"
        moving = True
    elif keys[pygame.K_RIGHT] or keys[pygame.K_d] or (hat == (1, 0)):
        character_x += character_speed
        character_direction = "right"
        moving = True

    if keys[pygame.K_SPACE] or (event.type == pygame.JOYBUTTONDOWN and event.button == 0):#выстрелы при нажатии пробела или кнопки геймпада A
        if ammo_count != 0:
            now_for_bullets = pygame.time.get_ticks()
            if now_for_bullets - last_shot_time >= shoot_interval:
                sound_shoot.play()
                last_shot_time = now_for_bullets
                #Создание новой пули
                new_bullet = {"x": character_x, "y": character_y, "direction": character_direction}
                bullets.append(new_bullet)
                ammo_count -= 1
                shooted_bullets += 1
        elif ammo_count == 0:
            sound_empty_gun.play()

    elif keys[pygame.K_r] or (event.type == pygame.JOYBUTTONDOWN and event.button == 2):#клавиша R или кнопка геймпада X
    #Перезарядка оружия
        '''while ammo_count != 8:
            k = 3
            while k < 5:
                sound_reload_mas[k].play()
                k += 1
            ammo_count += 8'''
        if ammo_count < 8:
            now = pygame.time.get_ticks()
            if now - last_reload_time >= reload_interval:
                if ammo_count < 7:
                    sound_reload_mas[3].play()
                elif ammo_count == 7:
                    sound_reload_mas[4].play()
                ammo_count += 1
                last_reload_time = now
                reload_countdown = reload_delay

    if moving:#движение игрока
        if character_speed != 0:
            character_sprite_timer += 1
            if character_sprite_timer >= 10:
                character_sprite_timer = 0
                character_sprite_index = (character_sprite_index + 1) % len(character_sprites[character_direction])
            if character_direction == "up":
                character_y += character_speed
            elif character_direction == "down":
                character_y -= character_speed
            elif character_direction == "left":
                character_x -= character_speed
            elif character_direction == "right":
                character_x += character_speed

        #Ограничение перемещения игрока границами экрана
        if character_x < 0: character_x = 0
        elif character_x > SCREEN_WIDTH - character_width: character_x = SCREEN_WIDTH - character_width
        if character_y > SCREEN_HEIGHT - character_height: character_y = SCREEN_HEIGHT - character_height

    #Враги
    now = pygame.time.get_ticks()
    if now >= ENEMY_SPAWN_TIMER:
        spawn_enemy()
        ENEMY_SPAWN_TIMER = now + ENEMY_SPAWN_INTERVAL
        ENEMY_SPAWN_INTERVAL -= 100
    for enemy in enemies:
        enemy["rect"].move_ip(enemy["velocity"])
        if enemy["rect"].left < 0 or enemy["rect"].right > SCREEN_WIDTH: enemy["velocity"][0] = -enemy["velocity"][0]
        if enemy["rect"].top < 0 or enemy["rect"].bottom > SCREEN_HEIGHT: enemy["velocity"][1] = -enemy["velocity"][1]
        update_enemy_image(enemy)
        next_enemy_image("up")
        update_enemy_image(enemy)
        next_enemy_image("right")
        update_enemy_image(enemy)

    #Отрисовка всех объектов на экране
    screen.blit(background, (0, 0))
    # Отрисовка счетчика очков
    score_text = counter_font.render("Убийств: " + str(score), True, text_color1)
    screen.blit(score_text, (10, 10))

    # Отображение количества патронов
    ammo_text = ammo_font.render("Патронов: " + str(ammo_count) + "/INF", True, (191, 156, 10))
    screen.blit(ammo_text, (10, 60))

    character_image = character_sprites[character_direction][character_sprite_index]
    screen.blit(pygame.transform.rotate(character_image, 90 * ["right", "down", "left", "up"].index(character_direction)), (character_x, character_y))

    if character_speed == 0: screen.blit(character_sprites[character_direction][0], (character_x, character_y))

    for enemy in enemies:
        screen.blit(enemy["image"], enemy["rect"])

    #Отрисовка всех пуль
    for bullet in bullets:
        bullet_direction = bullet["direction"]

        if bullet_direction == "down":
            screen.blit(bullet_up, ((bullet["x"] + 16), (bullet["y"] + 22)))
            bullet["y"] -= 10
        elif bullet_direction == "up":
            screen.blit(bullet_down, (bullet["x"] + 24, bullet["y"] + 70))
            bullet["y"] += 10
        elif bullet_direction == "left":
            screen.blit(bullet_left, (bullet["x"] + 8, bullet["y"] + 24))
            bullet["x"] -= 10
        elif bullet_direction == "right":
            screen.blit(bullet_right, (bullet["x"] + 80, bullet["y"] + 16))
            bullet["x"] += 10

        # Удаление пуль, вышедших за границы экрана
        if bullet["x"] < -64 or bullet["x"] > SCREEN_WIDTH or bullet["y"] < -64 or bullet["y"] > SCREEN_HEIGHT:
            bullets.remove(bullet)

        #Проверка столкновения пули с врагами
        for bullet in bullets:
            for enemy in enemies:
                if enemy["rect"].colliderect(
                        pygame.Rect(bullet["x"], bullet["y"], bullet_up.get_width(), bullet_up.get_height())):
                    enemies.remove(enemy)

                    bullet_out = random.randint(1, 10)#случайное пробитие пулей насквозь
                    if bullet_out != 10: bullets.remove(bullet)

                    sound_kiil_enemy.play()
                    score += 1

        pygame.display.update()

    #Проверка условия поражения
    for enemy in enemies:
        screen.blit(enemy["image"], enemy["rect"])
        if enemy["rect"].colliderect(pygame.Rect(character_x, character_y, character_width, character_height)):
            game_over = True
            sound_dead_character.play()
            text_game_over = game_over_font.render("You`re dead!", True, text_color3)
            screen.blit(text_game_over, (SCREEN_WIDTH // 2 - text_game_over.get_width() // 2, (SCREEN_HEIGHT) // 2 - text_game_over.get_height() // 2))
            score_text = counter_font.render("", True, text_color1)
            screen.blit(score_text, (10, 10))
            text_score_total = total_score_font.render("Совершено было убийств: " + str(score), True, text_color1)
            screen.blit(text_score_total, (SCREEN_WIDTH // 2 - text_score_total.get_width() // 2, (SCREEN_HEIGHT + 100) // 2 - text_score_total.get_height() // 2))
            text_bullets_total = total_score_font.render("Совершено было выстрелов: " + str(shooted_bullets), True, text_color1)
            screen.blit(text_bullets_total, (SCREEN_WIDTH // 2 - text_bullets_total.get_width() // 2, (SCREEN_HEIGHT + 200) // 2 - text_bullets_total.get_height() // 2))
            pygame.display.flip()
            pygame.time.delay(2000)
            exit(0)

    clock.tick(60)
    pygame.display.flip()

pygame.quit()