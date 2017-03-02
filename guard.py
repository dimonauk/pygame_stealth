import pygame
from animatedSprite import AnimatedSprite

class Guard:
    # animated sprite data
    eastImage = pygame.image.load("shepherd_east.png")
    westImage = pygame.image.load("shepherd_west.png")
    
    def __init__(self, startX, startY, destX, destY):
        self.size = 24
        self.speed = 1

        self.posX = startX
        self.posY = startY

        self.box = [startX, startY, self.size, self.size]
        self.color = [255, 0, 0]

        # guards patrol between two points
        # first point is the given start position
        self.aX = startX
        self.aY = startY

        self.bX = destX
        self.bY = destY

        self.nextPoint = "B"

        # figure out initial orientation based on patrol points
        if startX < destX and startY < destY: self.orientation = "SE"
        if startX < destX and startY > destY: self.orientation = "NE"
        if startX > destX and startY < destY: self.orientation = "SW"
        if startX > destX and startY > destY: self.orientation = "NW"
        
        if self.orientation == "NE" or self.orientation == "SE":
            self.image = self.eastImage
        else:
            self.image = self.westImage
        
        self.sprite = AnimatedSprite(self.image,
                                     [self.posX, self.posY],
                                     6,
                                     3,
                                     6,
                                     6,
                                     8)

    def update(self):
        # step towards next patrol point
        if self.nextPoint == "B" and self.color != [255,255,255]:
            if self.bX < self.aX:
                self.posX -= self.speed
            else:
                self.posX += self.speed
            
            if self.bY < self.aY:
                self.posY -= self.speed
            else:
                self.posY += self.speed

            # change destination if end of path is reached
            if self.posX == self.bX and self.posY == self.bY:
                self.nextPoint = "A"

                # adjust orientation and sprite image
                if   self.orientation == "NE":
                    self.orientation = "SW"
                    self.sprite.image = self.westImage
                elif self.orientation == "NW":
                    self.orientation = "SE"
                    self.sprite.image = self.eastImage
                elif self.orientation == "SE":
                    self.orientation = "NW"
                    self.sprite.image = self.westImage
                elif self.orientation == "SW":
                    self.orientation = "NE"
                    self.sprite.image = self.eastImage

        # same logic above applies to moving to the other patrol point
        if self.nextPoint == "A" and self.color != [255,255,255]:
            if self.aX < self.bX:
                self.posX -= self.speed
            else:
                self.posX += self.speed
            
            if self.aY < self.bY:
                self.posY -= self.speed
            else:
                self.posY += self.speed

            if self.posX == self.aX and self.posY == self.aY:
                self.nextPoint = "B"

                if   self.orientation == "NE":
                    self.orientation = "SW"
                    self.sprite.image = self.westImage
                elif self.orientation == "NW":
                    self.orientation = "SE"
                    self.sprite.image = self.eastImage
                elif self.orientation == "SE":
                    self.orientation = "NW"
                    self.sprite.image = self.westImage
                elif self.orientation == "SW":
                    self.orientation = "NE"
                    self.sprite.image = self.eastImage
            
        # update render position
        self.box[0] = self.posX - self.size / 2
        self.box[1] = self.posY - self.size / 2

        # update animated sprite data
        self.sprite.setPosition(self.posX - 58 / 2,
                                self.posY - 36 / 2)

        # switch to barking animation if player is caught
        if self.color == [255, 255, 255]:
            self.sprite.startFrameIndex = 0
            self.sprite.numberOfFrames = 4
            
        self.sprite.update()

    def reset(self):
        self.posX = self.aX
        self.posY = self.aY

        self.box = [self.aX, self.aY, self.size, self.size]
        self.color = [255, 0, 0]

        self.nextPoint = "B"

        # figure out initial orientation based on patrol points
        if self.aX < self.bX and self.aY < self.bY: self.orientation = "SE"
        if self.aX < self.bX and self.aY > self.bY: self.orientation = "NE"
        if self.aX > self.bX and self.aY < self.bY: self.orientation = "SW"
        if self.aX > self.bX and self.aY > self.bY: self.orientation = "NW"

        # animated sprite data
        if self.orientation == "NE" or self.orientation == "SE":
            self.image = self.eastImage
        else:
            self.image = self.westImage
        
        self.sprite = AnimatedSprite(self.image,
                                     [self.posX, self.posY],
                                     6,
                                     3,
                                     6,
                                     6,
                                     8)

    def draw(self, surface):
        self.sprite.draw(surface)
