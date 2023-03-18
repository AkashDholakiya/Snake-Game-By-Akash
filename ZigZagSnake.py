import pygame
import random
import os

pygame.mixer.init()
pygame.init()   

#RGB value for colors
white = (255 ,255, 255) 
red = (255,0,0)
black = (0,0,0)
blue = (0,0,255)
green = (0,255,0)
# creating window
screen_width = 1500
screen_height = 800
gameWindow = pygame.display.set_mode((screen_width,screen_height))


#backgroung image 
bgimg = pygame.image.load('images/backimg.jpg')
bgimg = pygame.transform.scale(bgimg, (screen_width,screen_height)).convert_alpha()
fbgimg = pygame.image.load('images/SGBA.jpg')
fbgimg = pygame.transform.scale(fbgimg, (screen_width,screen_height)).convert_alpha()
limg = pygame.image.load('images/Lost.jpg')
limg = pygame.transform.scale(limg, (screen_width,screen_height)).convert_alpha()


pygame.display.set_caption("ZigZag Snake")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None,55)
pygame.display.update() 

def score_screen(text,color,x,y):
    screen_text = font.render(text,True,color)
    gameWindow.blit(screen_text, [x,y])
    
def plot_snake(gameWindow,color,snk_list,snake_size):    
    for x,y in snk_list:
        #for rectangle snake
        # pygame.draw.rect(gameWindow, blue , [x,y,snake_size,snake_size])
        #for circle snake
        pygame.draw.circle(gameWindow, blue , [x,y],15)
def welcome():
    exit_game = False
    while not exit_game:
        gameWindow.fill(white)
        gameWindow.blit(fbgimg, (0,0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pygame.mixer.music.load('music/back.mp3')
                    pygame.mixer.music.play(-1)
                    gameloop()
            
        pygame.display.update()
        clock.tick(60)
#creating game loop
def gameloop():
    #game specific variables
    if(not os.path.exists("highscore.txt")):
        with open("highscore.txt","w") as f:
             f.write("0")
    with open("highscore.txt","r") as f:
        highscore = f.read()
    exit_game = False
    game_over = False
    snake_x = screen_width/2
    snake_y = screen_height/2
    food_x = random.randint(30,screen_width/2)
    food_y = random.randint(30,screen_height/2)
    velocity_x = 0
    velocity_y = 0
    snake_size = 30
    fps  = 30
    initial_velocity = 5
    definer1 = True
    definer2 = True
    definer3 = True
    score = 0        
    snk_length = 1
    snk_list = []
    while not exit_game:
        if game_over:
            with open("highscore.txt","w") as f:
                f.write(str(highscore)) 
            gameWindow.fill(white)
            gameWindow.blit(limg, (0,0))
            score_screen("highscore = " + str(highscore),white,5,5)
            score_screen("your score = " + str(score),white,5,50)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        welcome()
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True
                    
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT and definer1:
                        velocity_x = initial_velocity
                        definer1 = False
                        definer3 = True
                        definer2 = True
                        
                    if event.key == pygame.K_LEFT and definer1:
                        velocity_x = -initial_velocity
                        definer1 = False 
                        definer2 = True
                        definer3 = True
                        
                    if event.key == pygame.K_UP and definer2: 
                        velocity_y = -initial_velocity
                        definer1 = True
                        definer2 = False
                        definer3 = False
                        
                    if event.key == pygame.K_DOWN and definer2:
                        velocity_y = initial_velocity
                        definer1 = True
                        definer2 = False
                        definer3 = False
            if definer3:
                snake_x += velocity_x
            else:
                snake_y += velocity_y
                
            if abs(snake_x - food_x) < snake_size and abs(snake_y - food_y) < snake_size:
                score += 10
                food_x = random.randint(30,screen_width/2)
                food_y = random.randint(30,screen_height/2)
                beep = pygame.mixer.Sound('music/beep.mp3')
                beep.play()
                initial_velocity += 0.12
                snk_length += 2
                if score > int(highscore):
                    highscore = score
                
                
            gameWindow.fill(white)
            gameWindow.blit(bgimg, (0,0))
            score_screen("score = " + str(score) + ',' + " highscore = " + str(highscore),black,5,5)
            #for rectangle food 
            # pygame.draw.rect(gameWindow, red , [food_x,food_y,snake_size,snake_size])
            #for circle food
            pygame.draw.circle(gameWindow, red , [food_x,food_y],15)
            head = []
            head.append(snake_x)
            head.append(snake_y)
            snk_list.append(head)
            
            if len(snk_list) > snk_length:
                del snk_list[0]
            
            if head in snk_list[:-1]:
                game_over = True
                pygame.mixer.music.load('music/gamelost.mp3')
                pygame.mixer.music.play()
            
            if snake_x < 0 or snake_x > screen_width or snake_y < 0 or snake_y > screen_height:
                game_over = True
                pygame.mixer.music.load('music/gamelost.mp3')
                pygame.mixer.music.play()
            
            plot_snake(gameWindow,green,snk_list,snake_size)
        pygame.display.update()
        clock.tick(fps)
        
    pygame.quit()
    try:
        if pygame.quit():
            quit()
    except quit():
        pass
welcome()