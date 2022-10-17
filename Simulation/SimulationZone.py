import pygame
import pymunk
import pygame_gui



class SimulationZone(pygame.Surface):
    def __init__(self,dimensions):
        self.dimensions=dimensions
        super().__init__(self.dimensions)
        self.manager=pygame_gui.UIManager(self.dimensions)
        self.space=pymunk.Space()
        self.space.gravity=(0,-10)
        self.space._set_damping(0.9)
        self.item_drawable=True
        self.simulation_time_state=2/60
        self.cursor_loader=None
        