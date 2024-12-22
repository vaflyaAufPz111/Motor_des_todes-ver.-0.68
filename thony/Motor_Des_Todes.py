import pygame
import random

pygame.init()

white = (255, 255, 255)

width, height = 600, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Motor_Des_Todes")

kit_image = pygame.image.load('Aid_Kid.png')
kit_image = pygame.transform.scale(kit_image, (40, 40))

wall_creater = pygame.image.load('wall_creater.png')
wall_creater_image = pygame.transform.scale(wall_creater, (40, 40))

tank1_image = pygame.image.load('Defender.png')
tank1_image = pygame.transform.scale(tank1_image, (40, 40))

tank2_image = pygame.image.load('enemy.png')
tank2_image = pygame.transform.scale(tank2_image, (40, 40))

wall_image = pygame.image.load('wall.jpg')
wall_image = pygame.transform.scale(wall_image, (40, 40))

bullet_image = pygame.image.load('bullet.png')
bullet_image = pygame.transform.scale(bullet_image, (10, 10))


class Creater:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x, self.y, 40, 40)
        self.image = wall_creater_image  

    def draw(self):
        screen.blit(self.image, (self.x, self.y))

    def create_walls(self, walls):
        for _ in range(5): 
            x = random.randint(40, width - 80)
            y = random.randint(40, height - 80)
            new_wall = wall(x, y)
            if not any(new_wall.rect.colliderect(w.rect) for w in walls):
                walls.append(new_wall)

class Kit:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x, self.y, 40, 40)
        self.image = kit_image

    def draw(self):
        screen.blit(self.image, (self.x, self.y))

class Tank1: 
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.speed = 2.5
        self.hp = 3
        self.direction = "up"
        self.image = tank1_image
        self.rect = pygame.Rect(self.x, self.y, 40, 40)

    def draw(self):
        screen.blit(self.image, (self.x, self.y))

    def move(self, keys, walls):
        old_x, old_y = self.x, self.y
        if keys[pygame.K_UP] and self.y > 0:
            self.y -= self.speed
            self.direction = "up"
            self.image = pygame.transform.rotate(tank1_image, 0)
        if keys[pygame.K_DOWN] and self.y < height - 40:
            self.y += self.speed
            self.direction = "down"
            self.image = pygame.transform.rotate(tank1_image, 180)
        if keys[pygame.K_LEFT] and self.x > 0:
            self.x -= self.speed
            self.direction = "left"
            self.image = pygame.transform.rotate(tank1_image, 90)
        if keys[pygame.K_RIGHT] and self.x < width - 40:
            self.x += self.speed
            self.direction = "right"
            self.image = pygame.transform.rotate(tank1_image, -90)

        self.rect = pygame.Rect(self.x, self.y, 40, 40)

        for wall in walls:
            if self.rect.colliderect(wall.rect):
                self.x, self.y = old_x, old_y
                self.rect = pygame.Rect(self.x, self.y, 40, 40)


class Tank2:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.speed = 1
        self.hp = 1
        self.direction = "down"
        self.image = tank2_image
        self.rect = pygame.Rect(self.x, self.y, 40, 40)
        self.bullet_timer = 2 

    def draw(self):
        screen.blit(self.image, (self.x, self.y))

    def chase(self, target_x, target_y, walls):
        old_x, old_y = self.x, self.y
        if self.x < target_x:
            self.x += self.speed
            self.direction = "right"
            self.image = pygame.transform.rotate(tank2_image, -90)
        elif self.x > target_x:
            self.x -= self.speed
            self.direction = "left"
            self.image = pygame.transform.rotate(tank2_image, 90)

        if self.y < target_y:
            self.y += self.speed
            self.direction = "down"
            self.image = pygame.transform.rotate(tank2_image, 180)
        elif self.y > target_y:
            self.y -= self.speed
            self.direction = "up"
            self.image = pygame.transform.rotate(tank2_image, 0)

        self.rect = pygame.Rect(self.x, self.y, 40, 40)

        for wall in walls:
            if self.rect.colliderect(wall.rect):
                self.x, self.y = old_x, old_y
                if self.direction in ["up", "down"]:
                    self.x += self.speed if self.x < target_x else -self.speed
                else:
                    self.y += self.speed if self.y < target_y else -self.speed
                self.rect = pygame.Rect(self.x, self.y, 40, 40)

    def shoot(self, bullets):
        if self.bullet_timer == 0:  
            bullets.append(bullet(self.x + 15, self.y + 15, self.direction, 5))
            self.bullet_timer = 60  

    def update_timer(self):
        if self.bullet_timer > 0:
            self.bullet_timer -= 1


