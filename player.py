import pygame
from animatedSprite import AnimatedSprite

class Player:
    # animated sprite data
    eastImage = pygame.image.load("neko_east.png")
    westImage = pygame.image.load("neko_west.png")

    # sprite dimensions
    SPRITE_X = 32
    SPRITE_Y = 31

    # initial x/y positions
    START_X = 16
    START_Y = 16
    
    def __init__(self):
        self.size = 24
        self.speed = 2
        
        self.posX = self.START_X
        self.posY = self.START_Y

        # visibility is conveyed to player through a square
        # indicator on the screen
        self.box = (320-60, 480-40, 120, 20)
        self.color = [0, 0, 0]
        
        self.visible = True
        self.caught = False

        # animated sprite data
        self.image = self.eastImage
        self.sprite = AnimatedSprite(self.image,
                                     [self.posX, self.posY],
                                     2,
                                     1,
                                     0,
                                     2,
                                     8)

    def getX(self):
        return self.posX

    def getY(self):
        return self.posY

    def isCaught(self):
        return self.caught

    def move(self, direction):
        # update animated sprite
        self.sprite.update()

        # decide direction based on given argument
        if direction == "UP":
            self.posY -= self.speed
        if direction == "DN":
            self.posY += self.speed
        if direction == "LT":
            self.posX -= self.speed
            
            # switch to facing west if necessary
            if self.image == self.eastImage:
                self.image = self.westImage
                self.sprite.image = self.image
                
        if direction == "RT":
            self.posX += self.speed
            
            # switch to facing east if necessary
            if self.image == self.westImage:
                self.image = self.eastImage
                self.sprite.image = self.image

    def update(self, shadows, guards):
        # set visibility based on whether or not player is in shadow
        for shadow in shadows:
            if (self.posX >= shadow.posX and
                self.posX <= shadow.posX + shadow.width and
                self.posY >= shadow.posY and
                self.posY <= shadow.posY + shadow.length):
                
                self.visible = False
                self.color = [0, 200, 0]
                break
            
            self.visible = True
            self.color = [200, 0, 0]

        # check to see if any guards have caught the player
        if self.visible:
            for guard in guards:
                if ((self.posX < guard.posX and self.posY < guard.posY
                     and guard.orientation == "NW") or
                    (self.posX < guard.posX and self.posY > guard.posY
                     and guard.orientation == "SW") or
                    (self.posX > guard.posX and self.posY < guard.posY
                     and guard.orientation == "NE") or
                    (self.posX > guard.posX and self.posY > guard.posY
                     and guard.orientation == "SE")):
                    
                    self.caught = True
                    guard.color = [255, 255, 255]

        # update animated sprite position
        self.sprite.setPosition(self.posX - self.SPRITE_X / 2,
                                self.posY - self.SPRITE_Y / 2)

    def reset(self):
        self.posX = self.START_X
        self.posY = self.START_Y
        
        self.box = (320-60, 480-40, 120, 20)
        self.color = [0, 0, 0]
        
        self.visible = True
        self.caught = False

        self.image = self.eastImage

        self.sprite = AnimatedSprite(self.image,
                                     [self.posX, self.posY],
                                     2,
                                     1,
                                     0,
                                     2,
                                     8)

    def draw(self, surface):
        self.sprite.draw(surface)

    def drawVisibility(self, surface):
        surface.fill(self.color, self.box)
