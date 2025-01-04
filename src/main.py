import pygame
from uploading_files_and_constants import *
from main_player import Player_cube


def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Игра")
    clock = pygame.time.Clock()
    player = Player_cube(player_image)
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)

    running = True
    is_fullscreen = False
    font_size = 36
    font = pygame.font.Font(font_Monaco_path, font_size)
    message = "Для игры войдите в полноэкранный режим. Нажмите F11"
    text_surface = font.render(message, True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11:
                    if is_fullscreen:
                        screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
                    else:
                        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                    is_fullscreen = not is_fullscreen
                if event.key == pygame.K_SPACE:
                    player.jump()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    player.jump()

        if not is_fullscreen:
            screen.fill((0, 0, 0))
            screen.blit(text_surface, text_rect)
        else:
            # Рисование фона в зависимости от размеров экрана
            background_scaled = pygame.transform.scale(background_image, (screen.get_width(), screen.get_height()))
            screen.blit(background_scaled, (0, 0))
            all_sprites.update()
            all_sprites.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