class wall:
    def __init__(self, x, y):
        self.hp = 1
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x, self.y, 40, 40)

    def draw(self):
        screen.blit(wall_image, (self.x, self.y))


class bullet:
    def __init__(self, x, y, direction, speed):
        self.x = x
        self.y = y
        self.direction = direction
        self.speed = speed
        self.rect = pygame.Rect(self.x, self.y, 10, 10)

    def move(self):
        if self.direction == "up":
            self.y -= self.speed
        elif self.direction == "down":
            self.y += self.speed
        elif self.direction == "left":
            self.x -= self.speed
        elif self.direction == "right":
            self.x += self.speed

        self.rect = pygame.Rect(self.x, self.y, 10, 10)

    def draw(self):
        screen.blit(bullet_image, (self.x, self.y))
def spawn_kit(kits, walls, enemies):
    x = random.randint(40, width - 80)
    y = random.randint(40, height - 80)
    new_kit = Kit(x, y)

    if not any(new_kit.rect.colliderect(obj.rect) for obj in walls + enemies):
        kits.append(new_kit)
        
def spawn_creater(creaters, walls, enemies):
    x = random.randint(40, width - 80)
    y = random.randint(40, height - 80)
    new_creater = Creater(x, y)

    if not any(new_creater.rect.colliderect(obj.rect) for obj in walls + enemies):
        creaters.append(new_creater)

def spawn_enemies(enemies, count, walls):
    for _ in range(count):
        x = random.randint(40, width - 80)
        y = random.randint(40, height - 80)
        new_enemy = Tank2(x, y)
        if not any(new_enemy.rect.colliderect(w.rect) for w in walls):
            enemies.append(new_enemy)

