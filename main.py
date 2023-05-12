import pygame
import g29_controller
import paho.mqtt.client as mqtt

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




def on_connect(client, userdata, flag, rc):
  print("Connected with result code " + str(rc))

def on_disconnect(client, userdata, rc):
  if rc != 0:
     print("Unexpected disconnection.")

# def on_publish(client, userdata, mid):
#   print("publish: {0}".format(mid))

def main():
    done = False
    controller = g29_controller.Controller(0)

    client = mqtt.Client()                
    client.on_connect = on_connect        
    client.on_disconnect = on_disconnect  
    # client.on_publish = on_publish   

    client.connect("mqtt.devwarp.work", 1883, 60) 

    client.loop_start()  

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
        
        # handle joysticks
        jsButtons = controller.get_buttons()
        jsInputs = controller.get_axis()

        window.fill(BLACK)

        plh = []
        btn = []
        axis = []
        arrBuffer = []

        for i in range(len(jsButtons)):
            plh.append("%d")
            btn.append(jsButtons[i])
            arrBuffer.append(int(jsButtons[i]))

            if i < 4:
                v = bytes([128 + int(jsInputs[i] * 128)])
                axis.append(int.from_bytes(v))
                arrBuffer.append(int.from_bytes(v))

        client.publish('g29', bytearray(arrBuffer))
        font = pygame.font.Font('freesansbold.ttf', 32)
        plhS = "  ".join(plh)
        aPlhS = "   ".join(plh[:4])

        btnText = font.render(plhS % tuple(btn), True, WHITE)
        axisText = font.render(aPlhS % tuple(axis), True, WHITE)

        btnTextRect = btnText.get_rect()
        axisTextRect = axisText.get_rect()
        btnTextRect.center = (450, 200)
        axisTextRect.center = (450, 300)
        window.blit(btnText, btnTextRect)
        window.blit(axisText, axisTextRect)

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == '__main__':        
    main()  


# quit app. 
pygame.quit()