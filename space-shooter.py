import pygame
import random
import sys
import math

# Inisialisasi pygame
pygame.init()

# Warna
black = (0, 0, 0)
white = (255, 255, 255)
blue = (0, 0, 255)
red = (255, 0, 0)
green = (0, 255, 0)
yellow = (255, 255, 0)
gray = (100, 100, 100)

# Ukuran jendela
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Game Tembak-Menembak Luar Angkasa')

# Variabel game
clock = pygame.time.Clock()
fps = 60
player_speed = 5
bullet_speed = 7
enemy_speed = 3
bullet_delay = 300  # waktu delay dalam milidetik antara tembakan
max_combo = 32  # Maksimum combo

# Font untuk skor
font = pygame.font.Font(None, 36)

# Dekorasi luar angkasa
stars = [(random.randint(0, width), random.randint(0, height)) for _ in range(100)]
moon_x, moon_y = random.randint(50, width-50), random.randint(-50, 0)

# Kelas
class Player(pygame.sprite.Sprite):
    def __init__(self, spaceship_choice):
        super().__init__()
        self.image = pygame.image.load(spaceship_choice).convert_alpha()  # Load gambar pesawat dengan alpha channel
        self.image = pygame.transform.scale(self.image, (50, 50))  # Sesuaikan ukuran
        self.rect = self.image.get_rect()
        self.rect.center = (width // 2, height - 50)
        self.speed = player_speed

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < width:
            self.rect.x += self.speed

    def shoot(self, combo_multiplier):
        bullets = []
        for i in range(combo_multiplier):
            offset = (i - (combo_multiplier - 1) / 2) * 10
            bullets.append(Bullet(self.rect.centerx + offset, self.rect.top))
        return bullets

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('bullet.png').convert_alpha()  # Load gambar peluru dengan alpha channel
        self.image = pygame.transform.scale(self.image, (5, 15))  # Sesuaikan ukuran
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y

    def update(self):
        self.rect.y -= bullet_speed
        if self.rect.bottom < 0:
            self.kill()

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('enemy.png').convert_alpha()  # Load gambar musuh dengan alpha channel
        self.image = pygame.transform.scale(self.image, (40, 40))  # Sesuaikan ukuran
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, width - self.rect.width)
        self.rect.y = random.randint(-150, -self.rect.height)
        self.speed = enemy_speed

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > height:
            self.kill()

