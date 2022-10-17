import pygame
import pygame_gui
from toolBox import SimulatorToolBox
from entity import *
from modificationWindow import ModificationWindow
from SimulationZone import SimulationZone
from CursorLoader import CursorLoader 


# from EntityPropertyWindow import EntityPropertyWindow    ._____.

 
HEIGHT=720
WIDTH=1368
clock=pygame.time.Clock()
TIME_DELTA= clock.tick(60)/1000.0
colors={
    'black':(0,0,0),
    'white':(255,255,255),
    'lightBlue':(173,216,230),
    'maroon':(125,0,0)
}
# entWindow=EntityPropertyWindow(simulation_window_manager)
# def drawToolBox(manager):
#     global toolbox
  
             
#     toolbox =ToolBox(
#         relative_rect=pygame.Rect(0, 0,70 , 300),
#         layer_height=1,
#         manager=manager
#     )
#     def toggle_hide_show():
#         print('Hide Clicked')
        
        
#     x=0
#     y=0
#     change_x=True
#     change_y=False

#     toolBoxButton1=ToolBoxButton(x,y,"ball",toolbox)
#     toolBoxButton2=ToolBoxButton(30,y,"move",toolbox)
#     toolBoxButton3=ToolBoxButton(x,30,"move",toolbox)

#     #  for i in range(1,10):

#         # toolBoxButton1=ToolBoxButton(x,y,str(i),tool)
#         # if change_x :
#         #     if x==30:
#         #         x=0
#         #         change_x=False
#         #         change_y=True
#         #     else:
#         #         x=30
                
#         # if change_y:
#         #     y+=30
#         #     change_y=False
#         #     change_x=True




def initComponents():
    global show_modification_button
    global modification_window
    global SIMULATION_WINDOW_HEIGHT
    global SIMULATION_WINDOW_WIDTH
    global simulation_window
    global simulation_window_manager
    global simulator_killed
    global display
    global simulation_pause_button
    global toolbox
    global land
    global cursor_loader
    pygame.init()
    pygame.display.init()
    simulator_killed=False
    display=pygame.display.set_mode((WIDTH,HEIGHT))
    pymunk.pygame_util.positive_y_is_up = True

    SIMULATION_WINDOW_WIDTH=WIDTH
    SIMULATION_WINDOW_HEIGHT=HEIGHT
    simulation_window=SimulationZone((SIMULATION_WINDOW_WIDTH,SIMULATION_WINDOW_HEIGHT))
    simulation_window_manager=simulation_window.manager
    simulation_pause_button=pygame_gui.elements.UIButton(pygame.Rect(WIDTH-200,0,50,30),"||",simulation_window_manager)
    toolbox=SimulatorToolBox(
        simulation_window,
        pygame.Rect(0, 0,70 , 300),
        1,
        simulation_window_manager
    )
    cursor_loader=CursorLoader(simulation_window)
    land=Land(simulation_window,(0,HEIGHT-200),(WIDTH,HEIGHT))
    # land=Land(simulation_window,(0,HEIGHT-200),(WIDTH,HEIGHT-200))
    # ball=Ball(simulation_window,50).setPos(500,200)
    # ball2=Ball(simulation_window,50).setPos(700,200)
    
    



    show_modification_button=pygame_gui.elements.UIButton(pygame.Rect(WIDTH-100,0,100,30),"Modify",simulation_window_manager)
    modification_window= ModificationWindow(simulation_window,WIDTH,HEIGHT)
    modification_window.hide()
    # ball.set_elasticity(0.5)
    # ball.set_friction(0.5)
    # ball2.set_elasticity(3)
    # ball2.set_friction(10)
    land.set_elasticity(0)
    land.set_friction(1.5)
    

initComponents() 
def toggleSimulation():
    
    if simulation_window.simulation_time_state==0:
        simulation_window.simulation_time_state=1/60
        simulation_pause_button.set_text('||')

    else:
        simulation_window.simulation_time_state=0
        simulation_pause_button.set_text('|>')


def check_mouse_hits_ui(manager):
    pos=pygame.mouse.get_pos()
    for sprite_surface in manager.ui_group:
        if sprite_surface.get_relative_rect().width==WIDTH and sprite_surface.get_relative_rect().height==HEIGHT:
            continue  
        if sprite_surface.get_relative_rect().collidepoint(pos) and sprite_surface.visible:
            return True
    return False 

def manage_default_ui_element ():
    if check_mouse_hits_ui(simulation_window_manager):
        simulation_window.item_drawable=False
    else:
        simulation_window.item_drawable=True
    if event.type==pygame.USEREVENT:
            if event.user_type==pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element==show_modification_button:
                    if  modification_window.isHidden:
                        modification_window.unhide()
                        show_modification_button.set_text("Hide")
                        show_modification_button.set_position((WIDTH-400,0))
                        simulation_pause_button.set_position((WIDTH-500,0))
                    else:
                        modification_window.hide()
                        show_modification_button.set_text("Modify")
                        show_modification_button.set_position((WIDTH-100,0))
                        simulation_pause_button.set_position((WIDTH-200,0))
                if event.ui_element==toolbox.show_button:
                    
                    if toolbox.isHidden:
                        toolbox.show_button.hide()
                        toolbox.show()
                        toolbox.isHidden=False
                if event.ui_element==simulation_pause_button:
                    toggleSimulation()

def draw():
    
    simulation_window.fill(colors['lightBlue'])
    Component.renderAll()
    
    cursor_loader.render()
    
    display.blit(simulation_window,(0,0))
    simulation_window_manager.draw_ui(display)
    
    
    





while not  simulator_killed:
    if check_mouse_hits_ui(simulation_window_manager):
        cursor_loader.disable_cursor_loader()
    else:
        cursor_loader.enable_cursor_loader()
    
    draw()
    # check_mouse_hits_ui(simulation_window_manager)
    # image=pygame.image.load('image\\cursor\\circle.png')
    # image=pygame.transform.scale(image,(200,200))
    # display.blit(image,(220,220))
    
    
    # simulation_window.fill((155,155,155))
    # display.blit(simulation_window,(0,0))
    # ball.body._set_position((ball.body.position.x+1,ball.body.position.y))
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            quit()

        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_ESCAPE:
                quit()
        manage_default_ui_element()  
        # simulation_window.space.debug_draw(options)
        Component.setOnClickListenerForAll(event,simulation_window_manager)
        simulation_window_manager.process_events(event)
        

    simulation_window_manager.update(TIME_DELTA)

    simulation_window.space.step(simulation_window.simulation_time_state) 
    clock.tick(300)
    
    pygame.display.flip()
    
    