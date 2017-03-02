import pygame

class Shadow:
    # shadow color
    COLOR = (32, 32, 32, 192)

    # unit size in pixels of a shadow
    # length/width multiples are passed to the constructor
    # to determine individual shadow size
    U = 32
    
    def __init__(self, posX, posY, width, length):
        self.posX = posX
        self.posY = posY
        self.width = width * self.U
        self.length = length * self.U

        self.data = pygame.Surface( (self.width, self.length),
                                    pygame.SRCALPHA, 32 )
        self.data.fill(self.COLOR)

    def draw(self, surface):
        surface.blit( self.data, (self.posX, self.posY) )
