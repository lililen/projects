#ProJ 3 for Resume Game Aim Trainer 
#Inspired by Rhythm Games
#Status: Finished

import pygame
import random
import math
import time

pygame.init()

# screen setup + colors 
WIDTH, HEIGHT = 900, 725
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Aim Trainer Game-Hit Circles as Close to Center in 30seconds!")

white = (255, 255, 255)
red = (255, 0, 0)
orange = (255, 140, 0)
yellow = (255, 255, 0)
black = (0, 0, 0)

# Target radius size
outter_circle = 50  # 1pt
middle_circle = 30  # 3pts
center_circle = 10  # 5pt


# Game settings/default settings
FPS = 60  
timer = 30  
font = pygame.font.SysFont(None, 36)

# default counter for varibles in game such as overall score += and total clicks 
score = 0
clicks = 0
game_over = False
start_time = time.time()

# use random.randint to generate a random position within the screen boundaries
def random_position():
    x = random.randint(outter_circle, WIDTH - outter_circle)
    y = random.randint(outter_circle, HEIGHT - outter_circle)
    return (x, y)

# calculate distance between two points
def distance(point1, point2):
    return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)

# Draw target design and position 
def target(position):
    pygame.draw.circle(screen, yellow, position, outter_circle)   
    pygame.draw.circle(screen, orange, position, middle_circle) 
    pygame.draw.circle(screen, red, position, center_circle)   

# calculate score based on clicks within the radius += # of points earned for that radius 
def calculate_score(position, click_position):
    d = distance(position, click_position)
    if d <= center_circle:
        return 5  
    elif d <= middle_circle:
        return 3  
    elif d <= outter_circle:
        return 1  
    else:
        return 0  # Missed the target/circle 

# Main game loop
def game_loop():
    global score, clicks, game_over
   
   
    # Initial target position
    target_position = random_position()

    clock = pygame.time.Clock()

    while not game_over:
        screen.fill(white)  #white background for the game

        for event in pygame.event.get():
            if event.type ==pygame.QUIT:
                game_over = True  # Quit the game if quit
            elif event.type == pygame.MOUSEBUTTONDOWN:
                clicks += 1  # count the num of clicks
                click_position = pygame.mouse.get_pos()

                # add score and respawn the circle at random 
                score += calculate_score(target_position, click_position)
                target_position = random_position()  

        # Draw the target at random position
        target(target_position)

        # Display interface for the overall score and timer during game
        elapsed_time = time.time() - start_time
        time_left = max(0, timer - int(elapsed_time))
        score_text = font.render(f"Score: {score}", True, black)
        timer_text = font.render(f"Time: {time_left}s", True, black)
        screen.blit(score_text, (10, 10))
        screen.blit(timer_text, (WIDTH - 150, 10))

        # end game if time runs out bool
        if time_left <= 0:
            game_over = True

        pygame.display.flip()  # update the screen
        clock.tick(FPS)  # maintain the frame rate

    # display final score screen after game_over = True 
    screen.fill(white)
    final_score_text = font.render(f"Final Score: {score}", True, black)
    accuracy_text = font.render(f"Accuracy: {round((score / (clicks * 5)) * 100, 2)}%", True, black)
    screen.blit(final_score_text, (WIDTH // 2 - 100, HEIGHT // 2 - 20))
    screen.blit(accuracy_text, (WIDTH // 2 - 100, HEIGHT // 2 + 20))
    pygame.display.flip()

    # display score time frame before quitting the program 
    time.sleep(2.5)
    pygame.quit()

game_loop()