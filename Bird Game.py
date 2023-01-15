# Abhin Tomar
# Bird Flying Sim
# This game was made using pygame and it involves collecting and avoiding certain objects
# in order to keep the bird's stamina and health up as well as trying to collect as many
# points as you can.

# importing external modules
import pygame,sys,random,time

#global variable section
floor_x_pos = 0
width = 1200
height = 600
gravity = 0.025
birdMovement = 0
coinsCollected = 0
starsCollected = 0
berriesCollected = 0
bombsHit = 0
tPoints = 0
red = (255,0,0)
green = (0,255,0)
white = (255,255,255)
black = (0,0,0)
redB = (255,0,0)
greenB = (0,255,0)
blueB = (0,0,255)
hbarLength = 450
sbarLength = 450
iTime = time.time()
eTime = time.time() - iTime
startGame = False
restart = False
outofBounds = False
htp = False

pygame.init()  # initializes pygame
screen = pygame.display.set_mode((width,height))      # creates screen for the game
pygame.display.set_caption("Bird Flying Simulator")   # sets game caption

clock = pygame.time.Clock()  # manages FPS

# getting images and rescaling them to certain sizes
bgSurface = pygame.image.load('gameBackground.jpg').convert()
bgSurface = pygame.transform.scale2x(bgSurface)

floor = pygame.image.load('bottom.png').convert()
floor = pygame.transform.scale(floor,(width,150))

htpSurface = pygame.image.load('htpScreen.png').convert()
htpSurface = pygame.transform.scale(htpSurface,(width,450))

coinSurface = pygame.image.load('coin21.png').convert_alpha()
coinSurface = pygame.transform.scale(coinSurface,(60,60))
coinList = []

# the event "SPAWNCOIN" occurs once every 3 seconds
SPAWNCOIN = pygame.USEREVENT
pygame.time.set_timer(SPAWNCOIN, 3000)

bombSurface = pygame.image.load('bomb21.png').convert_alpha()
bombSurface = pygame.transform.scale(bombSurface,(75,60))
bombList = []

berrySurface = pygame.image.load('berry1.png').convert_alpha()
berrySurface = pygame.transform.scale(berrySurface,(60,60))
berryList = []

starSurface = pygame.image.load('starr.png').convert_alpha()
starSurface = pygame.transform.scale(starSurface,(60,60))
starList = []

# 3 types of bird images
birdNormal = pygame.image.load('midFlap.png').convert_alpha()
birdNormal = pygame.transform.scale(birdNormal,(120,40))

birdUp = pygame.image.load('wingUp.png').convert_alpha()
birdUp = pygame.transform.scale(birdUp,(120,60))

birdDown = pygame.image.load('wingDown.png').convert_alpha()
birdDown = pygame.transform.scale(birdDown,(120,60))

birdRect = birdNormal.get_rect(center = (400,200))    # hitbox for bird

# sounds
oobSound = pygame.mixer.Sound("oob.wav")
oobSound.set_volume(0.5)
coinSound = pygame.mixer.Sound("coin2.wav")
berrySound = pygame.mixer.Sound("berry1.mp3")
starSound = pygame.mixer.Sound("coin.wav")
bombSound = pygame.mixer.Sound("bomb.wav")
bombSound.set_volume(0.3)

# draws floor with animations
def drawFloor():
    screen.blit(floor,(floor_x_pos,450))
    screen.blit(floor,(floor_x_pos + width,450))

# creates and returns a coin everytime it's called
def createCoin():
    newCoin = coinSurface.get_rect(midtop = (1300,random.randint(0,390)))
    return newCoin

# moves the coins to the left at a certain speed
def moveCoin(coins):
    for coin in coins:
        coin.centerx -= 2
    return coins

# draws the coins to the screen
def drawCoin(coins):
    for coin in coins:
        screen.blit(coinSurface,coin)

# creates and returns a bomb everytime it's called
def createBomb():
    newBomb = bombSurface.get_rect(midtop = (random.randint(1350,1600),random.randint(0,390)))
    return newBomb

