""" Flyobj

The module of flying objects that represents sounds of various loudness from various direction.

Example:
    import flyobj
    import numpy as np
    import time

    flyobj.init()
    
    while(flyobj.display_thread.is_alive()):
        flyobj.gen_triangle(angle=np.random.random()*360.0, scale=np.random.random()+1.0)
        time.sleep(0.1)
"""

import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import threading
import time
from abc import ABCMeta, abstractclassmethod

class Flyobj(metaclass=ABCMeta):
    """
    An abstract class representing a flying object in 3D space.

    Attributes:
        objs (list): A list of all Flyobj instances.
        angle (float): Angle of Flyobj in degrees.
        scale (float): Scale of the Flyobj.
        v (float): Velocity of the Flyobj.
        r (float): Initial distance from origin.
        r_end (float): The distance at which the object should be destroyed.
        x (float): x-coordinate.
        y (float): y-coordinate.
    """

    objs = []

    def __init__(self, angle=0.0, scale=1.0, v=0.2, r_start=10.0, r_end=5.0) -> None:
        """ Create a Flyobj instance

        Args:
            angle (float): Angle of Flyobj in degrees.
            scale (float): Scale of Flyobj.
            v (float): Velocity of Flyobj.
            r_start (float): Initial distance from origin.
            r_end (float): Distance at which the object should be destroyed.
        """
        self.objs.append(self)
        self.angle = angle
        self.scale = scale
        self.v = v
        self.r = r_start
        self.r_end = r_end
        self.reload_coordinate()  

    def __del__(self) -> None:
        """
        Remove the instance from the list of objects when it is destroyed.
        """
        self.objs.remove(self)

    def reload_coordinate(self):
        self.x = self.r*np.cos(self.angle/180.0*np.pi)
        self.y = self.r*np.sin(self.angle/180.0*np.pi)
        self.r -= self.v

    @abstractclassmethod
    def draw(self):
        """
        Draw the object on the screen.
        """
        pass

    def run(self) -> None:
        """
        Update the object's position and draw it on the screen.
        If the object has reached its destination, destroy it.
        """
        if self.r <= self.r_end:
            del(self)
        else:
            self.reload_coordinate()
            glPushMatrix()
            glTranslatef(self.x, self.y, 0.0)
            glRotatef(self.angle, 0.0, 0.0, 1.0)
            glScalef(self.scale, self.scale, self.scale)
            self.draw()
            glPopMatrix()

    @classmethod
    def display(cls) -> None:
        """
        Update all objects.
        """
        for obj in cls.objs:
            obj.run()

    
class Triangle(Flyobj):
    """
    A class representing a triangle that can fly in 3D space.

    Attributes:
        vertices (tuple): A tupule of three 3D points representing the vertices of the triangle.
    
    """
    vertices = ((-1, 0, 0),
                (1, -1, 0),
                (1, 1, 0))

    def draw(self) -> None:
        """
        Draw the object on the screen.  
        Overrides the abstract method defined in Flyobj class.
        """
        glBegin(GL_TRIANGLE_STRIP)
        glColor3fv((1, 0, 0))
        for v in self.vertices:
            glVertex3dv(v)
        glEnd()

class TextObj():
    """
    A class representing a text

    Attributes:
        objs (list) : A list of all text objects. 
        current_time (float) : Current time [s]
        screen (Surface) : Surface object.
        font : Font object.
    """
    objs = []
    current_time = time.time()
    screen = None
                               
    def __init__(self, text, angle = 0.0, size = 100, r = 10.0, lifetime = 1.0) -> None:
        self.end_time = lifetime + TextObj.current_time
        self.font = pygame.font.Font("ipaexg.ttf", int(size))
        self.t = self.font.render(text, True, (0, 255, 0, 255)).convert_alpha()
        sw, sh = TextObj.screen.get_width(), TextObj.screen.get_height()
        self.tw, self.th = self.t.get_width(), self.t.get_height()
        self.x = sw/2 - self.tw/2 + r * np.cos(angle*np.pi/180.0)
        self.y = sh/2 - self.th/2 + r * np.sin(angle*np.pi/180.0)
        TextObj.objs.append(self)

    def draw(self):
        if self.end_time <= TextObj.current_time:
            del(self)
        else:
            text_data = pygame.image.tostring(self.t, "RGBA", True)
            glWindowPos2f(self.x, self.y)
            glDrawPixels(self.tw, self.th, GL_RGBA, GL_UNSIGNED_BYTE, text_data)
    
    def __del__(self):
        TextObj.objs.remove(self)

    @classmethod
    def display(cls):
        cls.current_time = time.time() # Update current time
        for obj in cls.objs:
            obj.draw()

def main_loop(width=1920, height=1080):
    """
    The main loop of pygame.
    Flying objects are drawn pygame display.

    Args:
        width (number): Width of pygame display.
        height (number): Height of pygame display.    
    """
    pygame.init()
    #screen = pygame.display.set_mode((width, height), DOUBLEBUF | OPENGL | pygame.FULLSCREEN)
    screen = pygame.display.set_mode((width, height), DOUBLEBUF | OPENGL)
    # For text drawing
    TextObj.screen = screen
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    glMatrixMode(GL_MODELVIEW)
    gluPerspective(45, (width/height), 0.1, 50.0)
    gluLookAt(0.0, -15.0, -15.0,
              0.0, 0.0, 0.0,
              0.0, 1.0, 0.0,)
              
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        Triangle.display()
        TextObj.display()
        pygame.display.flip()
        pygame.time.wait(10)

def gen_triangle(angle=0.0, scale=1.0, v=0.2, r_start=10.0, r_end=5.0) -> None:
    """
    Generate a triangle with the given properties.

    Args:
        angle (float): Angle of the triangle in degrees.
        scale (float): Scale of the triangle.
        v (float): Velocity of the triangle.
        r_start (float): Initial distance from origin.
        r_end (float): Distance at which the triangle should be destroyed.

    Returns:
        None
    """
    Triangle(angle, scale, v, r_start, r_end)

def gen_text(text = "", angle = 0.0, size = 50, r = 200.0, lifetime = 1.0) -> None:
    TextObj(text, angle, size, r, lifetime)

display_thread = None

def init(width=800, height=600):
    """
    Initializes the display thread.
    """
    global display_thread
    display_thread = threading.Thread(args=(width, height), target = main_loop)
    display_thread.start()

# Example code
if __name__ == "__main__":
    init()
    time.sleep(1)
    while(display_thread.is_alive()):
        angle =  np.random.random()*360.0
        gen_triangle(angle, scale=np.random.random()+1.0)
        gen_text("こんにちは", angle+180)
        time.sleep(0.1)