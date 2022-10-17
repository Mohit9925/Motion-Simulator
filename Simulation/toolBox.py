import pygame
import pygame_gui
from pygame_gui.elements import UIPanel
from pygame_gui.elements import UIButton
from entity import Entity
from Helpers import *
import entity
class ToolBox(UIPanel):

    def __init__(self,relative_rect,layer_height,manager):
        self.selectedTool=None
        self.tools=[]
        self.manager=manager
        self.height=relative_rect.h
        self.width=relative_rect.w
        self.isHidden=False
        
        super().__init__(relative_rect,layer_height,manager)
        self.hide_button=UIButton(pygame.Rect(0,self.height-30,self.width-6,30),'Hide',manager=self.manager,container=self.get_container())
        self.show_button=UIButton(pygame.Rect(0,200,30,100),">",self.manager)
        self.show_button.hide()
    def add_Tool(self,tool):
        self.tools.append(tool)
        
    
    def process_event(self,event):
        super().process_event(event)
        
        if event.type==pygame.USEREVENT:
            if event.user_type==pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element in self.tools:
                    if self.selectedTool:
                        self.selectedTool.unselect()
                    self.selectedTool=event.ui_element
                    event.ui_element.select()
                if event.ui_element==self.hide_button:                    
                    if not self.isHidden:
                        self.hide()
                        self.show_button.show()
                        self.isHidden=True
                
                
                        
                        



    def toggle_show(self):
        if self.isHidden:
            self.show()
        else:
            self.hide()
        

    
class ToolBoxButton(UIButton):
    def __init__(self,posx,posy,text,toolbox,command=None,on_screen_click=None,height=30,width=30):
        self.command=command
        self.on_screen_click=on_screen_click
        self.tool_box=toolbox
        toolbox.add_Tool(self)
        super().__init__(pygame.Rect(posx,posy,width,height),text,manager=toolbox.manager,container=toolbox.get_container())
    
    
    def process_event(self,event):
        super().process_event(event)
        if event.type==pygame.USEREVENT:
            if event.user_type==pygame_gui.UI_BUTTON_PRESSED:
                if self.command:
                    self.command()
        
        

def ball_tool_event(self):
    self.selectedTool=self.ball
    self.screen.cursor_loader.update_cursor('./image/cursor/circle.png')

def ball_on_screen_click(self):
    if self.screen.item_drawable:
        pos=pygame.mouse.get_pos()
        new_Ball=entity.Ball(self.screen,50).setPos(pos[0],pos[1])
    

    

class SimulatorToolBox(ToolBox):
    def __init__(self,screen,relative_rect,layer_height,manager):
        super().__init__(relative_rect,layer_height,manager)
        x,y=0,0
        self.screen=screen
        self.selectedTool=None
        self.ball=ToolBoxButton(x,y,"ball",self,lambda:ball_tool_event(self),lambda:ball_on_screen_click(self))
        self.move=ToolBoxButton(30,y,"move",self)
        self.move2=ToolBoxButton(x,30,"move",self)
    
    def process_event(self,event):
        super().process_event(event)
        if event.type==pygame.USEREVENT:
            if event.user_type==pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element==self.ball:
                    if self.ball.command:
                        self.ball.command()
        if event.type==pygame.MOUSEBUTTONDOWN:
            if event.button==1: #right click                 
                if self.selectedTool and self.selectedTool.on_screen_click:
                    self.selectedTool.on_screen_click()
        

    