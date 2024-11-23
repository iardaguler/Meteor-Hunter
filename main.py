import pygame
import sys
import random
import time
from player import Player
from laser import Laser
from meteor import Meteor
from health import Health

# Pygame'i başlat
pygame.init()

score = 0
# Font oluştur
score_font = pygame.font.SysFont("Thunderbolt", 50)
score_write = score_font.render(f"Score: {score}", True, (255, 255, 255))
score_write_rect = score_write.get_rect(center=(100, 40))
score_write_rect_end = score_write.get_rect(center=(640, 200))

# Oyun sıfırlama fonksiyonu
def reset_game():
    global health_amount, game_over, player_object, player_group, health_group, score, meteor_spawn_rate
    pygame.mixer.music.play()
    health_amount = 3
    game_over = False
    game_over_sound.stop()
    score = 0
    meteor_spawn_rate = 500  # Başlangıç meteor spawn hızını belirle

    player_object = Player("assets/images/araç_düz.png", "assets/images/araç_sol.png", "assets/images/araç_sağ.png", 640, 675, 7)
    player_group.add(player_object)

    health_group.empty()  # Mevcut sağlık simgelerini temizle
    for i in range(3):
        health_object = Health("assets/images/can.png", 1150 + (i * 50), 40)
        health_group.add(health_object)

    # Meteorların spawn hızını başlat
    pygame.time.set_timer(METEOR_EVENT, meteor_spawn_rate)

# Ekranı ayarla
width = 1280
height = 720
fps = 144
health_amount = 3
frame = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

game_over = False
meteor_spawn_rate = 500  # Meteor spawn başlangıç hızı

# Başlığı değiştir
pygame.display.set_caption("Meteor Hunter")

# İkonu değiştir
icon = pygame.image.load("assets/images/araç_düz.png")
pygame.display.set_icon(icon)

# Arka plan müziğini yükle ve çal
pygame.mixer.music.load("assets/sounds/background.ogg")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.5)

# Lazer ateşleme sesini yükle
laser_fire_sound = pygame.mixer.Sound("assets/sounds/laserfire.mp3")
laser_fire_sound.set_volume(0.1)

laser_fire_multi_sound = pygame.mixer.Sound("assets/sounds/laserfiremulti.ogg")
laser_fire_multi_sound.set_volume(0.2)

# Oyun bitme ekranı müziğini yükle
game_over_sound = pygame.mixer.Sound("assets/sounds/gameover.ogg")
game_over_sound.set_volume(0.1)

# Arka plan resmi yükle
background_image = pygame.image.load("assets/images/arkaplan.png")

# Oyun bitti resmi yükle
game_over_image = pygame.image.load("assets/images/gameover.jpg")

# Meteor çarpma sesi yükle
meteor_crash_sound = pygame.mixer.Sound("assets/sounds/meteor_crash.mp3")
meteor_crash_sound.set_volume(0.1)

