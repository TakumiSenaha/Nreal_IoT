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

def main_loop(width=800, height=600):
    """
    The main loop of pygame.
    Flying objects are drawn pygame display.

    Args:
        width (number): Width of pygame display.
        height (number): Height of pygame display.    
    """
    pygame.init()
    pygame.display.set_mode((width, height), DOUBLEBUF | OPENGL)

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
    while(display_thread.is_alive()):
#         np.random.random()*360.0
        gen_triangle(angle=180, scale=np.random.random()+1.0)
        time.sleep(0.1)