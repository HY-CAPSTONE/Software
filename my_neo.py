import board
import neopixel
import time

# brightness - overall brightness of LED
# fill - Color all pixels a given color
# show - Udate LED colors if auto_write is set to False

# initailize
#pixels = neopixel.NeoPixel(board.D18, 30)
# red in first NeoPixel 
#pixels[0] = (255, 0, 0)
# fill all NeoPixels in green
#pixels.fill((0, 255, 0))
# pixels.show()
 

pixel_pin = board.D18
num_pixels = 8

ORDER = neopixel.GRB

pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=1, auto_write=False, pixel_order=ORDER)

def doNeoPixel():
    pixels[0] = (239, 0, 0)
    pixels[1] = (0, 70, 255)
    pixels[2] = (239, 0, 0)
    pixels[3] = (0, 70, 255)
    pixels[4] = (239, 0, 0)
    pixels[5] = (0, 70, 255)
    pixels[6] = (239, 0, 0)
    pixels[7] = (0, 70, 255)

    pixels.show()

def stopNeoPixel():
    pixels.fill((0,0,0))
    pixels.show() 

def doMoodNeoPixel():
	pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.2, auto_write=False, pixel_order=ORDER)
	#FF9800
	pixels.fill((255,152,0 ))
	pixels.show()
	

if __name__ == "__main__":
    pixels[0] = (239, 0, 0)
    pixels[1] = (0, 70, 255)
    pixels[2] = (239, 0, 0)
    pixels[3] = (0, 70, 255)
    pixels[4] = (239, 0, 0)
    pixels[5] = (0, 70, 255)
    pixels[6] = (239, 0, 0)
    pixels[7] = (0, 70, 255)


    pixels.show()
    time.sleep(3)
    stopNeoPixel()
else :
    pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=1, auto_write=False, pixel_order=ORDER) 
    # do nothing