# Tekrar oyna butonu yükle
play_again_image = pygame.image.load("assets/images/playagain.png")
play_again_image = pygame.transform.scale(play_again_image, (759 // 4, 245 // 4))
play_again_image_rect = play_again_image.get_rect(center=(640, 550))

# Player sınıfından player objesi oluştur
player_object = Player("assets/images/araç_düz.png", "assets/images/araç_sol.png", "assets/images/araç_sağ.png", 640, 675, 7)

# Sprite grupları oluştur
player_group = pygame.sprite.Group()
player_group.add(player_object)

laser_group = pygame.sprite.Group()
meteor_group = pygame.sprite.Group()
health_group = pygame.sprite.Group()

# Health objesi oluştur
for i in range(3):
    health_object = Health("assets/images/can.png", 1150 + (i * 50), 40)
    health_group.add(health_object)

# Meteor olayı oluştur
METEOR_EVENT = pygame.USEREVENT
pygame.time.set_timer(METEOR_EVENT, meteor_spawn_rate)

laser_cooldown = 500
last_laser_time = 0

laser_cooldown_multi = 1000
last_laser_time_multi = 0

is_running = True

while is_running:
    if not game_over:
        score += .1
    mouse_pos = pygame.mouse.get_pos()  # Fare konumunu burada al
    score_write = score_font.render(f"Score: {int(score)}", True, (255, 255, 255))
    current_time_for_meteor = pygame.time.get_ticks() // 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            current_time = pygame.time.get_ticks()
            if event.button == 1:  # Sol fare tuşu
                if game_over and play_again_image_rect.collidepoint(event.pos):
                    reset_game()  # Yeniden başlatma
                elif not game_over and current_time - last_laser_time >= laser_cooldown:
                    laser_fire_sound.play()
                    laser_object = Laser("assets/images/lazer_kırmızı.png", player_object.rect.centerx, player_object.rect.top, 0, 7)
                    laser_group.add(laser_object)
                    last_laser_time = current_time
            elif event.button == 3:  # Sağ fare tuşu
                if game_over and play_again_image_rect.collidepoint(event.pos):
                    reset_game()
                elif not game_over and current_time - last_laser_time_multi >= laser_cooldown_multi:
                    laser_fire_multi_sound.play()
                    laser_object_mid = Laser("assets/images/lazer_kırmızı.png", player_object.rect.centerx, player_object.rect.top, -1, 7)
                    laser_object_left = Laser("assets/images/lazer_kırmızı.png", player_object.rect.centerx, player_object.rect.top, 0, 7)
                    laser_object_right = Laser("assets/images/lazer_kırmızı.png", player_object.rect.centerx, player_object.rect.top, 1, 7)
                    laser_group.add(laser_object_left)
                    laser_group.add(laser_object_mid)
                    laser_group.add(laser_object_right)
                    last_laser_time_multi = current_time
        if event.type == METEOR_EVENT:
            random_file_path = random.choice(("assets/images/meteorBüyük.png", "assets/images/meteorKüçük.png"))
            random_x = random.randint(0, 1280)
            random_y = random.randint(-200, -50)
            random_x_velocity = random.randint(-3, 3)
            random_y_velocity = random.randint(6, 10)
            meteor_object = Meteor(random_file_path, random_x, random_y, random_x_velocity, random_y_velocity)
            meteor_group.add(meteor_object)

            # Meteor spawn hızını, oyun süresine göre arttır
            if score > 30 and meteor_spawn_rate > 300:
                meteor_spawn_rate = 300  # 30 saniye sonra spawn hızı artacak
                pygame.time.set_timer(METEOR_EVENT, meteor_spawn_rate)
            elif score > 60 and meteor_spawn_rate > 200:
                meteor_spawn_rate = 200  # 60 saniye sonra spawn hızı daha da artacak
                pygame.time.set_timer(METEOR_EVENT, meteor_spawn_rate)
            elif score > 90 and meteor_spawn_rate > 150:
                meteor_spawn_rate = 150  # 90 saniye sonra spawn hızı daha da artacak
                pygame.time.set_timer(METEOR_EVENT, meteor_spawn_rate)

    for laser in laser_group:
        if pygame.sprite.spritecollide(laser, meteor_group, True):
            laser.kill()

    for meteor in meteor_group:
        if pygame.sprite.spritecollide(meteor, player_group, False):
            meteor_crash_sound.play()
            meteor.kill()
            if health_amount != 0:
                health_group.sprites()[0].kill()  # Sağlık simgesini kaldır
                health_amount -= 1
            if health_amount == 1:
                player_object.file_path = "assets/images/araç_hasarlı.png"
                player_object.file_path_left = "assets/images/araç_hasarlı.png"
                player_object.file_path_right = "assets/images/araç_hasarlı.png"
                player_object.velocity = 5
            if health_amount == 0:
                meteor_crash_sound.stop()
                game_over = True  # Oyun bitti durumunu güncelle

    # Arka plan resmi ekle
    frame.blit(background_image, (0, 0))
    frame.blit(score_write, score_write_rect)

    player_group.draw(frame)
    player_group.update()

    laser_group.draw(frame)
    laser_group.update()

    meteor_group.draw(frame)
    meteor_group.update()

    health_group.draw(frame)
    health_group.update()

    # Oyun bittiğinde mesajı ekrana yazdır
    if game_over:
        current_time_for_meteor = 0
        frame.blit(game_over_image, (0, 0))
        frame.blit(score_write, score_write_rect_end)

        # Buton hover durumunu kontrol et
        if play_again_image_rect.collidepoint(mouse_pos):
            # Butonu biraz büyüt
            play_again_image_hovered = pygame.transform.scale(play_again_image, (int(play_again_image.get_width() * 1.1), int(play_again_image.get_height() * 1.1)))
            play_again_image_rect_hovered = play_again_image_hovered.get_rect(center=play_again_image_rect.center)
            frame.blit(play_again_image_hovered, play_again_image_rect_hovered)
        else:
            frame.blit(play_again_image, play_again_image_rect)

        player_group.empty()  # Player'ı temizle
        laser_group.empty()  # Lazerleri temizle
        meteor_group.empty()  # Meteorları temizle
        health_group.empty()  # Sağlık simgelerini temizle
        pygame.mixer.music.stop()
        game_over_sound.play(-1)

        # Meteor spawna sıklığını sıfırla
        pygame.time.set_timer(METEOR_EVENT, 0)

    pygame.display.update()
    clock.tick(fps)

pygame.quit()
sys.exit()
