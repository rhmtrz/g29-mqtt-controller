import pygame
import g29_controller


pygame.init()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

windowSize = (900, 600)
window = pygame.display.set_mode(windowSize)
pygame.display.set_caption("G29 Controller")

FPS = 10
clock = pygame.time.Clock()


done = False

controller = g29_controller.Controller(0)

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    
    # handle joysticks
    jsButtons = controller.get_buttons()
    jsInputs = controller.get_axis()

    steerPos = controller.get_steer()
    throtPos = controller.get_throttle()
    breakPos = controller.get_break()
    clutchPos = controller.get_clutch()

    steerV = bytes([128 + int(steerPos * 128)])
    throtV = bytes([128 + int(throtPos * 128)])
    breakV = bytes([128 + int(breakPos * 128)])
    clutchV = bytes([128 + int(clutchPos * 128)])
    if steerPos >= 0:
        ball_color = RED
    else:
        ball_color = GREEN

    window.fill(BLACK)

    plh = []
    btn = []
    axis = []
    # axisPlh = []
    axis.append(int.from_bytes(steerV))
    axis.append(int.from_bytes(throtV))
    axis.append(int.from_bytes(breakV))
    axis.append(int.from_bytes(clutchV))

    for i in range(len(jsButtons)):
        plh.append("%d")
        btn.append(jsButtons[i]) 
        # if i < 5: axisPlh.append("%d")
        
    font = pygame.font.Font('freesansbold.ttf', 32)
    ph = "  ".join(plh)
    aph = "   ".join(plh[:4])
    btn = tuple(btn)
    btnText = font.render(ph % btn, True, WHITE)
    axisText = font.render(aph % tuple(axis), True, WHITE)

    btnTextRect = btnText.get_rect()
    axisTextRect = axisText.get_rect()
    btnTextRect.center = (450, 300)
    axisTextRect.center = (450, 400)
    window.blit(btnText, btnTextRect)
    window.blit(axisText, axisTextRect)

    pygame.display.flip()
    clock.tick(FPS)

# quit app. 
pygame.quit()