# moves the bombs to the left at a certain speed
def moveBomb(bombs):
    for bomb in bombs:
        bomb.centerx -= 3
    return bombs

# draws the bombs to the screen
def drawBomb(bombs):
    for bomb in bombs:
        screen.blit(bombSurface,bomb)

# creates and returns a berry everytime it's called
def createBerry():
    newBerry = berrySurface.get_rect(midtop = (random.randint(1350,1500),random.randint(0,390)))
    return newBerry

# moves the berries to the left at a certain speed
def moveBerry(berries):
    for berry in berries:
        berry.centerx -= 2
    return berries

# draws the berries to the screen
def drawBerry(berries):
    for berry in berries:
        screen.blit(berrySurface,berry)

# creates and returns a star everytime it's called
def createStar():
    newStar = starSurface.get_rect(midtop = (random.randint(1350,1600),random.randint(0,390)))
    return newStar

# moves the stars to the left at a certain speed
def moveStar(stars):
    for star in stars:
        star.centerx -= 4
    return stars

# draws the stars to the screen
def drawStar(stars):
    for star in stars:
        screen.blit(starSurface,star)

# Checks if the bird collides with the coin  
def getsCoin():
    global coinsCollected
    global hbarLength
    global sbarLength
    collide = birdRect.collidelist(coinList)

    if (collide != -1):
        pygame.mixer.Sound.play(coinSound)   # plays sound
        coinsCollected += 1                  # increments coins collected by 1 each time
        hbarLength += 40                     # adds health
        sbarLength += 10                     # adds stamina
        coinList.remove(coinList[collide])  # removes that coin from the list

# Checks if the bird collides with the berry 
def getsBerry():
    global berriesCollected
    global hbarLength
    global sbarLength
    collide = birdRect.collidelist(berryList)

    if (collide != -1):
        pygame.mixer.Sound.play(berrySound)
        berriesCollected += 1
        hbarLength += 10
        sbarLength += 50
        berryList.remove(berryList[collide])

# Checks if the bird collides with the star 
def getsStar():
    global starsCollected
    global hbarLength
    global sbarLength
    collide = birdRect.collidelist(starList)

    if (collide != -1):
        pygame.mixer.Sound.play(starSound)
        starsCollected += 1
        hbarLength += 80
        sbarLength += 100
        starList.remove(starList[collide])

# Checks if the bird is out of bounds
def birdOutofBounds():
    # all global variables used
    global birdRect
    global hbarLength
    global outofBounds
    global iTime
    global coinList
    global berryList
    global starList
    global bombList
    global birdMovement

    # If the bird is not out of bounds already, checks to see if it is
    # out of bounds using its y coordinates
    if not outofBounds:
        if birdRect.top <= 0 or birdRect.bottom >= 450:
            birdRect.centery = 200      # recenters the bird
            pygame.mixer.Sound.play(oobSound)
            hbarLength -= 150
            pygame.time.wait(100)       # small delay of 0.1 seconds

            # after the delay, the objects are all reset 
            # so the user can easily restart
            birdMovement = 0            
            del coinList[:]
            del berryList[:]
            del starList[:]
            del bombList[:]
            outofBounds = True

# checks if bird is in bounds
def birdInBounds():
    global birdRect
    global outofBounds
    
    if birdRect.top > 0 and birdRect.bottom < 450:
        outofBounds = False          # changes value of "outofBounds" depending on its y-coord

