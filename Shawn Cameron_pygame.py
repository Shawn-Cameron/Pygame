import pygame, random
pygame.init()
pygame.font.init()

#sets screen size for both x and y in variables to be used later in the code
screen_sizeX = 800
screen_sizeY = 600

min = 0
max = screen_sizeX
# defines colours to be used in the program
white = (255,255,255)
blue = (0,0,255)
red = (255,0,0)
green = (0,255,0)
black = (0,0,0)
purple =(153,0,153)
dark_red = (200,0,0)
dark_purple = (130,0,130)

size = (screen_sizeX,screen_sizeY)
screen = pygame.display.set_mode(size)
screen.fill(white)

#uploads images to be used in the game
spaceship = pygame.image.load('spaceship (2).png')
background = pygame.image.load('spacebackground2.jpg')
pausedbg = pygame.image.load('spacebackground2 - Copy.jpg')
startbackground = pygame.image.load('spacestartingscreen.jpg')

clock = pygame.time.Clock()
pygame.display.set_caption("Space Bound")


#needed to be definded before the functions ran to allow pause functionallity
pause = False

def mainmusic():
    pygame.mixer.music.load('Clutch.mp3')
    pygame.mixer.music.play()
    pygame.mixer.music.set_volume(0.5)
    
#allows quit to be used in button function
def quitgame():
    pygame.quit()
    quit()
    
#allows unpause functionallity to be used in button function    
def unpause():
    global pause
    pause = False
    
#when the user presses p this loop will stop the game from continuing     
def paused():
    global pause
    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type ==  pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    pause = False
                
        screen.blit(pausedbg,[0,0])
        screen_message("Paused")
        #the button the user presses will run the corresponding function
        button("Continue",200,purple,dark_purple,unpause)
        button("Quit!",500,red,dark_red,quitgame)
        pygame.display.update()
        clock.tick(10)

# button function allows certian functions to run when the user presses the corresponding button
def button(msg,x,act,inact,action = None):
    mouse = pygame.mouse.get_pos()
    mouse_click = pygame.mouse.get_pressed()
    if x+100 > mouse[0] > x and 400+50 > mouse[1]> 400:#allows the button to change colour when the mouse is over
        pygame.draw.rect(screen,act,[x,400,100,50])    #the button and allows the function to run when the user
        if mouse_click[0]== 1 and action == game:      #uses left click
            mainmusic()#changes music when the user clicks on the game button in starting screen
        if mouse_click[0] == 1 and action != None:
            action()
    else:
        pygame.draw.rect(screen,inact,[x,400,100,50])
    #creates text over each of the buttons
    Text = pygame.font.Font("freesansbold.ttf",20)
    surface,textbox = text_obj(msg,Text)
    textbox.center = (x+50,425)
    screen.blit(surface,textbox)

def startingscreen():
    pygame.mixer.music.load('Astral Projection.mp3')#opening music
    pygame.mixer.music.play()
    pygame.mixer.music.set_volume(0.5)
    start = False
    while not start: #allows the starting screen to remain on untill the user clicks a button
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                
        screen.blit(startbackground,[0,0])
        screen_message("Space Bound")

        button("Start!",200,purple,dark_purple,game)# runs the game when clicked
        button("Quit!",500,red,dark_red,quitgame)

        
        pygame.display.update()
        clock.tick(10) #sets fps at a low rate to avoid program crash

        

def text_obj(text,font):#used for text in each text function
    textsurface = font.render(text,True,white)
    return textsurface, textsurface.get_rect()

# 3 different funtions for displaying 3 different types text
def screen_message(text):
    largeText = pygame.font.Font('freesansbold.ttf',80)
    surface,textbox = text_obj(text,largeText)
    textbox.center=((screen_sizeX/2),(screen_sizeY/2))
    screen.blit(surface,textbox)

def screen_message2(text):
    mediumText = pygame.font.Font('freesansbold.ttf',40)
    surface,textbox = text_obj(text,mediumText)
    textbox.center=((screen_sizeX/2),(screen_sizeY/2 + 100))
    screen.blit(surface,textbox)

def screen_score(score):
    smallText = pygame.font.Font('freesansbold.ttf',20)
    surface,textbox = text_obj("Score:"+str(score),smallText)
    textbox =(0,0)
    screen.blit(surface,textbox)
    
    #both creates random positions for each enemy and stores them in a list
def Xenemylocation():
    locationXe = []
    min = 0
    max = 100
    for a in range(0,4):
        b = random.randint(min,max)
        locationXe.append(b)
        min += 200 #after a number is appened to the list the range will change to avoid enemies from overlapping to
        max += 200 #make the game harder
    return locationXe

