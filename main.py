import pygame
import random

pygame.init()
screen = pygame.display.set_mode((1280, 908))
clock = pygame.time.Clock()
running = True

background = pygame.image.load('cozyduck.png').convert()
spatula = pygame.image.load('spatula.png').convert_alpha()
fly = pygame.image.load('fly.png').convert_alpha()

background = pygame.transform.scale(background, (1280, 908))
spatula = pygame.transform.scale(spatula, (90, 230))
fly = pygame.transform.scale(fly, (40, 35))

# Load the font for the start menu and score
font = pygame.font.Font('ThaleahFat.ttf', 64)

# Initialize start menu options
start_text = font.render('Start', True, (0, 0, 0))
how_to_play_text = font.render('How to Play', True, (0, 0, 0))
start_rect = pygame.Rect(500, 400, 280, 100)
how_to_play_rect = pygame.Rect(460, 550, 360, 100)

start_menu = True
game_started = False
show_instructions = False

flies = []
num_flies = random.randint(1, 5)
for _ in range(num_flies):
    fly_rect = fly.get_rect()
    fly_rect.center = (random.randint(100, 1180), random.randint(100, 808))
    fly_velocity = [random.choice([-2, 2]), random.choice([-2, 2])]
    flies.append((fly_rect, fly_velocity))

score = 0

bounce = 0

# Timer variables
message_timer = 0
show_message = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if start_menu:
                if start_rect.collidepoint(event.pos):
                    start_menu = False
                    game_started = True
                elif how_to_play_rect.collidepoint(event.pos):
                    show_instructions = True
            elif game_started:
                for fly_rect, _ in flies:
                    if spatula_rect.colliderect(fly_rect):
                        fly_rect.center = (random.randint(100, 1180), random.randint(100, 808))
                        score += 1
                        if score >= 300:
                            show_message = True
                            message_timer = pygame.time.get_ticks()  # Start the timer

            elif show_instructions:
                show_instructions = False

    spatula_rect = spatula.get_rect()
    spatula_rect.center = pygame.mouse.get_pos()

    if start_menu:
        screen.blit(background, (0, 0))

        # Draw background rectangle behind "Start" button with curved corners
        pygame.draw.rect(screen, (255, 248, 220), start_rect, border_radius=10)
        pygame.draw.rect(screen, (255, 255, 255), start_rect, 5, border_radius=10)

        # Check if the "Start" button is hovered
        if start_rect.collidepoint(pygame.mouse.get_pos()):
            # Enlarge the text
            start_text = font.render('Start', True, (0, 0, 0))
            start_text = pygame.transform.scale(start_text, (int(start_text.get_width() * 1.1), int(start_text.get_height() * 1.1)))
            start_text_rect = start_text.get_rect(center=start_rect.center)
        else:
            start_text = font.render('Start', True, (0, 0, 0))
            start_text_rect = start_text.get_rect(center=start_rect.center)

        screen.blit(start_text, start_text_rect)

        # Draw background rectangle behind "How to Play" button with curved corners
        pygame.draw.rect(screen, (255, 248, 220), how_to_play_rect, border_radius=10)
        pygame.draw.rect(screen, (255, 255, 255), how_to_play_rect, 5, border_radius=10)

        # Check if the "How to Play" button is hovered
        if how_to_play_rect.collidepoint(pygame.mouse.get_pos()):
            # Enlarge the text
            how_to_play_text = font.render('How to Play', True, (0, 0, 0))
            how_to_play_text = pygame.transform.scale(how_to_play_text, (int(how_to_play_text.get_width() * 1.1), int(how_to_play_text.get_height() * 1.1)))
            how_to_play_text_rect = how_to_play_text.get_rect(center=how_to_play_rect.center)
        else:
            how_to_play_text = font.render('How to Play', True, (0, 0, 0))
            how_to_play_text_rect = how_to_play_text.get_rect(center=how_to_play_rect.center)

        screen.blit(how_to_play_text, how_to_play_text_rect)

    elif game_started:
        screen.blit(background, (0, 0))
        screen.blit(spatula, spatula_rect)

        for fly_rect, fly_velocity in flies:
            fly_rect.move_ip(fly_velocity)

            if fly_rect.left < 0 or fly_rect.right > 1280:
                fly_velocity[0] = -fly_velocity[0]
            if fly_rect.top < 0 or fly_rect.bottom > 908:
                fly_velocity[1] = -fly_velocity[1]

            screen.blit(fly, fly_rect)

            if spatula_rect.colliderect(fly_rect):
                fly_rect.center = (random.randint(100, 1180), random.randint(100, 808))
                score += 1
                if score >= 100:
                    show_message = True
                    message_timer = pygame.time.get_ticks()  # Start the timer

        # Render the score
        score_text = font.render(f'Score: {score}', True, (0, 0, 0))
        score_rect = score_text.get_rect(topright=(1250, 20))
        screen.blit(score_text, score_rect)

        if show_message:
            # Render the "Well done! You made Ducky happy!" message
            message_text = font.render('Well done! You made Ducky happy!', True, (0, 0, 0))
            message_rect = message_text.get_rect(center=(640, 454))
            screen.blit(message_text, message_rect)

            # Check if the timer has exceeded 3 seconds
            if pygame.time.get_ticks() - message_timer >= 3000:
                score = 0  # Reset the score
                show_message = False

    elif show_instructions:
        screen.blit(background, (0, 0))

        # Draw background rectangle for instructions with curved corners
        instructions_rect = pygame.Rect(400, 400, 480, 100)
        pygame.draw.rect(screen, (255, 248, 220), instructions_rect, border_radius=10)
        pygame.draw.rect(screen, (255, 255, 255), instructions_rect, 5, border_radius=10)

        # Render the instructions text with black color
        instructions_text = font.render('Smack The Flies To Make Ducky Happy!', True, (0, 0, 0))
        instructions_rect = instructions_text.get_rect(center=(640, 454))
        screen.blit(instructions_text, instructions_rect)

    pygame.display.flip()

    clock.tick(60)

pygame.quit()
