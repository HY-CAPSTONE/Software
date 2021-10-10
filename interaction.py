import time
import argparse

from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.core.legacy import text
from luma.core.legacy.font import proportional, LCD_FONT




serial = spi(port=0, device= 0, gpio=noop())
device = max7219(serial, width = 16, height = 16, rotate= 0, block_orientation=90)

def tempState(temp_state):
    # 온도값에 따라 temp_emoji다르게 설정
    if temp_state == 0:
        temp_emoji = [[0,0,0,0,0,1,1,1,1,1,1,0,0,0,0,0],
                   [0,0,0,1,1,0,0,0,0,0,0,1,1,0,0,0],
                   [0,0,1,0,0,0,0,0,0,0,0,0,0,1,0,0],
                   [0,1,0,0,0,0,0,0,0,0,0,0,0,0,1,0],
                   [0,1,0,0,1,1,0,0,0,0,1,1,0,0,1,0],
                   [1,0,0,1,1,1,1,0,0,1,0,0,1,0,0,1],
                   [1,0,0,0,1,1,0,0,0,0,0,0,0,0,0,1],
                   [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                   [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                   [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                   [1,0,0,1,0,0,0,0,0,0,0,0,1,0,0,1],
                   [0,1,0,0,1,0,0,0,0,0,0,1,0,0,1,0],
                   [0,1,0,0,0,1,1,1,1,1,1,0,0,0,1,0],
                   [0,0,1,0,0,0,0,0,0,0,0,0,0,1,0,0],
                   [0,0,0,1,1,0,0,0,0,0,0,1,1,0,0,0],
                   [0,0,0,0,0,1,1,1,1,1,1,0,0,0,0,0]]

    elif temp_state == 1:
        temp_emoji= [[0,0,0,0,0,1,1,1,1,1,1,0,0,0,0,0],
                [0,0,0,1,1,0,0,0,0,0,0,1,1,0,0,0],
                [0,0,1,0,0,0,0,0,0,0,0,0,0,1,0,0],
                [0,1,0,0,1,0,0,0,0,0,0,1,0,0,1,0],
                [0,1,0,1,0,0,0,0,0,0,0,0,1,0,1,0],
                [1,0,1,0,0,0,0,0,0,0,0,0,0,1,0,1],
                [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                [1,0,0,1,0,0,1,0,0,1,0,0,1,0,0,1],
                [1,0,0,0,1,1,0,0,0,0,1,1,0,0,0,1],
                [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                [0,1,0,0,0,0,0,0,0,0,0,0,0,0,1,0],
                [0,1,0,0,0,0,1,1,1,1,0,0,0,0,1,0],
                [0,0,1,0,0,0,1,1,1,1,0,0,0,1,0,0],
                [0,0,0,1,1,0,0,1,1,0,0,1,1,0,0,0],
                [0,0,0,0,0,1,1,1,1,1,1,0,0,0,0,0]]

    elif temp_state == 2:
        temp_emoji= [[0,0,0,0,0,1,1,1,1,1,1,0,0,0,0,0],
                [0,0,0,1,1,0,0,0,0,0,0,1,1,0,0,0],
                [0,0,1,0,0,0,0,0,0,0,0,0,0,1,0,0],
                [0,1,0,0,1,0,0,0,0,0,0,1,0,0,1,0],
                [0,1,0,1,0,0,0,0,0,0,0,0,1,0,1,0],
                [1,0,1,0,0,0,0,0,0,0,0,0,0,1,0,1],
                [1,0,0,0,1,0,0,0,0,0,0,1,0,0,0,1],
                [1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1],
                [1,0,0,0,0,0,1,0,0,1,0,0,0,0,0,1],
                [1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1],
                [1,0,0,0,1,0,0,0,0,0,0,1,0,0,0,1],
                [0,1,0,0,0,0,0,0,0,0,0,0,0,0,1,0],
                [0,1,0,0,0,0,1,1,1,1,0,0,0,0,1,0],
                [0,0,1,0,0,1,0,0,0,0,1,0,0,1,0,0],
                [0,0,0,1,1,0,0,0,0,0,0,1,1,0,0,0],
                [0,0,0,0,0,1,1,1,1,1,1,0,0,0,0,0]]

    return temp_emoji


   
def waterState(water_state):
    # 물 수위값에 따라서 emoji다르게 설정
    if water_state == 0:
        water_emoji = [[0,0,0,0,0,1,1,1,1,1,1,0,0,0,0,0],
                   [0,0,0,1,1,0,0,0,0,0,0,1,1,0,0,0],
                   [0,0,1,0,0,0,0,0,0,0,0,0,0,1,0,0],
                   [0,1,0,0,0,0,0,0,0,0,0,0,0,0,1,0],
                   [0,1,0,0,1,1,0,0,0,0,1,1,0,0,1,0],
                   [1,0,0,1,1,1,1,0,0,1,0,0,1,0,0,1],
                   [1,0,0,0,1,1,0,0,0,0,0,0,0,0,0,1],
                   [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                   [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                   [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                   [1,0,0,1,0,0,0,0,0,0,0,0,1,0,0,1],
                   [0,1,0,0,1,0,0,0,0,0,0,1,0,0,1,0],
                   [0,1,0,0,0,1,1,1,1,1,1,0,0,0,1,0],
                   [0,0,1,0,0,0,0,0,0,0,0,0,0,1,0,0],
                   [0,0,0,1,1,0,0,0,0,0,0,1,1,0,0,0],
                   [0,0,0,0,0,1,1,1,1,1,1,0,0,0,0,0]]
    elif water_state == 1:
        water_emoji =[[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                    [0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                    [0,0,1,0,0,0,0,0,0,0,1,1,1,1,1,0],
                    [0,0,0,1,0,0,0,0,0,1,1,1,0,0,1,1],
                    [0,0,0,0,1,0,0,0,1,1,1,1,1,0,0,1],
                    [0,0,0,0,0,1,0,1,1,1,1,1,1,1,0,1],
                    [0,0,0,0,0,0,1,0,1,1,1,1,1,1,1,0],
                    [0,0,0,0,0,0,0,1,0,1,1,1,1,1,1,1],
                    [0,0,0,0,0,0,0,0,1,0,1,1,1,1,1,0],
                    [0,0,0,1,0,0,1,1,1,1,0,1,1,1,0,0],
                    [0,0,0,1,1,1,1,1,1,1,1,0,1,0,0,0],
                    [0,0,0,1,1,0,0,0,0,0,0,1,0,0,0,0],
                    [0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0],
                    [0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0],
                    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0],
                    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1]]
    
    return water_emoji

def sunState():
    # 물 수위값에 따라서 emoji다르게 설정
    if sun_state == 0:
        sun_emoji = [[0,0,0,0,0,1,1,1,1,1,1,0,0,0,0,0],
                   [0,0,0,1,1,0,0,0,0,0,0,1,1,0,0,0],
                   [0,0,1,0,0,0,0,0,0,0,0,0,0,1,0,0],
                   [0,1,0,0,0,0,0,0,0,0,0,0,0,0,1,0],
                   [0,1,0,0,1,1,0,0,0,0,1,1,0,0,1,0],
                   [1,0,0,1,1,1,1,0,0,1,0,0,1,0,0,1],
                   [1,0,0,0,1,1,0,0,0,0,0,0,0,0,0,1],
                   [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                   [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                   [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                   [1,0,0,1,0,0,0,0,0,0,0,0,1,0,0,1],
                   [0,1,0,0,1,0,0,0,0,0,0,1,0,0,1,0],
                   [0,1,0,0,0,1,1,1,1,1,1,0,0,0,1,0],
                   [0,0,1,0,0,0,0,0,0,0,0,0,0,1,0,0],
                   [0,0,0,1,1,0,0,0,0,0,0,1,1,0,0,0],
                   [0,0,0,0,0,1,1,1,1,1,1,0,0,0,0,0]]

    elif sun_state == 1:
        sun_emoji =[[0,0,0,1,0,0,0,1,0,0,1,0,0,0,1,0],
                [0,0,0,0,1,0,0,1,0,0,1,0,0,1,0,0],
                [0,1,0,0,0,1,0,1,0,0,1,0,1,0,0,0],
                [0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,1],
                [0,0,0,1,0,0,1,1,1,1,1,0,0,0,1,0],
                [0,0,0,0,0,1,1,1,1,1,1,1,0,0,0,0],
                [1,1,1,0,1,1,1,1,1,1,1,1,1,0,1,1],
                [0,0,0,0,1,1,1,1,1,1,1,1,1,0,0,0],
                [0,0,0,0,1,1,1,1,1,1,1,1,1,0,0,0],
                [1,1,1,0,1,1,1,1,1,1,1,1,1,0,1,1],
                [0,0,0,0,1,1,1,1,1,1,1,1,0,0,0,0],
                [0,0,0,0,0,1,1,1,1,1,1,0,0,0,0,0],
                [0,0,1,0,0,0,1,1,1,1,1,0,0,0,1,0],
                [0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                [1,0,0,0,1,0,0,1,0,0,1,0,1,0,0,0],
                [0,0,0,1,0,0,0,1,0,0,1,0,0,1,0,0]]



    elif sun_state == 2:
        sun_emoji = [[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                    [0,1,0,0,1,0,0,1,0,0,1,0,0,1,0,0],
                    [0,0,1,0,0,1,0,1,0,0,1,0,1,0,0,0],
                    [0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,1],
                    [0,0,0,0,1,0,1,1,1,1,1,0,0,0,1,0],
                    [0,0,0,0,0,1,0,1,1,1,1,1,0,0,0,0],
                    [0,1,1,0,1,0,1,0,1,1,1,1,1,0,1,1],
                    [0,0,0,0,1,1,0,1,0,1,1,1,1,0,0,0],
                    [0,0,0,0,1,1,1,0,1,0,1,1,1,0,0,0],
                    [0,1,1,0,1,1,1,1,0,1,0,1,1,0,1,1],
                    [0,0,0,0,1,1,1,1,1,0,1,0,0,0,0,0],
                    [0,0,0,0,0,1,1,1,1,1,0,1,0,0,0,0],
                    [0,0,1,0,0,0,1,1,1,1,1,0,1,0,1,0],
                    [0,1,0,0,0,0,0,0,0,0,0,0,0,1,0,1],
                    [0,0,0,0,1,0,0,1,0,0,1,0,0,0,1,0],
                    [0,0,0,1,0,0,0,1,0,0,1,0,0,0,0,1]]
    
    return sun_emoji







def showtempMatrix(temp_state):
    # create matrix device
    print("Created device")
    temp_emoji = tempState(temp_state)
    
              
    with canvas(device) as draw:
        for y in range(16):
            for x in range(16):
                if(temp_emoji[x][y]==1):
                    draw.point((x, y), fill="green")
    time.sleep(3)

def showwaterMatrix(water_state):
    # create matrix device
    print("Created device")

    water_emoji = waterState(water_state)
    
              
    with canvas(device) as draw:
        for y in range(16):
            for x in range(16):
                if(water_emoji[x][y]==1):
                    draw.point((x, y), fill="green")
    time.sleep(3)


def showsunMatrix(sun_state):
    # create matrix device
    print("Created device")

    
    
              
    with canvas(device) as draw:
        for y in range(16):
            for x in range(16):
                if(sun_emoji[x][y]==1):
                    draw.point((x, y), fill="green")
    time.sleep(3)

        
