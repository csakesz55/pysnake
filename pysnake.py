import contextlib
with contextlib.redirect_stdout(None):
    import pygame
import time
import keyboard
import random
import os

class App():

    def __init__(self):
        pygame.init()
        self.myfont = pygame.font.SysFont('Segoe UI', 20)
        self.game_over_font = pygame.font.SysFont('Segoe UI', 60)

        self.white = (255,255,255)
        self.grey = (63,63,63)

        #create window
        self.width = 880
        self.height = 680
        self.pd = pygame.display
        self.screen = self.pd.set_mode((self.width, self.height), pygame.DOUBLEBUF)
        self.pd.set_caption('PySnake')
        self.pd.flip()
        self.screen.fill(self.grey)

        if not os.path.isfile("highscore.txt"):
            highscore = open("highscore.txt", "w")
            highscore.write(str(0))
            highscore.close()

    
        self.welcome_screen()
        
        exit = False

        while not exit:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.new_game()
                        exit = True

    def new_game(self):
        game_over = False
        
        read_highscore = open("highscore.txt", "r")
        highscore = int(read_highscore.read())
        read_highscore.close()

        score = 0

        #function call to create a snake with a custom length
        snake = self.create_snake(3)
        food_raw = self.create_food()

        food_coord_x = 0
        food_coord_y = 0
        snake_head_x = 0
        snake_head_y = 0
        self.rects = []

        for i in snake:
            self.rects.append(pygame.draw.rect(self.screen, self.white, i, 1))

        pygame.display.flip()
        #movement
        orientation = (20,0)
        while not game_over:

            self.screen.fill(self.grey)
            self.draw_sides(self.screen)

            text = self.myfont.render('Score: ', False, self.white)
            score_text = self.myfont.render(str(score), False, self.white)
            highscore_text = self.myfont.render('Highscore: ', False, self.white)
            highscore_text_num = self.myfont.render(str(highscore), False, self.white)

            self.screen.blit(text, (40,0))
            self.screen.blit(score_text, (140,0))
            self.screen.blit(highscore_text, (720,0))
            self.screen.blit(highscore_text_num, (820,0))

            food = pygame.draw.rect(self.screen, (255,0,0), food_raw, 2)

            food_coord_x = food.left
            food_coord_y = food.top

            prev_x = 0
            prev_y = 0
            #new_x = 0
            #new_y = 0
            
            press = 0

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and press == 0:
                    press += 1
                    if event.key == pygame.K_LEFT and orientation != (20,0):
                        orientation = (-20,0)
                    elif event.key == pygame.K_RIGHT and orientation != (-20,0):
                        orientation = (20, 0)
                    elif event.key == pygame.K_UP and orientation != (0, 20):
                        orientation = (0, -20)
                    elif event.key == pygame.K_DOWN and orientation != (0, -20):
                        orientation = (0, 20)
                    elif event.key == pygame.K_ESCAPE:
                        game_over = True

            for i in self.rects:
                #tmp_x = i.left
                #tmp_y = i.top

                if i == self.rects[0]:
                    prev_x = i.left
                    prev_y = i.top

                    i.move_ip(orientation)
                    if i.left >= 40 and i.left < 840 and i.top >= 40 and i.top < 640:
                        i = pygame.draw.rect(self.screen, self.white, i, 1)

                    new_x = i.left
                    new_y = i.top
                    #pygame.display.flip()

                    snake_head_x = i.left
                    snake_head_y = i.top

                    if self.snake_food_coll(food_coord_x, food_coord_y, snake_head_x, snake_head_y):
                        self.rects.append(self.grow_snake(prev_x, prev_y, self.screen))
                        food_raw = self.create_food()
                        score += 1

                    if self.area_side_coll(snake_head_x, snake_head_y):
                        game_over = True

                    if self.snake_coll(snake_head_x, snake_head_y, self.rects):
                        game_over = True

                    #game_over = self.snake_food_coll(food_coord_x, food_coord_y, snake_head_x, snake_head_y)
                else:
                    to_x = prev_x - i.left
                    to_y = prev_y - i.top
                    prev_x = i.left
                    prev_y = i.top

                    #print(to_x, to_y, prev_x, prev_y)

                    i.move_ip(to_x, to_y)
                    i = pygame.draw.rect(self.screen, self.white, i, 1)

                    new_x = i.left
                    new_y = i.top
                    #pygame.display.flip()

            pygame.display.flip()
            time.sleep(0.1)
            #print("end of loop")
            #print(prev_x, prev_y)
            #print(self.rects)
            #key = pygame.key.get_pressed()
            #if key[pygame.K_LEFT]:
        if score > highscore:
            write_highscore = open("highscore.txt", "w")
            write_highscore.write(str(score))
            write_highscore.close()

        if game_over:
            self.end_game(score, highscore)
            exit = False

            while not exit:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        exit = True
                        
    def create_snake(self, length):
        snake = []
        x = 400
        y = 300
        for i in range(length):
            new_rect = (x,y,20,20)
            snake.append(new_rect)
            x-=20
        return snake

    def create_food(self):
        x = self.myround(random.randint(40,800))
        y = self.myround(random.randint(40,600))

        food = (x,y,20,20)

        return food

    def grow_snake(self, x, y, screen):
        return pygame.draw.rect(screen, self.white, (x,y,20,20), 1)

    def myround(self, x):
        base = 20
        return int(base * round(float(x)/base))

    def snake_food_coll(self, x, y, x1, y1):
        if x == x1 and y == y1:
            return True

    def area_side_coll(self, x, y):
        if x == 840 or x < 40 or y == 640 or y < 40:
            return True
    
    def snake_coll(self, x, y, rects):
        for i in range(len(rects)-1):
            if x == rects[i+1].left and y == rects[i+1].top:
                return True

    def draw_sides(self, screen):
        pygame.draw.rect(screen, self.white, (40,40,800,600),2)

    def end_game(self, score, highscore):
        self.screen.fill(self.grey)
        self.draw_sides(self.screen)

        game_over_text = self.game_over_font.render('Game Over', False, self.white)
        text = self.myfont.render('Your Score: ', False, self.white)
        score_text = self.myfont.render(str(score), False, self.white)
        highscore_text = self.myfont.render('Highscore: ', False, self.white)
        highscore_text_num = self.myfont.render(str(highscore), False, self.white)
        press_any_text = self.myfont.render("Press any key to exit!", False, self.white)

        self.screen.blit(game_over_text, (300,270))
        self.screen.blit(text, (310,360))
        self.screen.blit(score_text, (420,360))
        self.screen.blit(highscore_text, (460,360))
        self.screen.blit(highscore_text_num, (560,360))
        self.screen.blit(press_any_text, (360,400))

        pygame.display.flip()

    def welcome_screen(self):
        self.screen.fill(self.grey)
        self.draw_sides(self.screen)

        welcome_text = self.game_over_font.render('Welcome to PySnake!', False, self.white)
        press_to_start = self.myfont.render('Press ENTER to start the game!', False, self.white)

        self.screen.blit(welcome_text, (180,270))
        self.screen.blit(press_to_start, (310,360))

        pygame.display.flip()

app = App()