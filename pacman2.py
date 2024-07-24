import pygame
import random

# Inicializace hry
pygame.init()

# Obrazovaka
screen_width = 1000
screen_height = 500
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Pacman2 1.1")

# nastaveni hry
DEBUG = False
jsme_ve_hre = False
pacman_distance = 5
fps = 60
clock = pygame.time.Clock()
score = 0
pacman_angle = 0

# Barvy
black = rgb = (0, 0, 0)
white = rgb = (255, 255, 255)
red = rgb = (255, 0, 0)
green = rgb = (0, 255, 0)
blue = rgb = (0, 0, 200)
yellow = rgb = (200, 200, 0)

# Obrazky
pacman_logo = pygame.image.load("img/pacman.png")
pacman_logo_rect = pacman_logo.get_rect()
pacman_logo_rect.center = (screen_width//2, screen_height//2)

czvlajka_image = pygame.image.load("img/czvlajka.png")
czvlajka_rect = czvlajka_image.get_rect()
czvlajka_rect.center = (993, 493)

pacman = pygame.image.load("img/pacman2.png")
pacman_rect = pacman.get_rect(center = (screen_width//2, screen_height//2))

hvezda = pygame.image.load("img/hvezda.png")
hvezda_rect = hvezda.get_rect()
hvezda_rect.center = (100, 350)

# nataveni fontu
font_big = pygame.font.Font("pismo/Emulogic.ttf", 40) 
font_medium = pygame.font.Font("pismo/Emulogic.ttf", 20) 

# font a text
pacman2_text = font_big.render("Pacman 2", True, yellow)
pacman2_text_rect = pacman2_text.get_rect()
pacman2_text_rect.center = (500, 40)

enter_text = font_medium.render("Press ENTER to start", True, yellow)
enter_text_rect = enter_text.get_rect()
enter_text_rect.center = (500, 470)

font_game = pygame.font.Font("pismo/Emulogic.ttf", 20)
game_text = font_game.render("Game", True, blue)
game_text_rect = game_text.get_rect()
game_text_rect.centerx = screen_width//2
game_text_rect.top = 10

score_text = font_medium.render(f"Score: {score}", True, blue)
score_text_rect = score_text.get_rect()
score_text_rect.x =10
score_text_rect.y =10

# hudba v pozadi
pygame.mixer.music.load("sound/pacman.mp3")
# prehrajeme hudbu v pozadi
pygame.mixer.music.play(-1, 0.0,2000)

# nahrani zvuky
sound_mission = pygame.mixer.Sound("sound/mission.mp3")
sound_mission.set_volume(1.)

# nahrani zvuku
hvezda_sound = pygame.mixer.Sound("sound/hvezdas.mp3") 
hvezda_sound.set_volume(0.5)

# Hlavní cyklus
lets_continue = True

while lets_continue:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            lets_continue = False

        
    # vypis vsech klaves
    keys = pygame.key.get_pressed()
    if jsme_ve_hre == False: # jsem v menu
        if (keys[pygame.K_RETURN]) and (jsme_ve_hre == False):
            jsme_ve_hre = True
    else: # jsem ve hre
        if keys[pygame.K_ESCAPE] and (jsme_ve_hre == True):
            jsme_ve_hre = False
            # pacman_rect.center = (screen_width//2, screen_height//2)
        elif (keys[pygame.K_UP] or keys[pygame.K_w]) and pacman_rect.top > 50:
            pacman_angle = 90
            pacman_rect.y -= pacman_distance
        elif(keys[pygame.K_DOWN] or keys[pygame.K_s]) and pacman_rect.bottom < screen_height:
            pacman_angle = 270
            pacman_rect.y += pacman_distance
        elif (keys[pygame.K_LEFT] or keys[pygame.K_a]) and pacman_rect.left > 0:
            pacman_rect.x -= pacman_distance
            pacman_angle = 180
        elif (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and pacman_rect.right < screen_width:
            pacman_rect.x += pacman_distance
            pacman_angle = 0
        
        # Kontrola kolize
        if pacman_rect.colliderect(hvezda_rect):
            hvezda_rect.centerx = random.randint(0 + 24, 1000 - 24)
            hvezda_rect.centery = random.randint(50 + 24, 500 - 24) 
            score += 1
            hvezda_sound.play()
    
    # obrazky a text
    rotated_pacman = pygame.transform.rotate(pacman, pacman_angle)
    rotated_pacman_rect = rotated_pacman.get_rect()
    rotated_pacman_rect.x = pacman_rect.x 
    rotated_pacman_rect.y = pacman_rect.y 
    
    if jsme_ve_hre == False: # jsem v menu
        screen.fill(blue)
        pygame.draw.line(screen, black, (0, 0), (1000, 500), 5)
        pygame.draw.line(screen, black, (1000, 0), (0, 500), 5)
        pygame.draw.circle(screen, yellow, (screen_width/2, screen_height/2), 100, 0)
        pygame.draw.rect(screen, black,(0, 450, 1000, 50))
        screen.blit(pacman_logo,pacman_logo_rect)
        screen.blit(czvlajka_image, czvlajka_rect)
        screen.blit(enter_text, enter_text_rect)
        screen.blit(pacman2_text, pacman2_text_rect)
    else: # jsem ve hre
        score_text = font_medium.render(f"Score: {score}", True, blue)
        score_text_rect = score_text.get_rect()
        score_text_rect.x =10
        score_text_rect.y =10  
        screen.fill(black)
        screen.blit(rotated_pacman, rotated_pacman_rect)
        screen.blit(hvezda, hvezda_rect)
        pygame.draw.line(screen, yellow, (0, 50), (1000, 50), 2)
        screen.blit(game_text, game_text_rect)
        screen.blit(score_text, score_text_rect)
        
        # tvary (hitbox) DEBUG
        if (DEBUG):
            pygame.draw.rect(screen, red, pacman_rect, 1)
            pygame.draw.rect(screen, green, hvezda_rect, 1)
        
        # tajna pisnicka
        if score == 100:
            sound_mission.play()

    # Udatujeme obrazovku
    pygame.display.update()

    # tikani hodin
    clock.tick(fps)

# Ukončení hry
print("Konec")
pygame.quit