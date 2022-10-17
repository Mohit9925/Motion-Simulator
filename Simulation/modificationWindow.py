import pygame
import pygame_gui
from pygame_gui.elements import UILabel,UIButton,UITextBox,UIPanel,UIHorizontalSlider
from pygame_gui import UIManager
# from pygame import Rect


class ModificationWindow(UIPanel):
    def __init__(self,screen,WIDTH,HEIGHT):
        self.isHidden=False
        self.screen=screen
        self.manager=self.screen.manager
        self.height=HEIGHT
        self.width=WIDTH
        super().__init__(pygame.Rect(WIDTH-300,0,300,HEIGHT),1,self.manager)
        self.set_gravity_label=UILabel(
            pygame.Rect(0,0,100,50),
            'Gravity:',
            self.manager,
            self.get_container()
        )
        self.gravity_slider=UIHorizontalSlider(
            pygame.Rect(0,50,200,30),
            10,
            (0,100),
            self.manager,
            container=self.get_container()
        )
        self.gravity_slider_label=UILabel(
            pygame.Rect(200,0,50,50),
            str(self.gravity_slider.get_current_value())+' m/s',
            self.manager,
            self.get_container()                    

        )
        
        self.set_damping_label=UILabel(
            pygame.Rect(0,150,100,50),
            'Damping:',
            self.manager,
            self.get_container()
        )

        self.damping_slider=UIHorizontalSlider(
            pygame.Rect(0,200,200,30),
            100,
            (0,100),
            self.manager,
            container=self.get_container()
        )
        self.damping_slider_label=UILabel(
            pygame.Rect(200,150,50,50),
            str(self.gravity_slider.get_current_value()/100.0),
            self.manager,
            self.get_container()                    

        )
        self.simulation_time_label=UILabel(
            pygame.Rect(0,250,150,50),
            'Simulation Time:',
            self.manager,
            self.get_container()
        )
        
        self.simulation_time_slider=UIHorizontalSlider(
            pygame.Rect(0,300,200,30),
            10,
            (0,100),
            self.manager,
            container=self.get_container()
        )
        self.simulation_time_slider_label=UILabel(
            pygame.Rect(200,250,50,50),
            str(self.gravity_slider.get_current_value()),
            self.manager,
            self.get_container()                    

        )
        self.apply_settings_button=UIButton(
            pygame.Rect(0,self.height-100,150,50),
            'Apply',
            self.manager,
            self.get_container()
        )
        self.reset_settings=UIButton(
            pygame.Rect(150,self.height-100,150,50),
            'Reset',
            self.manager,
            self.get_container()
        )

    
    def hide(self):
        super().hide()
        self.isHidden=True
    
    def unhide(self):
        super().show()
        self.isHidden=False
    
    def process_event(self,event):
        if self.alive() :
            if self.gravity_slider.has_moved_recently:
                self.gravity_slider_label.set_text(str(self.gravity_slider.get_current_value())+' m/s')
            if self.damping_slider.has_moved_recently:
                self.damping_slider_label.set_text(str(self.damping_slider.get_current_value()/100.0))
        if event.type==pygame.USEREVENT:
            if event.user_type==pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element==self.apply_settings_button:
                    self.screen.space._set_gravity((0,-self.gravity_slider.get_current_value()*10))
                    self.screen.space._set_damping(self.damping_slider.get_current_value()/100)
                    