def draw_button(screen, text, rect, font, text_color, color, hover_color, action=None):
    mouse_pos = pygame.mouse.get_pos()
    clicked = pygame.mouse.get_pressed()

    if rect.collidepoint(mouse_pos):
        pygame.draw.rect(screen, hover_color, rect)
        if clicked[0] and action:
            action()
    else:
        pygame.draw.rect(screen, color, rect)

    text_surface = font.render(text, True, text_color)
    screen.blit(text_surface, (rect.x + (rect.width - text_surface.get_width()) // 2,
                               rect.y + (rect.height - text_surface.get_height()) // 2))

def spawn_wall_creater(wall_creaters, walls):
    x = random.randint(40, width - 80)
    y = random.randint(40, height - 80)
    new_creater = Creater(x, y)

    if not any(new_creater.rect.colliderect(w.rect) for w in walls):
        wall_creaters.append(new_creater)

def restart_game():
    pygame.quit()  
    main_menu()

def create_initial_walls():
    return [
        wall(200, 200), wall(240, 200), wall(240, 160), wall(240, 120),
        wall(360, 200), wall(360, 160), wall(360, 120), wall(400, 200), wall(200, 300), wall(200, 260),  wall(200, 220), wall(400, 300), wall(400, 260), wall(400, 220),
        wall(200, 400), wall(240, 400), wall(280, 400), wall(320, 400),
        wall(360, 400), wall(400, 400), wall(555, 450), wall(0, 450), wall(555, 0),
        wall(445, 43), wall(335, 4),
    ] 
 

def play_game(walls):
    tank1 = Tank1(300, 300)
    walls = create_initial_walls()
    enemies = [] 

    enemies = []
    while len(enemies) < random.randint(5, 10):
        x = random.randint(40, width - 80)
        y = random.randint(40, height - 80)
        new_enemy = Tank2(x, y)
        if not any(new_enemy.rect.colliderect(w.rect) for w in walls) and not new_enemy.rect.colliderect(tank1.rect):
            enemies.append(new_enemy)
    
    bullets = []
    enemy_bullets = []
    clock = pygame.time.Clock()
    running = True

    while running:
        screen.fill((0, 0, 0))
        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bullets.append(bullet(tank1.x + 15, tank1.y, tank1.direction, 10))

        tank1.move(keys, walls)
        
        for enemy in enemies[:]:
            enemy.chase(tank1.x, tank1.y, walls)
            enemy.shoot(enemy_bullets)
            enemy.update_timer()

            if tank1.rect.colliderect(enemy.rect): 
                tank1.hp -= 1
                enemies.remove(enemy)
                if tank1.hp <= 0:
                    running = False

        for bullet_obj in bullets[:]:
            bullet_obj.move()
            for enemy in enemies[:]:
                if bullet_obj.rect.colliderect(enemy.rect):
                    enemies.remove(enemy)
                    bullets.remove(bullet_obj)
                    break
            for wall in walls[:]:
                if bullet_obj.rect.colliderect(wall.rect):
                    wall.hp -= 1
                    bullets.remove(bullet_obj)
                    if wall.hp <= 0:
                        walls.remove(wall)
                    break

        for enemy_bullet in enemy_bullets[:]:
            enemy_bullet.move()
            if enemy_bullet.rect.colliderect(tank1.rect):
                tank1.hp -= 1
                enemy_bullets.remove(enemy_bullet)
                if tank1.hp <= 0:
                    running = False
            for wall in walls[:]:
                if enemy_bullet.rect.colliderect(wall.rect):
                    walls.remove(wall)
                    enemy_bullets.remove(enemy_bullet)
                    break

        if not enemies:
           font = pygame.font.Font(None, 75)
           text = font.render("You Win!", True, (0, 255, 0))
           screen.blit(text, (width // 2 - 150, height // 2 - 50))
           wait_text = font.render("Wait 3 second", True, (255, 250, 250))
           screen.blit(wait_text, (width // 2 - 200, height // 2 - 100))
           pygame.display.flip()
           pygame.time.wait(3000)
           break

        if not running:
            font = pygame.font.Font(None, 50)
            game_over_text = font.render(f"Game Over!", True, (255, 0, 0))
            screen.blit(game_over_text, (width // 2 - 200, height // 2 - 50))
            wait_text = font.render("Wait 3 second", True, (255, 250, 250))
            screen.blit(wait_text, (width // 2 - 200, height // 2 - 100))
            pygame.display.flip()
            pygame.time.wait(3000)
            break

        tank1.draw()
        for enemy in enemies:
            enemy.draw()
        for bullet_obj in bullets:
            bullet_obj.draw()
        for enemy_bullet in enemy_bullets:
            enemy_bullet.draw()
        for wall in walls:
            wall.draw()
        

        pygame.display.flip()
        clock.tick(30)

 
def Score_game(walls):
    tank1 = Tank1(300, 300)
    score = 0
    walls = create_initial_walls()
    enemies = []
    bullets = []
    enemy_bullets = []
    clock = pygame.time.Clock()
    wall_creaters = []
    kits = []
    running = True
    enemy_spawn_timer = 0
    kit_spawn_timer = 0
    wall_creater_spawn_timer = 0 
    
    while running:
        screen.fill((0, 0, 0))
        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bullets.append(bullet(tank1.x + 15, tank1.y, tank1.direction, 10))

        if kit_spawn_timer >= 300:
            spawn_kit(kits, walls, enemies)
            kit_spawn_timer = 0

        for kit in kits[:]:
            if tank1.rect.colliderect(kit.rect):
                tank1.hp = min(tank1.hp + random.randint(1, 2), 10) 
                kits.remove(kit)
                
        wall_creater_spawn_timer += 1
        if wall_creater_spawn_timer >= 120:  
           spawn_wall_creater(wall_creaters, walls)
           wall_creater_spawn_timer = 0
            
        for wall_creater in wall_creaters[:]:
            if tank1.rect.colliderect(wall_creater.rect):
                wall_creater.create_walls(walls)  
                wall_creaters.remove(wall_creater)




        tank1.move(keys, walls)

        for enemy in enemies[:]:
            enemy.chase(tank1.x, tank1.y, walls)
            enemy.shoot(enemy_bullets)
            enemy.update_timer()

            if tank1.rect.colliderect(enemy.rect):
                tank1.hp -= 1
                enemies.remove(enemy)
                if tank1.hp <= 0:
                    running = False

        for bullet_obj in bullets[:]:
            bullet_obj.move()
            for enemy in enemies[:]:
                if bullet_obj.rect.colliderect(enemy.rect):
                    enemies.remove(enemy)
                    bullets.remove(bullet_obj)
                    score += 1
                    break
            for wall in walls[:]:
                if bullet_obj.rect.colliderect(wall.rect):
                    walls.remove(wall)
                    bullets.remove(bullet_obj)
                    break

        for enemy_bullet in enemy_bullets[:]:
            enemy_bullet.move()
            if enemy_bullet.rect.colliderect(tank1.rect):
                tank1.hp -= 1
                enemy_bullets.remove(enemy_bullet)
                if tank1.hp <= 0:
                    running = False
            for wall in walls[:]:
                if enemy_bullet.rect.colliderect(wall.rect):
                    walls.remove(wall)
                    enemy_bullets.remove(enemy_bullet)
                    break

        enemy_spawn_timer += 2
        if enemy_spawn_timer >= 300:
            spawn_enemies(enemies, random.randint(1, 3), walls)
            enemy_spawn_timer = 0

        kit_spawn_timer += 0.5
        if kit_spawn_timer >= 300:
            spawn_kit(kits, walls, enemies)
            kit_spawn_timer = 0
        
        tank1.draw()
        for kit in kits:
            kit.draw()
        for enemy in enemies:
            enemy.draw()
        for bullet_obj in bullets:
            bullet_obj.draw()
        for enemy_bullet in enemy_bullets:
            enemy_bullet.draw()
        for wall_creater in wall_creaters:
            wall_creater.draw()
        for wall in walls:
            wall.draw()

        font = pygame.font.Font(None, 30)
        score_text = font.render(f"Score: {score}", True, white)
        hp_text = font.render(f"HP: {tank1.hp}", True, white)
        screen.blit(score_text, (10, 10))
        screen.blit(hp_text, (10, 40))

        pygame.display.flip()
        clock.tick(30)

        if not running:
            font = pygame.font.Font(None, 50)
            game_over_text = font.render(f"Game Over!", True, (255, 0, 0))
            screen.blit(game_over_text, (width // 2 - 200, height // 2 - 50))
            wait_text = font.render("Wait 3 second", True, (255, 250, 250))
            screen.blit(wait_text, (width // 2 - 200, height // 2 - 100))
            pygame.display.flip()
            pygame.time.wait(3000)
            break


font = pygame.font.Font(None, 100)
font1 = pygame.font.Font(None, 25)

def main_menu():
    menu_running = True
    font = pygame.font.Font(None, 50)
    
    walls = create_initial_walls()

    while menu_running:
        screen.fill((0, 0, 0))
        play_button = pygame.Rect(width // 2 - 55, height // 2 - 55, 160, 40)
        score_button = pygame.Rect(width // 2 - 50, height // 2 + 30, 120, 40)

        draw_button(screen, "Defender", play_button, font, (255, 255, 255), (100, 100, 100), (150, 150, 150), lambda: play_game(walls))
        draw_button(screen, "Score", score_button, font, (255, 255, 255), (100, 100, 100), (150, 150, 150), lambda: Score_game(walls))
        
        text_surface = font.render("Motor_Des_Todes", True, (255, 255, 255))
        screen.blit(text_surface, (180, 150))
        
        text_surface1 = font1.render("created-by_Money_Lover:)-", True, (255, 255, 255))
        screen.blit(text_surface1, (1, 5))
        
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menu_running = False

    pygame.quit()



main_menu()               
