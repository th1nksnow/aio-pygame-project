import pygame
import sys
from random import randint
from settings import *
from sprites import Sprites


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Snow Grinder')
        pygame.display.set_icon(pygame.image.load('icons/main.bmp'))
        pygame.mixer.pre_init(44100, -16, 1, 512)
        pygame.time.set_timer(pygame.USEREVENT, 500)
        pygame.mixer.music.load('sounds/main_theme.mp3')
        pygame.mixer.music.play(-1)
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()

    def run(self):
        main_theme = 0
        vol = 1.0
        start_score = 0
        punch_animation = 0

        freeze_condition = True

        # Sounds
        sound_punch = pygame.mixer.Sound('sounds/punch.mp3')
        sound_punch.set_volume(0.3)
        freeze_sound = pygame.mixer.Sound('sounds/freeze_sound.mp3')
        freeze_sound.set_volume(1.5)

        background = pygame.image.load('images/background.jpg')

        score = pygame.image.load('images/score_board.png').convert_alpha()
        score_font = pygame.font.SysFont('arial', 46)

        player_straight = pygame.image.load('images/shani_right.png')
        player_reverse = pygame.image.load('images/shani_left.png')
        player_punch = pygame.image.load('images/shani_punch.png')
        player_punch.set_colorkey((255, 255, 255))
        player_straight.set_colorkey((255, 255, 255))
        player_reverse.set_colorkey((255, 255, 255))
        player = player_straight
        player_rect = player_straight.get_rect(centerx=WIDTH // 2, bottom=HEIGHT - 5)

        sprites_group = pygame.sprite.Group()
        sprites_data = ({'path': 'sprite_bronya.png', 'score': 100},
                        {'path': 'sprite_volech.png', 'score': 150},
                        {'path': 'sprite_nastya.png', 'score': 200},
                        {'path': 'sprite_bomb.png', 'score': -200},
                        {'path': 'sprite_freeze.png', 'score': 0},)
        sprites_surf = [pygame.image.load('images/' + data['path']).convert_alpha() for data in sprites_data]

        # freeze_surf = pygame.Surface((1600, 900))
        # freeze_surf.fill((0, 255, 255))

        def create_sprite(group):
            indx = randint(0, len(sprites_surf) - 1)
            x = randint(20, WIDTH - 20)
            speed = randint(2, 6)

            return Sprites(x, speed, sprites_surf[indx], sprites_data[indx]['score'], group)

        # Main cycle
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or start_score >= 9999:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.USEREVENT:
                    create_sprite(sprites_group)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_m:
                        main_theme = not main_theme
                        if main_theme:
                            pygame.mixer.music.pause()
                        else:
                            pygame.mixer.music.unpause()
                    elif event.key == pygame.K_EQUALS:
                        vol += 0.1
                        pygame.mixer.music.set_volume(vol)
                    elif event.key == pygame.K_MINUS:
                        vol -= 0.1
                        pygame.mixer.music.set_volume(vol)

            if player != player_punch:
                player_before_punch = player
            else:
                if punch_animation == 40:
                    player = player_before_punch
                    punch_animation = 0
                else:
                    punch_animation += 1

            # Player motion
            key_pressed = pygame.key.get_pressed()
            if key_pressed[pygame.K_RIGHT]:
                player_rect.x += player_speed
                if player != player_punch:
                    player = player_straight
                if player_rect.x > WIDTH - player_rect.width:
                    player_rect.x = WIDTH - player_rect.width
            elif key_pressed[pygame.K_LEFT]:
                player_rect.x -= player_speed
                if player != player_punch:
                    player = player_reverse
                if player_rect.x < 0:
                    player_rect.x = 0

            for sprite in sprites_group:
                if player_rect.collidepoint(sprite.rect.center):
                    if sprite.score != 0:
                        player = player_punch
                        sound_punch.play()
                        start_score += sprite.score
                        sprite.kill()
                    else:
                        freeze_condition = True
                        player = player_punch
                        sound_punch.play()
                        freeze_sound.play()
                        sprite.kill()

            if freeze_condition:
                freeze_condition = False
                for freeze_sprite in sprites_group:
                    if freeze_sprite.speed > 1.5:
                        freeze_sprite.speed /= 1.5

            # Drawing
            self.screen.blit(background, (0, 0))
            self.screen.blit(score, (10, 10))
            score_text = score_font.render('Волыч должен серому: ' + str(start_score) + '$', 1, (100, 138, 14))
            self.screen.blit(score_text, (20, 17))
            sprites_group.draw(self.screen)
            if player == player_punch:
                self.screen.blit(player, (player_rect.x, player_rect.y - 100))
            else:
                self.screen.blit(player, player_rect)
            pygame.display.update()
            sprites_group.update(HEIGHT)
            self.clock.tick(FPS)


if __name__ == '__main__':
    game = Game()
    game.run()