def Yenemylocation():
    locationYe = []
    min = 0
    max = 100
    for a in range(0,4):
        b = random.randint(min,max)
        locationYe.append(b)
        min += 125
        max += 125
    return locationYe
    
def charater(x,y):# allows character to be projected to the screen
    screen.blit(spaceship,(x,y))

def enemy(coorX,coorY,x,y):#creates each enemy and draws the changed location
    for a in range(0,4):
        pygame.draw.rect(screen,blue,[x[a],coorY,100,40])#draws each enemy with the locations it recieved from the lists
        pygame.draw.rect(screen,blue,[coorX,y[a],30,80])
    pygame.display.update()
    
def died(score):#runs when there is collision and restarts the game after 2 seconds
    screen_message2('Your score is '+ str(score))
    screen_message('You have been killed')
    pygame.display.update()
    pygame.time.delay(2000)
    game()
    
def collision(downEnemyX,downEnemyY,sideEnemyX,sideEnemyY,charaterX,charaterY,score):
    for a in range(0,4): #checks for collision between the different sides of the charater and all of the sides of the enemies
        if charaterY + 30 < downEnemyY + 40 and charaterY + 30 > downEnemyY or charaterY + 80 > downEnemyY and charaterY + 80 < downEnemyY + 40: 
            if charaterX > downEnemyX[a] and charaterX < downEnemyX[a] + 100 or charaterX + 80 > downEnemyX[a] and charaterX + 80 < downEnemyX[a] + 100:
                died(score)
        
        if charaterY < downEnemyY + 40 and charaterY > downEnemyY:
            if charaterX + 30 > downEnemyX[a] and charaterX + 30 < downEnemyX[a] + 100 or charaterX + 50 > downEnemyX[a] and charaterX + 50 < downEnemyX[a] + 100:
                died(score)

                    
        if charaterX + 30 < sideEnemyX + 30 and charaterX + 30 > sideEnemyX or charaterX + 50 > sideEnemyX and charaterX + 50 < sideEnemyX + 30:
            if charaterY  > sideEnemyY[a] and charaterY < sideEnemyY[a] + 80 or charaterY + 30 > sideEnemyY[a] and charaterY + 30 < sideEnemyY[a] + 80:
                died(score)
                

            
        if charaterX < sideEnemyX + 30 and charaterX > sideEnemyX or charaterX + 80 > sideEnemyX and charaterX + 80 < sideEnemyX + 30:
            if charaterY + 30 > sideEnemyY[a] and charaterY + 30 < sideEnemyY[a] + 80 or charaterY + 80 > sideEnemyY[a] and charaterY + 80 < sideEnemyY[a] + 80:
                died(score)

                

def game():
    global pause
    #predefined to allow character movement  
    x = (screen_sizeX * 0.45)
    y = (screen_sizeY * 0.8)
    x_change = 0
    y_change = 0
    #must equal to -2 for the real score to start at 0
    score = -2

    #enemies start at this location to alow the random location generator to run at the start of the game
    coorY = 600
    coorX = 800
    done = False
    collided = 0
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            #allows character to move in all directions
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    y_change = -5
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    y_change = 5
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    x_change = -5
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    x_change = 5
                if event.key == pygame.K_p:
                    pause = True
                    paused()
            #stops the character from moving when the user releases the key
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN or event.key == pygame.K_w or event.key == pygame.K_s:
                    y_change = 0
                elif event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_a or event.key == pygame.K_d:
                    x_change = 0
        #continuously adds the change to the location of the character
        x += x_change
        y += y_change
        #give the character screen boundaries
        if x <= 0:
            x = 0
        if x >= screen_sizeX - 80:
            x = screen_sizeX - 80
        if y <= 0:
            y = 0
        if y >= screen_sizeY - 80:
            y = screen_sizeY - 80
            
        screen.blit(background,[0,0])
        charater(x,y)
        screen_score(score)# prints the score on the screen
        #both causes the locations of each enemy to be generated when they reach or pass 600/800
        #locations start here to allow is part of the program to run
        #score must start at -2 because both will run adding 2 to the score at the start
        if coorY >= 600:
            score += 1
            locationsX = Xenemylocation()
            coorY = -100
   
        if coorX >= 800:
            score += 1
            locationsY = Yenemylocation()
            coorX = -100

        #checks for collision between the charater and the enemies
        collision(locationsX,coorY,coorX,locationsY,x,y,score)
        #takes in the location lists and the changing locations
        enemy(coorX,coorY,locationsX,locationsY)
        coorX += 3
        coorY += 3
        pygame.display.update()
        clock.tick(100)
    if done:
        pygame.quit()
        quit()

#startingscreen calls the other functions
startingscreen()