# checks if each of the objects overlap with one another 
def overlap(coins,bombs,berries,stars):

    # uses for loops to check for each object inside the object's list and uses
    # their positions to check if they will collide
    for coin in coins:
        for bomb in bombs:
            if (coin.centery + 60) >= bomb.centery >= (coin.centery - 60) and bomb.centerx >= 1230:
                # if true, changes the y-coord of one of the objects to a random number
                bomb.top = random.randint(0,390)
    for coin in coins:
        for star in stars:
            if (coin.centery + 70) >= star.centery >= (coin.centery - 70) and star.centerx >= 1230:
                star.top = random.randint(0,390)
    for berry in berries:
        for bomb in bombs:
            if (berry.centery + 70) >= bomb.centery >= (berry.centery - 70) and bomb.centerx >= 1230:
                bomb.top = random.randint(0,390)
    for star in stars:
        for bomb in bombs:
            if (star.centery + 70) >= bomb.centery >= (star.centery - 70) and star.centerx >= 1230:
                star.top = random.randint(0,390)
    for star in stars:
        for berry in berries:
            if (berry.centery + 70) >= star.centery >= (berry.centery - 70) and star.centerx >= 1230:
                star.top = random.randint(0,390)
    for coin in coins:
        for berry in berries:
            if (coin.centery + 70) >= berry.centery >= (coin.centery - 70) and berry.centerx >= 1230:
                berry.top = random.randint(0,390)

# Checks if any objects have passed the screen. If true, removes the certain
# object. This function makes the overlap() function much more efficient and 
# faster.
def passedObjects(coins,bombs,berries,stars):

    for coin in coins:
        if coin.centerx < -30:
            coins.remove(coin)
    for berry in berries:
        if berry.centerx < -30:
            berries.remove(berry)
    for star in stars:
        if star.centerx < -30:
            stars.remove(star)
    for bomb in bombs:
        if bomb.centerx < -30:
            bombs.remove(bomb)

# Checks if bird hits a bomb. If true, removes the bomb
# from the list
def hitsBomb():
    global hbarLength
    global bombsHit
    collide = birdRect.collidelist(bombList)

    if (collide != -1):
        pygame.mixer.Sound.play(bombSound)
        bombList.remove(bombList[collide])
        bombsHit += 1
        hbarLength -= 150

# makes sure that the bars cannot exceed their original length of 450
def maxBar():
    global hbarLength
    global sbarLength
    if hbarLength > 450:
        hbarLength = 450
    if sbarLength > 450:
        sbarLength = 450

# Changes the bird image used based on its vertical movement
def wingMovement():
    global birdMovement
    global birdRect
    if birdMovement > 0:
        birdRect = birdDown.get_rect(center = (birdRect.centerx,birdRect.centery))   # wings down
        screen.blit(birdDown, birdRect)
    elif birdMovement < 0:
        birdRect = birdUp.get_rect(center = (birdRect.centerx,birdRect.centery))    # wings up
        screen.blit(birdUp, birdRect)
    else:
        birdRect = birdNormal.get_rect(center = (birdRect.centerx,birdRect.centery)) # normal image
        screen.blit(birdNormal, birdRect)    

# creates the health bar using rect and text
def healthBar():
    global hbarLength
    healthBar = pygame.Rect(20, 505, hbarLength, 60)
    pygame.draw.rect(screen,white,pygame.Rect(20,505,450,60))
    pygame.draw.rect(screen,red,healthBar)
    pygame.draw.rect(screen,black,pygame.Rect(20,505,450,60),5)
    hFont = pygame.font.SysFont('Arial_Black', 50)
    hText = hFont.render("HEALTH", True, (0,0,0))
    screen.blit(hText, (130, 500))

# creates the stamina bar using rect and text
def staminaBar():
    global sbarLength
    stamBar = pygame.Rect(730, 505, sbarLength, 60)
    pygame.draw.rect(screen,white,pygame.Rect(730,505,450,60))
    pygame.draw.rect(screen,green,stamBar)
    pygame.draw.rect(screen,black,pygame.Rect(730,505,450,60),5)
    sFont = pygame.font.SysFont('Arial_Black', 50)
    sText = sFont.render("STAMINA", True, (0,0,0))
    screen.blit(sText, (830, 500))

# Determines the look of the start screen
def startScreen():
    # floor + background
    global floor_x_pos
    screen.blit(bgSurface,(0,0))
    floor_x_pos -= 1
    drawFloor()
    if floor_x_pos <= -width:
        floor_x_pos = 0

    # game title
    sFont = pygame.font.SysFont('Arial_Black', 82)
    sText = sFont.render("BIRD FLYING SIMULATOR", True, (0,0,0))
    screen.blit(sText, (20,0))
    
    # extra images that may help user understand the game better
    screen.blit(birdNormal,(100,250))
    screen.blit(birdUp,(280,140))
    screen.blit(birdDown,(420,310))
    screen.blit(coinSurface,(770,255))
    screen.blit(berrySurface,(900,150))
    screen.blit(starSurface,(900,350))
    screen.blit(bombSurface,(1030,250))