class Alien(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('alien.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (60, 60))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, width - self.rect.width)
        self.rect.y = random.randint(-150, -self.rect.height)
        self.speed = enemy_speed // 2
        self.health = 20

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > height:
            self.kill()

class Combo(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('coin.png').convert_alpha()  # Load gambar koin dengan alpha channel
        self.image = pygame.transform.scale(self.image, (30, 30))  # Sesuaikan ukuran
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, width - self.rect.width)
        self.rect.y = random.randint(-150, -self.rect.height)
        self.speed = enemy_speed // 2

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > height:
            self.kill()

def draw_space_decorations(player):
    # Draw stars
    for i, star in enumerate(stars):
        stars[i] = (star[0], (star[1] + 1) % height)
        pygame.draw.circle(screen, white, stars[i], 1)
    
    # Draw moon
    global moon_x, moon_y
    moon_y = (moon_y + 0.5) % height
    pygame.draw.circle(screen, gray, (int(moon_x), int(moon_y)), 30)
    pygame.draw.circle(screen, black, (int(moon_x) + 10, int(moon_y) - 10), 25)

def show_game_over_screen(score):
    screen.fill(black)
    draw_space_decorations(None)
    game_over_text = font.render("Game Over!", True, white)
    score_text = font.render(f"Final Score: {score}", True, white)
    restart_text = font.render("Press R to Restart or Q to Quit", True, white)
    
    screen.blit(game_over_text, (width // 2 - game_over_text.get_width() // 2, height // 2 - 60))
    screen.blit(score_text, (width // 2 - score_text.get_width() // 2, height // 2))
    screen.blit(restart_text, (width // 2 - restart_text.get_width() // 2, height // 2 + 60))
    
    pygame.display.flip()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return True
                elif event.key == pygame.K_q:
                    return False
    return False

def choose_spaceship():
    screen.fill(black)
    draw_space_decorations(None)
    title_text = font.render("Choose Your Spaceship", True, white)
    option1_text = font.render("1. Spaceship 1", True, white)
    option2_text = font.render("2. Spaceship 2", True, white)
    option3_text = font.render("3. Spaceship 3", True, white)
    
    screen.blit(title_text, (width // 2 - title_text.get_width() // 2, height // 2 - 200))
    screen.blit(option1_text, (width // 2 - option1_text.get_width() // 2, height // 2 - 50))
    screen.blit(option2_text, (width // 2 - option2_text.get_width() // 2, height // 2))
    screen.blit(option3_text, (width // 2 - option3_text.get_width() // 2, height // 2 + 50))
    
    spaceship1 = pygame.image.load('spaceship.png').convert_alpha()
    spaceship2 = pygame.image.load('spaceship2.png').convert_alpha()
    spaceship3 = pygame.image.load('spaceship3.png').convert_alpha()
    
    spaceship1 = pygame.transform.scale(spaceship1, (100, 100))
    spaceship2 = pygame.transform.scale(spaceship2, (100, 100))
    spaceship3 = pygame.transform.scale(spaceship3, (100, 100))
    
    screen.blit(spaceship1, (width // 4 - 50, height // 2 + 100))
    screen.blit(spaceship2, (width // 2 - 50, height // 2 + 100))
    screen.blit(spaceship3, (3 * width // 4 - 50, height // 2 + 100))
    
    pygame.display.flip()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return 'spaceship.png'
                elif event.key == pygame.K_2:
                    return 'spaceship2.png'
                elif event.key == pygame.K_3:
                    return 'spaceship3.png'
    return None

def main():
    spaceship_choice = choose_spaceship()
    if spaceship_choice is None:
        return

    player = Player(spaceship_choice)
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)

    bullets = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    aliens = pygame.sprite.Group()
    combos = pygame.sprite.Group()

    last_shoot_time = pygame.time.get_ticks()
    last_alien_spawn_time = pygame.time.get_ticks()
    score = 0
    combo_multiplier = 1

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    current_time = pygame.time.get_ticks()
                    if current_time - last_shoot_time > bullet_delay:
                        last_shoot_time = current_time
                        new_bullets = player.shoot(combo_multiplier)
                        for bullet in new_bullets:
                            all_sprites.add(bullet)
                            bullets.add(bullet)

        # Update
        all_sprites.update()

        # Check for collisions
        for bullet in bullets:
            hit_enemies = pygame.sprite.spritecollide(bullet, enemies, True)
            for enemy in hit_enemies:
                bullet.kill()
                score += 10 * combo_multiplier

            hit_aliens = pygame.sprite.spritecollide(bullet, aliens, False)
            for alien in hit_aliens:
                bullet.kill()
                alien.health -= 1
                if alien.health <= 0:
                    alien.kill()
                    score += 50 * combo_multiplier

        hit_player = pygame.sprite.spritecollideany(player, enemies)
        if hit_player:
            if show_game_over_screen(score):
                # Restart the game
                spaceship_choice = choose_spaceship()
                if spaceship_choice is None:
                    running = False
                    continue
                player = Player(spaceship_choice)
                all_sprites = pygame.sprite.Group()
                all_sprites.add(player)
                bullets = pygame.sprite.Group()
                enemies = pygame.sprite.Group()
                aliens = pygame.sprite.Group()
                combos = pygame.sprite.Group()
                last_shoot_time = pygame.time.get_ticks()
                last_alien_spawn_time = pygame.time.get_ticks()
                score = 0
                combo_multiplier = 1
            else:
                running = False
            continue

        # Check for combo collisions
        hit_combo = pygame.sprite.spritecollideany(player, combos)
        if hit_combo:
            hit_combo.kill()
            combo_multiplier = min(combo_multiplier * 2, max_combo)

        # Add new enemies
        if random.random() < 0.02:
            enemy = Enemy()
            all_sprites.add(enemy)
            enemies.add(enemy)

        # Add new aliens every 30 seconds
        current_time = pygame.time.get_ticks()
        if current_time - last_alien_spawn_time > 30000:  # 30 seconds
            last_alien_spawn_time = current_time
            alien = Alien()
            all_sprites.add(alien)
            aliens.add(alien)

        # Add new combos
        if random.random() < 0.005:
            combo = Combo()
            all_sprites.add(combo)
            combos.add(combo)

        # Draw
        screen.fill(black)
        draw_space_decorations(player)
        all_sprites.draw(screen)

        # Draw score and combo multiplier
        score_text = font.render(f"Score: {score}", True, white)
        combo_text = font.render(f"Combo: x{combo_multiplier}", True, yellow)
        screen.blit(score_text, (10, 10))
        screen.blit(combo_text, (width - combo_text.get_width() - 10, 10))

        pygame.display.flip()

        # Cap the frame rate
        clock.tick(fps)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
