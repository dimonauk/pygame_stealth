import pygame

###########################################################################
#
###########################################################################
class AnimatedSprite:

    #######################################################################
    def __init__(self,
                 img,           ## Image containg all frames of animation
                 target_posn,   ## Location on surface to draw current frame
                 framesPerRow = 1,  ## Number of frames in each row
                 framesPerColumn = 1,
                 startFrameIndex = 0,
                 numberOfFrames = 1,
                 updateDivisor = 1   ## Only increment current frame index after
                                     ## this many updates
                 ):
        self.image = img
        self.position= target_posn
        self.framesPerRow = framesPerRow
        self.framesPerColumn = framesPerColumn
        self.startFrameIndex = startFrameIndex
        self.numberOfFrames = numberOfFrames
        self.currentFrameIndex = startFrameIndex
        self.frameWidth = self.image.get_width() / self.framesPerRow;
        self.frameHeight =  self.image.get_height() /self.framesPerColumn
        self.updateDivisor = updateDivisor
        self.updateCount = 0
        self.isDone = False
        
    #######################################################################
    def setPosition(self, x , y):
        self.position = (x, y)

    #######################################################################
    def update(self):
        if 0 == self.updateCount % self.updateDivisor:
            self.currentFrameIndex += 1

            if self.currentFrameIndex >= (self.startFrameIndex + \
                                          self.numberOfFrames):
               self.currentFrameIndex = self.startFrameIndex
               self.isDone = True
        #print 'sprite update', self.currentFrameIndex
        
        self.updateCount += 1
           
    #######################################################################
    def draw(self, target_surface):
        patch_rect = (self.currentFrameIndex % self.framesPerRow * \
                      self.frameWidth,
                      int(self.currentFrameIndex / self.framesPerRow) * \
                          self.frameHeight,
                      self.frameWidth,
                      self.frameHeight)
        target_surface.blit(self.image, self.position, patch_rect)
        #print 'sprite draw', self.image, self.position, patch_rect
    
    #######################################################################
    def containsPoint(self, pt):
        """ """
        (my_x, my_y) = self.position
        (x, y) = pt
        return ( x >= my_x and x < my_x + self.frameWidth and
                  y >= my_y and y < my_y + self.frameHeight)

    #######################################################################
    def handleClick(self):
        """ """
