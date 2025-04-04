import pygame
import random
from game_sprites import Player, Bullet, Enemy



# Initialize pygame
pygame.init()

# Define constants used for the game.
screen_width = 800
screen_height = 600
player_width = 50
player_height = 50
movement_size = 2
bullet_damage = 25
frame_rate = 60
cool_down_count = 0

# Set the screen display mode and size
screen = pygame.display.set_mode(size = (screen_width,screen_height))

# Create a clock

clock = pygame.time.Clock()

# player = pygame.Rect(300, 400, 50, 50)
#hero = Player(color = (255,255,0), width = player_width, height = player_height)
# Set hero spawn point

players = pygame.sprite.Group()
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()

# Create a bullet at the position of the player
def shoot(player: Player):
    projectile = Bullet(color = (255,0,0), width = 5, height = 5)
    projectile.rect.x = player.rect.x + 0.5*player_width
    projectile.rect.y = player.rect.y
    bullets.add(projectile)


# Perform tasks needed every game tick.
def gametick():
    check_collisions()
    for bullet in bullets:
        bullet.rect.y = bullet.rect.y-movement_size
        if(bullet.rect.y < 0):
            bullet.kill()

        for enemy in enemies:
            enemy.cooldown()
            dist = pygame.math.Vector2(bullet.rect.x, bullet.rect.y).distance_to((enemy.rect.x, enemy.rect.y))
            print(dist)
            if dist < 45:
                enemy.automove(screen_width)
    #for enemy in enemies:
        #enemy.automove(screen_width)


# Spawn the player
def spawn_player():
    if players.has() == False:
        print(players.has())
        #spawn enemy, size 25x25
        player = Player(color = (255,255,0), width = player_width, height = player_height)
        player.rect.x = screen_width/2
        #spawn an enemy at a random position
        player.rect.y = screen_height - 30
        players.add(player)
        return player

# Spawn an enemy
def spawn_enemy():
    #spawn enemy, size 25x25
    enemy = Enemy(color = (0,0,255), width = 25, height = 25, hitpoints = 100)
    enemy.rect.x = random.randint(0, screen_width)
    #spawn an enemy at a random position
    enemy.rect.y = 40

    enemies.add(enemy)

# Check for collisions with enemies, kill enemies if they have no more hitpoints
def check_collisions():
    # For every bullet that exists, check if it hits an enemy.
    for bullet in bullets:
        collided_enemy = pygame.sprite.spritecollideany(bullet, enemies)
        # If it hits an enemy, kill the bullet, then deduct hitpoints from the enemy. If enemy hitpoints are less than 0, kill the enemy.
        if collided_enemy != None:
            collided_enemy.hit(bullet_damage)
            bullet.kill()
            print("hit enemy")
            if collided_enemy.hitpoints <= 0:
                collided_enemy.kill()

# Print instructions at specified position
def print_instructions(instructions: str, xposition: int, yposition: int):
    font = pygame.font.SysFont(name = "Helvetica", size = 20, bold = False, italic = False)
    surface = font.render(instructions, False, (255,255,255))
    screen.blit(source = surface, dest = (xposition, yposition))



#The loop that runs the game
def main():
    # Define variables used for the game
    hero = None
    run = True
    while run:
        # Run game at the desired FPS
        clock.tick(frame_rate)
        # re-write the screen background every loop as a solid color.
        screen.fill(color = (0,0,0))
        print_instructions("s to start, e to spawn enemy, space to shoot", 10, 570)

        gametick() # ticks are a way of managing events every loop though. The gametick function calculates collisions and moves the bullets.
        # Update all of the sprite groups and redraw them.
        players.update()
        players.draw(screen)
        enemies.update()
        enemies.draw(screen)
        bullets.update()
        bullets.draw(screen)

        if hero is not None:
            # Prevent the hero from leaving the screen
            hero.rect.clamp_ip(screen.get_rect())
            # Detect keypresses and move the player
            key = pygame.key.get_pressed()
            if key[pygame.K_LEFT] == True:
                hero.rect.x = hero.rect.x-movement_size
            if key[pygame.K_RIGHT] == True:
                hero.rect.x = hero.rect.x+movement_size
            if key[pygame.K_UP] == True:
                hero.rect.y = hero.rect.y-movement_size
            if key[pygame.K_DOWN] == True:
                hero.rect.y = hero.rect.y+movement_size
            #if key[pygame.K_SPACE] == True: #this shot too many at once, so I moved to to a pygame event so it only happens once per press.
                #shoot(hero)
            #if key[pygame.K_e] == True: #This spawned too many enemies at once. Moved to pygame event so it only happens once per press.
                #spawn_enemy()

        # Detect events and perform tasks accordingly
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    shoot(hero)
                if event.key == pygame.K_e:
                    spawn_enemy()
                if event.key == pygame.K_s:
                    hero = spawn_player()
        pygame.display.update()

    pygame.quit()


# Call the main routine
main()