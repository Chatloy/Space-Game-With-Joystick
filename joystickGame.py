import joystick
import sprite
import pygame
import time
import random
import boomtone
import leaderBoard

state = "lobby"

sprite.init()

boom = boomtone.SONGS["boom"]

font = sprite.newFont("freesansbold", 30)

abc = "abcdefghijklmnopqrstuvwxyz"

def setinitials():
    global initials, currentLetterNum, currentLetter, initialsNum, text, screen, pressed
    if joystick.Y >= 200:
        if pressed == False:
            currentLetterNum -= 1
            pressed = True
    elif joystick.Y <= 100:
        if pressed == False:
            currentLetterNum += 1
            pressed = True
    elif joystick.X >= 200:
        if pressed == False:
            pressed = True
            initialsNum -= 1
    elif joystick.X <= 100:
        if pressed == False:
            pressed = True
            initialsNum += 1
    else:
        pressed = False
    
    currentLetterNum = currentLetterNum % 26
    currentLetter = abc[currentLetterNum]
    initialsList = list(initials)
    if initialsNum != 3:
        #print(initialsNum)
        initialsList[initialsNum] = currentLetter
        initials = "".join(initialsList)
    else:
        return True

    text = font.render(initials, True, (255,255,255))
    screen.blit(text,
    (50 - text.get_width() // 2, 100 - text.get_height() // 2))



def setup():
    global sound, pressed, playButton, quitButton, player, badGuys, bulletList, running, screen, pointer, score
    sound = []

    score = 0

    #yellow = sprite.newColor((255,255,0))
    #yellow = pygame.color.Color(255,255,0)

    screen = sprite.setScreen(670, 670)

    pressed = True

    playButton = sprite.Player(screen, (255,255,255), 160, 335,500, True, 0)
    playButton.setImage("playButton.png")

    quitButton = sprite.Player(screen, (0,0,0), 160, 520,500, True, 0)
    quitButton.setImage("quitButton.png")

    pointer = sprite.Player(screen, (0,0,0), 50, 0,400,True, 0)
    pointer.setImage("pointer.png")

    player = sprite.Player(screen, (0,0,0), 50, 335, 500, True, 0.8)
    player.setImage("faceInverted.png")

    #coin = sprite.Sprite(screen, (255,255,0), 20, 335, 335)
    badGuys = []
    bulletList = []
    for i in range(random.randint(3,10)):
        badGuys.append(sprite.Player(screen, (0,0,0), 40, random.randint(0,670), 50, True, 0))
    running = True

    print("wires go up")
    joystick.setup()

def joyControls():
    global pressed
    joystick.loop()
    if joystick.Y >= 200:
        player.y = player.y + 10
        #print("player moved +10")
    elif joystick.Y <= 100:
        player.y = player.y - 10
        #print("player moved -10, Y:%d" % (joystick.Y))
    
    if joystick.X >= 200:
        player.x = player.x - 10
    elif joystick.X <= 100:
        player.x = player.x + 10

    if joystick.Z == 0:
        if not pressed:
            bulletList.append(sprite.Sprite(screen, (255,255,255), 10, player.x, player.y))
            pressed = True
    else:
        pressed = False
    

def updateBadGuys():
    global sound
    global state, score
    if badGuys != []:
        for i in badGuys:
            i.setImage("spaceShip.png")
            i.update()
            if i.touching(player):
                state = "dead"
            else:
                i.y = i.y + 5
            
            for bullet in bulletList:
                if i.touching(bullet):
                    score = score + 10
                    badGuys.remove(i)
                    sound = ["c6", 0.05]
            
            if i.y > 700:
                badGuys.remove(i)


def updateBullets():
    for i in bulletList:
        i.update()
        i.y = i.y - 10

def leaderboard(): 
    leaderboard = leaderBoard.getLeaderboard('spaceJoystick')
    return leaderboard["leaders"]



if __name__ == "__main__":
    setup()
    initials = "aaa"
    currentLetterNum = 0
    currentLetter = abc[currentLetterNum]
    initialsNum = 0
    stop = False
    while not stop:
        sprite.setBackground((0,0,0))
        joystick.loop()
        stop = setinitials()
        pygame.display.flip()
        #print(initials)
        time.sleep(0.01)
    while running:
        sprite.setBackground((0,0,0))
        if state == "play":
            player.update()
            updateBadGuys()
            updateBullets()
            text = font.render("Score is: "+str(score), True, (255,255,255))
            screen.blit(text,
            (50 - text.get_width() // 2, 100 - text.get_height() // 2))
            pygame.display.flip()
            joyControls()
            #player.move(sprite.getKeys())
            #print(player.distanceFrom((335,335)))
            sprite.run()
            if random.randint(1,50) == 1:
                for i in range(random.randint(1,5)):
                    badGuys.append(sprite.Player(screen, (0,0,0), 40, random.randint(0,670), 50 + random.randint(-30,30), True, 0))
            if sound != []:
                if sound[1] > 0:
                    #print(sound[1])
                    boomtone.startSound(sound)
                    sound[1] = sound[1] - 0.01
                else:
                    boomtone.stop()
                    sound = []
        elif state == "lobby":
            playButton.update()
            joystick.loop()
            while joystick.Z == 1:
                sprite.setBackground((0,0,0))
                playButton.update()
                pygame.display.flip()
                joystick.loop()
            state = "play"
        elif state == "dead":
            leaderBoard.addToLeaderBoard(initials, score)
            sprite.setBackground((0,0,0))
            playButton.x = 166
            playButton.update()
            quitButton.update()
            joystick.loop()
            choice = "play"
            leaders = leaderboard()
            while joystick.Z == 1:
                if choice == "play":
                    pointer.x = 166
                else:
                    pointer.x = 520
                sprite.setBackground((0,0,0))
                playButton.update()
                quitButton.update()
                pointer.update()
                joystick.loop()
                joystick.loop()
                j = 1
                for i in leaders:
                    text = font.render(i["name"]+":          "+str(i["score"]), True, (255,255,255))
                    screen.blit(text,
                    (335 - text.get_width() // 2, (25*j) - text.get_height() // 2))
                    j = j + 1

                pygame.display.flip()
                if joystick.X >= 200:
                    choice = "play"
                if joystick.X <= 100:
                    choice = "exit"
            if choice == "play":
                state = choice
                setup()
            else:
                print("goodbye")
                exit()
        time.sleep(0.01)
        

