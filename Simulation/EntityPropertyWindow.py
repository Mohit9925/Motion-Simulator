from pygame_gui.elements import UIWindow,UILabel,UIButton,UITextBox,UIHorizontalSlider
from pygame import Rect
class EntityPropertyWindow(UIWindow):
    opened_window_for_entity=None
    def __init__(self,posx,posy,entity):
        super().__init__(Rect((posx,posy), (300, 300)),
                         entity.screen.manager,
                         window_display_title='Menue',
                         object_id="#guiopedia_window")
        opened_window_for_entity=entity
        label_posy=10
        for text in entity.config_dict.keys():
            print(text)
            UILabel(
                Rect(10,label_posy,80,20),
                text,
                entity.screen.manager,
                container=self.get_container()
            )
            label_posy+=50
        self.radius_label=UILabel(
            Rect(80,10,50,20),
            str(entity.radius),
            entity.screen.manager,
            self.get_container()
        )
        self.mass=UIHorizontalSlider(
            Rect(80,60,100,20),
            1,
            (0,100),
            entity.screen.manager,
            self.get_container()
            )
        self.color_label=UILabel(
            Rect(80,120,100,20),
            str(entity.color),
            entity.screen.manager,
            self.get_container()
            
        )
        
        self.moment_of_inertia=UILabel(
            Rect(100,210,50,20),
            str(entity.body._get_moment()),
            entity.screen.manager,
            self.get_container()
            )
        self.submit_btn=UIButton(Rect(10,250,100,30),
        'submit',
        opened_window_for_entity.screen.manager,
        self.get_container()
        
        )



         
    

        