# Requires 4 parameters (3 buttons and the mouse position)
def buttons(s,i,e,m):
    global greenB
    global blueB
    global redB
    
    # highlights the certain button if the mouse is hovering over it
    if s.collidepoint(m):
        greenB = (127,255,0)
    else:
        greenB = (0,255,0)

    if i.collidepoint(m):
        blueB = (30,144,255)
    else:
        blueB = (0,0,255)

    if e.collidepoint(m):
        redB = (255,91,71)
    else:
        redB = (255,0,0)

# Gets the progress using the elapsed time and displays
# it on the top right corner of the play screen
def progress():
    global eTime
    progress = int(eTime * 2)
    pFont = pygame.font.SysFont('Arial_Black', 20)
    pText = pFont.render("%d" % progress, True, (0,0,0))
    screen.blit(pText, (1040,0))

    p2Font = pygame.font.SysFont('Arial_Black', 20)
    p2Text = p2Font.render("% complete", True, (0,0,0))
    screen.blit(p2Text, (1070,0))

# Creates the end screen. Takes 2 parameters : end screen text and an outcome
# (1 for lose, 0 for win)   
def endScreen(s,outcome):
    global gravity
    global birdMovement
    global birdRect
    global tPoints
    global hbarLength
    global sbarLength

    # sets volume of out of bounds sound to 0 
    # changes bird pos so it cannot be seen on screen
    oobSound.set_volume(0.0)
    birdRect.center = (4000,2000)
    # redraws floor and background over the screen
    screen.blit(bgSurface,(0,0))
    drawFloor()
    gravity = 0
    birdMovement = 0

    # displays win/lose text
    wFont = pygame.font.SysFont('Arial_Black', 100)
    wText = wFont.render(s, True, (0,0,0))
    if s == "You Win!":
        screen.blit(wText, (390,50))
    else:
        screen.blit(wText, (350,50))

    # displays and creates restart and exit buttons
    restartButton = pygame.Rect(150,505,350,60)
    exitButton = pygame.Rect(700,505,350,60)
    extraButton = pygame.Rect(7000,5050,350,60)
    pygame.draw.rect(screen,greenB,restartButton)
    pygame.draw.rect(screen,redB,exitButton)
    
    # Text for buttons
    bFont = pygame.font.SysFont('Arial_Black', 40)
    bText = bFont.render("PLAY AGAIN                             EXIT", True, (0,0,0))
    screen.blit(bText, (185,505))

    # Displays total points at the end of the game
    pFont = pygame.font.SysFont('Arial_Black', 30)
    pText = pFont.render("Total Points :", True, (0,0,0))
    screen.blit(pText, (150,380))

    p1Text = pFont.render("%d" % tPoints, True, (0,0,0))
    screen.blit(p1Text, (380,380))
    
    lFont = pygame.font.SysFont('Arial_Black', 40)
    if outcome == 1:    # if user loses
        # finds out why they lost based on the bar lengths 
        # and displays the reason 
        if hbarLength <= 0:
            lText = lFont.render("Reason : No Health", True, (0,0,0))
            screen.blit(lText, (430,230))
        elif sbarLength <= 0:
            lText = lFont.render("Reason : No Stamina", True, (0,0,0))
            screen.blit(lText, (420,230))
    else:
        # if user wins, displays "Great Work!"
        lText = lFont.render("Great Work!", True, (0,0,0))
        screen.blit(lText, (510,230))

    # displays high score
    sFont = pygame.font.SysFont('Arial_Black', 30)
    sText = sFont.render("High Score: ", True, (0,0,0))
    screen.blit(sText, (800,380))

    hsText = sFont.render("%d" % highScore(tPoints), True, (0,0,0))
    screen.blit(hsText, (1000,380))

    # gets mouse position
    m = pygame.mouse.get_pos()
    
    for event in pygame.event.get():
        
        # exits program
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # if user clicks on restart button, returns True
        # if user clicks on exit button, program ends and window closes
        if event.type == pygame.MOUSEBUTTONUP:
            if restartButton.collidepoint(m):
                return True
            if exitButton.collidepoint(m):
                pygame.quit()
                sys.exit()

    # calls button highlighting function
    # the extra button is never used
    buttons(restartButton,extraButton,exitButton,m)

