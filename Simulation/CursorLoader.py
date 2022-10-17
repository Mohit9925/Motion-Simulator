from pygame.image import load
from pygame.transform import scale
from pygame.mouse import get_pos,set_visible
class CursorLoader:
    def __init__(self,screen,image_url=None):
        self.screen=screen
        self.image_url=image_url
        self.kill_cursor_loader=True
        self.screen.cursor_loader=self

        if image_url!=None:
            self.image=load(image_url)
            self.image=scale(self.image,(50,50))
            self.kill_cursor_loader=True
            set_visible(False)
    def update_cursor(self,image_url=None):
        if not image_url:
            return 
        self.image_url=image_url

        self.image=load(self.image_url)
        self.image=scale(self.image,(50,50))
       
    


        

    
    def disable_cursor_loader(self):
        if self.image_url:
            self.kill_cursor_loader=True
            set_visible(True)
    def enable_cursor_loader(self):
        if self.image_url:
            self.kill_cursor_loader=False
            set_visible(False)


    def render(self):

        if  self.image_url==None or self.kill_cursor_loader:
            return
        pos=get_pos()
        
        
        self.screen.blit(self.image,(pos[0]-20,pos[1]-20))


    