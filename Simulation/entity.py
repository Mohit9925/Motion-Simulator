import pygame
import pymunk.pygame_util
import pygame_gui
import pymunk
import os
import math
from EntityPropertyWindow import EntityPropertyWindow


def convertToPygameCoordinates(pos,width):
    return Vec2d(pos[0], -pos[1]+width)
def findDistance(x1,y1,x2,y2):
    return math.sqrt(((x1-x2)**2)+((y1-y2)**2))


class Component:
    allComponents={}
    
    def __init__(self,screen):
        self.mass=1
        self.momentum=1
        self.screen=screen
        self.body=pymunk.Body(self.mass,self.momentum)
        self.shape=None
        
        self.posx=0
        self.posy=0
        if self.__class__ in Component.allComponents.keys():
            Component.allComponents[self.__class__].append(self)
        else:
            Component.allComponents[self.__class__]=[self]
        

        
        

    def setPos(self,posx,posy):
         
        self.posx=posx
        self.posy=posy
        # self.rect=pyagme.Rect(self.posx,self.posy,self.height,self.width)
        return self
    def __del__(self):
        if self.__class__ in Component.allComponents.keys() and len(Component.allComponents[self.__class__])>0:
            Component.allComponents[self.__class__].remove(self)
            del(self)
    
    def set_elasticity(self,elasticity):
        if self.shape:
            self.shape._set_elasticity(elasticity)
        return self 
    def set_density(self,density):
        if self.shape:
            self.shape._set_density(density)
        return self 
    
    def set_mass(self,mass):
        if self.shape:
            self.shape._set_mass(mass)
            self.mass=mass
        return self
    def set_friction(self,friction):
        if self.shape:
            self.shape._set_friction(friction)
        return self
    def setOnClickListenerForAll(event,manager):
        for classes in Component.allComponents.keys():
            for component in Component.allComponents[classes]:
                component.runOnClickListener(event,manager)
    def renderAll():
        for classes in Component.allComponents.keys():
            for component in Component.allComponents[classes]:              
                
                component.render()        
        
class Entity(Component):
    clicked_entity=None
    
    
    
    def __init__(self,screen):
        super().__init__(screen)
        self.color=(200,0,0)
        self.rect=None
        
        self.name=None
        self.momentum=1
        
        self.body.position=pymunk.pygame_util.from_pygame((self.posx,self.posy),self.screen)
        self.angle=self.body._get_angle()
        self.cursor_image_url='/image/cursor/circle.png'
        
        
        
    
     
    def setPos(self,posx,posy):
        self.posx=posx
        self.posy=posy
        self.body._set_position(pymunk.pygame_util.from_pygame((self.posx,self.posy),self.screen))
        
        
        if self.rect:
            self.rect=pygame.Rect( self.posx,self.posy,self.width,self.height)
        return self
    def setColor(self,color):
        self.color=color

    def openPropWindow(self):
        
        if EntityPropertyWindow.opened_window_for_entity!=self:
            if EntityPropertyWindow.opened_window_for_entity!=None:
                
                del(EntityPropertyWindow.opened_window_for_entity)
            Entity.prop_window_opened_for=self
            pos=pygame.mouse.get_pos()
            EntityPropertyWindow(pos[0],pos[1],self)

    def runOnClickListener(self,event,manager):
        pos=pygame.mouse.get_pos()
        LEFT=1
        RIGHT=3
        if event.type==pygame.MOUSEBUTTONDOWN:
            if self.rect:
                if self.rect.collidepoint(pos):
                    Entity.clicked_entity=self
                    if event.button==RIGHT:
                        self.openPropWindow()

    def render(self):
        if self.posx not in range(0,self.screen.get_width()+100) or self.posy not in range(0,self.screen.get_height()+100):
            
            del(self)
            return


    
    
        
    
        
        


class Ball(Entity):
    #initialization or constructor
    
    def __init__(self,screen,radius):
        super().__init__(screen)
        self.radius=radius
        
        self.originalRad=radius
        self.color=(223, 31, 8)
        self.clickedPos=None
        self.name='ball'
        self.mass=1
        self.momentum=pymunk.moment_for_circle(self.mass,0,self.radius)
        self.body=pymunk.Body(self.mass,self.momentum)
        self.shape=pymunk.Circle(self.body,self.radius)
        self.screen.space.add(self.shape,self.body)
        self.set_elasticity(0.5)
        self.set_friction(1)
        # pymunk.Body.
        self.text=f"""
                velocity:{self.body._get_velocity()}
            """
        self.Label=pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(self.posx,self.posy,50,20),
            text="v:",
            manager=self.screen.manager
        )
        
        self.config_dict={
            'radius':self.radius,
            'mass':self.body._get_mass(),
            'color':self.color,
            'friction':self.shape._get_friction(),
            # 'momentum':self.shape._get_moment()
            
        }
         

    #override
    
    
    
    def render(self):
        super().render()
        self.angle=self.body._get_angle()
        self.posx,self.posy=pymunk.pygame_util.to_pygame(self.body.position,self.screen)
        # print(self.posx,self.posy)
        
        self.rect=pygame.draw.circle(self.screen,self.color,(int(self.posx),int(self.posy)),self.radius)
        self.line=(self.posx,self.posy)+pymunk.pygame_util.Vec2d(self.radius,0).rotated(90-self.angle)
        self.text=f"""
                velocity:{self.body._get_velocity()}
            """
        self.Label.set_position((self.posx,self.posy))
        vel=len(str(self.body._get_velocity()))

        self.Label.relative_rect.width=(vel//3)*4

        self.Label.set_text('v:'+str(int(abs(self.body._get_velocity()[0]-self.body._get_velocity()[1]))))
        # self.Label.set_text(self.text)

        pygame.draw.lines(self.screen,(0,0,0),False,((self.posx,self.posy),self.line))
        
    
    def runOnClickListener(self,event,manager):
        super().runOnClickListener(event,manager)
        
    def resize(self,radius):
        self.radius=radius
        del(self.shape)
        self.shape=pymunk.Circle(self.body,self.radius)
        for land  in Component.allComponents[Land]:
            if self.rect.colliderect(land.rect):
                while not self.rect.colliderect(land.rect):
                    self.posy-=1
                    self.setPos(self.posx,self.posy)
        return self
    


class Land(Component):
    def __init__(self,screen,start_pos,end_pos):
        super().__init__(screen)
        self.start_pos=start_pos
        self.end_pos=end_pos
        self.screen=screen
    
        self.shape=pymunk.Segment(
            self.screen.space.static_body,
            pymunk.pygame_util.from_pygame(self.start_pos,self.screen),
            pymunk.pygame_util.from_pygame(self.end_pos,self.screen),
            1            
        
        )
        self.screen.space.add(self.shape)
        self.angle=0
        


    
    def setPos(self,start_pos,end_pos):
        self.start_pos=start_pos
        self.end_pos=end_pos
        self.body.position(pymunk.pygame_util.from_pygame())
    
    def render(self):
              
        pygame.draw.line(self.screen,(0,0,0),self.start_pos,self.end_pos)

    def runOnClickListener(self,event,manager):
        pass
            

    
    
    

class Wall(Entity):
    def __init__(self,screen,):
        super().__init__(screen)
        self.height=200
        self.width=100
        self.image=pygame.image.load('./img/wall.png')
        self.image=pygame.transform.scale(self.image,(self.width,self.height))
        self.name='wall'
    def render(self):
        self.screen.blit(self.image,(self.posx,self.posy))
        pygame.draw.rect(self.screen,(0,0,0),pygame.Rect(self.posx,self.posy,self.width,self.height),2)
        