# checks if any of the bars are 0. If True, changes the 
# total points to 0 and returns True. Otherwise, returns
# False
def barZero():
    global hbarLength
    global sbarLength
    global tPoints

    if hbarLength <= 0:
        tPoints = 0
        return True
    elif sbarLength <= 0:
        tPoints = 0
        return True
    else:
        return False

# Gets and displays points onto screen
def points(c,b,s,be):
    global tPoints
    tPoints = (c) + (2*be) + (5*s) - (3*b)   # calculates points using objects collected
    text_x_pos = 30

    # displays points on top left corner of play screen
    pFont = pygame.font.SysFont('Arial_Black', 20)
    pText = pFont.render("%d" % tPoints, True, (0,0,0))
    screen.blit(pText, (10,0))

    # reformats text 
    if tPoints >= 10:
        text_x_pos = 45
    else:
        text_x_pos = 30

    tFont = pygame.font.SysFont('Arial_Black', 20)
    tText = tFont.render("Points", True, (0,0,0))
    screen.blit(tText, (text_x_pos,0))

# returns current highscore using a text file
def highScore(score):
    # opens and reads text file to get original highscore
    with open ("highScore.txt", "r") as f: 
        highScore = f.read()
    # if file is empty, highscore is 0
    if highScore == "":
        highScore = 0

    # if the score becomes greater than current highscore, then the highscore
    # becomes the score
    if score > int(highScore):
        highScore = score

    # writes the new high score to the file as a string
    with open ("highScore.txt", "w") as f:
        f.write(str(highScore))

    # returns integer value of the high score
    return int(highScore)

# how to play screen function, needs a mouse as its parameter
def htpScreen(m):
    # displays floor and the how to play screen which is an image
    # imported from a google slides which contains all of the text
    global floor_x_pos
    global greenB
    screen.blit(htpSurface,(0,0))
    floor_x_pos -= 1
    drawFloor()
    if floor_x_pos <= -width:
        floor_x_pos = 0
    
    # creates return button
    retButton = pygame.Rect(350,505,500,60)
    pygame.draw.rect(screen,greenB,retButton)

    # highlights button if mouse is hovering over it
    if retButton.collidepoint(m):
        greenB = (127,255,0)
    else:
        greenB = (0,255,0)

    # text on button
    rFont = pygame.font.SysFont('Arial_Black', 40)
    rText = rFont.render("RETURN", True, (0,0,0))
    screen.blit(rText, (510,505))

    # return the button (rect)
    return retButton

# start menu
while startGame == False:  # while the game hasn't started
    # gets mouse position
    mouse = pygame.mouse.get_pos()

    # while the user is on the how to play screen
    while htp == True:
        mouse = pygame.mouse.get_pos()

        for event in pygame.event.get():   

            # exits program
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # if user clicks return, exits out of this while loop by making htp = False
            if event.type == pygame.MOUSEBUTTONUP:
                if htpScreen(mouse).collidepoint(mouse):
                    htp = False
        
        # displays how to play screen
        htpScreen(mouse)

        # constantly updates screen
        pygame.display.update()
        clock.tick(120)          # framerate
    
    for event in pygame.event.get():   

        # exits program
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        # if user clicks start button, exits out of this while loop 
        # and program enter the game loop
        if event.type == pygame.MOUSEBUTTONUP:
            if startButton.collidepoint(mouse):
                startGame = True
                iTime = time.time()   # gets the time spent on the start screen
            # if user clicks HTP button, enters the above while loop
            if insButton.collidepoint(mouse):
                htp = True
            # exits program if exit button is pressed
            if exitButton.collidepoint(mouse):
                pygame.quit()
                sys.exit()

    # display start screen
    startScreen()
    # draw buttons
    startButton = pygame.Rect(20,505,350,60)
    insButton = pygame.Rect(420,505,350,60)
    exitButton = pygame.Rect(820,505,350,60)
    pygame.draw.rect(screen,greenB,startButton)
    pygame.draw.rect(screen,blueB,insButton)
    pygame.draw.rect(screen,redB,exitButton)
    
    # button text
    bFont = pygame.font.SysFont('Arial_Black', 40)
    bText = bFont.render("PLAY               HOW TO PLAY               EXIT", True, (0,0,0))
    screen.blit(bText, (130,505))

    # highlighting buttons function
    buttons(startButton,insButton,exitButton,mouse)

    # updates screen
    pygame.display.update()
    clock.tick(120)      # framerate

