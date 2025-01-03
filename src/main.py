import pygame
from uploading_files_and_constants import player_image, FPS
from main_player import Player


def main():
    pygame.init()
    window_width = 1200
    window_height = 700
    screen = pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption("Игра")
    clock = pygame.time.Clock()
    player = Player(player_image)
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)

    running = True
    is_fullscreen = False
    font_path = "C:\\Users\\Ususl\\PycharmProjects\\Dash game\\assets\\fonts\\Monaco.otf"  # ставим свой путь под шрифт
    font_size = 36
    font = pygame.font.Font(font_path, font_size)
    message = "Для игры войдите в полноэкранный режим. Нажмите F11"
    text_surface = font.render(message, True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=(window_width // 2, window_height // 2))

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11:
                    if is_fullscreen:
                        screen = pygame.display.set_mode((window_width, window_height))
                    else:
                        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                    is_fullscreen = not is_fullscreen
                if event.key == pygame.K_SPACE:
                    player.jump()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    player.jump()

        screen.fill((0, 0, 0))
        if not is_fullscreen:
            screen.blit(text_surface, text_rect)
        else:
            all_sprites.update()

        all_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
