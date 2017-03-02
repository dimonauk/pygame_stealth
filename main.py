import pygame
from player import Player
from shadow import Shadow
from guard import Guard

def main():
    # constants
    WIN_X = 640
    WIN_Y = 480
    FONT_SIZE = 16
    S_U = Shadow.U # shadow unit size taken from Shadow class
    BASE_RESET_TICKS = 60 * 3 # 3 seconds to reset after being caught
    
    # pygame setup
    pygame.init()
    screen = pygame.display.set_mode((WIN_X, WIN_Y))
    font = pygame.font.SysFont("Courier", FONT_SIZE, True)
    clock = pygame.time.Clock()

    # player data
    player = Player()

    # Shadow/Guard data for each level. These two lists need to be
    # of the same size, otherwise, there will be some extra data
    # that is unused in either list, and the game may not do level
    # transition properly. The lists for the individual levels' data
    # within the main list can be of any size.

    shadows = [[Shadow(0, 0, 1, 1),
                Shadow(WIN_X - S_U, WIN_Y - S_U, 1, 1),
                Shadow(100, 100, 8, 2),
                Shadow(275, 300, 8, 2)],
               
               [Shadow(0, 0, 1, 1),
                Shadow(100, 100, 1, 8),
                Shadow(200, 100, 8, 2),
                Shadow(500, 100, 2, 10),
                Shadow(WIN_X - S_U, WIN_Y - S_U, 1, 1)],

               [Shadow(0, 0, 1, 1),
                Shadow(WIN_X - S_U, WIN_Y - S_U, 1, 1),
                Shadow(150, 70, 2, 3),
                Shadow(360, 150, 2, 2),
                Shadow(450, 70, 2, 5),
                Shadow(150, 240, 2, 3),
                Shadow(300, 240, 2, 3),
                Shadow(450, 270, 2, 5),
                Shadow(170, 350, 5, 1)],

               [Shadow(0, 0, 1, 1),
                Shadow(WIN_X - S_U, WIN_Y - S_U, 1, 1),
                Shadow(85, 75, 2, 8),
                Shadow(180, 300, 7, 2),
                Shadow(225, 225, 2, 2),
                Shadow(290, 150, 2, 2),
                Shadow(370, 95, 2, 2),
                Shadow(450, 70, 5, 4),
                Shadow(565, 230, 2, 6)]]

    guards = [[Guard(500, 75, 500-250, 75+250),
               Guard(85, 400, 85+250, 400-250)],
              
              [Guard(400, 400, 250, 250),
               Guard(500, 200, 250, 450),
               Guard(100, 50, 100-75, 50+75)],

              [Guard(190, 50, 190+130, 50+130),
               Guard(330, 225, 330-150, 225+150),
               Guard(265, 410, 265+170, 410-170)],

              [Guard(60, 300, 60+100, 300+100),
               Guard(220, 160, 220+110, 160+110),
               Guard(500, 300, 500-220, 300-220),
               Guard(610, 215, 610-160, 215+160)]]

    # ----------------------------------------------------------

    # metagame data
    ticksToReset = BASE_RESET_TICKS
    levelComplete = False
    levelFailed = False
    level = 0
    NUM_LEVELS = len(shadows)
    levelDisplay = "Level: {0}/{1}".format(level + 1, NUM_LEVELS)
    status = "You are undetected."

    bg = pygame.image.load("bg.png").convert()

    while True:
        ## EVENTS ----------------------------------------------
        
        nextEvent = pygame.event.poll()

        # quit game
        if nextEvent.type == pygame.QUIT:
            break

        # accept character movement if level is yet completed
        if not levelComplete and not levelFailed:
            keysDown = pygame.key.get_pressed()
            if keysDown[pygame.K_UP] and player.posY > 0:
                player.move("UP")
            if keysDown[pygame.K_DOWN] and player.posY < WIN_Y:
                player.move("DN")
            if keysDown[pygame.K_LEFT] and player.posX > 0:
                player.move("LT")
            if keysDown[pygame.K_RIGHT] and player.posX < WIN_X:
                player.move("RT")

        ## UPDATE ----------------------------------------------

        # update player data based on new position, shadows, and guards
        player.update(shadows[level], guards[level])

        # update guards
        for guard in guards[level]:
            guard.update()

        # check for necessary changes to metagame flags
        if player.getX() >= WIN_X - 16 and player.getY() >= WIN_Y - 16:
            levelComplete = True
        if player.isCaught():
            levelFailed = True

        # update status text and counter
        if not levelComplete and not levelFailed:
            status = "You are undetected."
        elif levelComplete:
            if level + 1 < NUM_LEVELS:
                status = "Transition in {0}...".format(ticksToReset / 60 + 1)
                ticksToReset -= 1
            else:
                status = "Game complete!"
        elif levelFailed:
            status = "Caught! Restart in {0}...".format(ticksToReset / 60 + 1)
            ticksToReset -= 1

        # reset level if necessary
        if levelFailed and ticksToReset == 0:
            ticksToReset = BASE_RESET_TICKS
            levelFailed = False

            player.reset()
            
            for guard in guards[level]:
                guard.reset()

        # level transition if necessary
        if levelComplete and ticksToReset == 0:
            ticksToReset = BASE_RESET_TICKS
            levelComplete = False
            level += 1
            levelDisplay = "Level: {0}/{1}".format(level + 1, NUM_LEVELS)
            status = "You are undetected."

            player.reset()

        ## RENDER ----------------------------------------------

        # render background
        screen.blit(bg, (0,0))

        # render player
        player.draw(screen)

        # render guards
        for guard in guards[level]:
            guard.draw(screen)

        # render shadows
        for shadow in shadows[level]:
            shadow.draw(screen)

        # render visibility display
        player.drawVisibility(screen)

        # display status text
        line1 = font.render(levelDisplay, True, (0, 0, 0))
        line2 = font.render(status, True, (0, 0, 0))
        screen.blit(line1, (10, WIN_Y - 10 - 2 * FONT_SIZE))
        screen.blit(line2, (10, WIN_Y - 10 - FONT_SIZE))
        
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

main()