# game loop (runs only after the above while loop ends)
while True:
    # gets elapsed time by subtracting total time by time spent on start screen
    eTime = time.time() - iTime
    
    for event in pygame.event.get():   # event loop

        # exits program
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # moves bird up and down based on key inputs
        # also removes stamina based on bird's vertical movement
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                birdMovement = 0
                birdMovement -= 2
                sbarLength -= 25
            elif event.key == pygame.K_DOWN:
                birdMovement = 0
                birdMovement += 2
                sbarLength -= 10

        # creates a coin every 3 sec after an input from user
        if event.type == SPAWNCOIN:
            coinList.append(createCoin())
            if random.randint(1,3) == random.randint(1,3):   # 33% chance of bomb spawning 
                bombList.append(createBomb())
            if random.randint(1,2) == random.randint(1,2):   # 50% chance of berry spawning 
                berryList.append(createBerry())
            if random.randint(1,5) == random.randint(1,5):   # 20% chance of star spawning 
                starList.append(createStar())
        
    # moving the bird due to gravity
    birdMovement += gravity
    birdRect.centery += birdMovement

    # displays floor, background, and bars onto screen
    screen.blit(bgSurface,(0,0))
    floor_x_pos -= 1
    drawFloor()
    if floor_x_pos <= -width:
        floor_x_pos = 0
    healthBar()
    staminaBar()
    
    passedObjects(coinList,bombList,berryList,starList)
    # checks if images overlap
    overlap(coinList,bombList,berryList,starList)
    
    # displays coins
    coinList = moveCoin(coinList)
    drawCoin(coinList)

    # displays berries
    berryList = moveBerry(berryList)
    drawBerry(berryList)

    # displays bombs
    bombList = moveBomb(bombList)
    drawBomb(bombList)

    # displays stars
    starList = moveStar(starList)
    drawStar(starList)

    # Calls all other game functions
    getsCoin()
    getsBerry()
    getsStar()
    hitsBomb()
    maxBar()
    birdInBounds()
    birdOutofBounds()
    wingMovement()
    progress()
    points(coinsCollected,bombsHit,starsCollected,berriesCollected)
    
    # checks if user won/lost and then displays end Screen
    # then checks what endScreen() returns. If it returns True(user
    # clicks on restart button), then game restarts
    if eTime*2 >= 100 and endScreen("You Win!",0) == True:
        restart = True
    if barZero() == True and endScreen("You Lost :(",1) == True:
        restart = True

    # resets the values of all of the variables back to their original value
    if restart:
        iTime = time.time()
        eTime = time.time()-iTime
        gravity = 0.025
        birdMovement = 0
        coinsCollected = 0
        starsCollected = 0
        berriesCollected = 0
        bombsHit = 0
        hbarLength = 450
        sbarLength = 450
        birdRect.center = (400,200)
        oobSound.set_volume(0.5)
        # deletes all of the objects from the lists
        del coinList[:]
        del berryList[:]
        del starList[:]
        del bombList[:]
        restart = False 
    
    # updates screen
    pygame.display.update()
    clock.tick(120)    # 120 fps max
