from pythonping import ping
from unicornhatmini import UnicornHATMini
from colorsys import hsv_to_rgb
from PIL import Image, ImageDraw, ImageFont
import time
import csv
import sys

unicornhatmini = UnicornHATMini()
seconds = time.time()

class pingStats_cycle:
    def __init__(self):
        self.ping_total   = 0
        self.ping_success = 0
        self.ping_failure = 0
        self.rtt = []

    def print_pingstats(self):
            print("Total pings: " + str(self.ping_total), "\nSuccesses: " + str(self.ping_success), "\nFailures: " + str(self.ping_failure))

    def append_rtt(self, rtt):
        self.rtt.append(rtt)
    
    def get_avg_rtt(self):
        avg = round((sum(self.rtt))/(len(self.rtt)), 2)
        return avg

    def reset_cycle(self):
        self.ping_total   = 0
        self.ping_success = 0
        self.ping_failure = 0
        self.rtt.clear()


class pingHistory:
    def __init__(self):
        self.index = 0
        self.interval = 1441
        self.day_failures = [0] * self.interval
    
    def queue_fails(self, failures):
        self.day_failures[self.index] = failures
        self.index += 1
        if(self.index >= self.interval):
            self.index = 0

    def total_fails(self):
        failed_pings = 0
        for x in range (0, self.interval-1):
            failed_pings += self.day_failures[x]
        return failed_pings


def append_file(ping_total, ping_successes, ping_failures, avg_rtt):
    
    #fields = ['time', 'ping total', 'ping successes', 'ping failures', 'avg rtt', 'ok']
    fields = [time.strftime("%m/%d/%Y, %H:%M:%S", time.localtime()), str(ping_total), str(ping_successes), str(ping_failures), str(avg_rtt)+" ms"]
    print(fields)

    with open('pingstats.csv', 'a') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(fields)
    csvfile.close()

def text_draw(font, display_width, display_height, lost_pings):
    
    text = str(lost_pings)

    # Measure the size of our text, we only really care about the width for the moment
    # but we could do line-by-line scroll if we used the height
    text_width, text_height = font.getsize(text)

    # Create a new PIL image big enough to fit the text
    image = Image.new('P', (text_width + display_width + display_width, display_height), 0)
    draw = ImageDraw.Draw(image)


    # Draw the text into the image
    draw.text((display_width, -1), text, font=font, fill=255)

    offset_x = display_width - (display_width - text_width)/2

    print("text width is: " + str(text_width) + "  |   offset x is:" + str(offset_x))

    for y in range(0, 6):
        for x in range(display_width):
            #hue = 160 #(time.time() / 10.0) + (x / float(display_width * 2))
            #r, g, b = [int(c * 255) for c in hsv_to_rgb(hue, 1.0, 1.0)]
            if image.getpixel((x + offset_x, y-1)) == 255:
                unicornhatmini.set_pixel(x, y, 0, 0, 255)
            else:
                unicornhatmini.set_pixel(x, y, 0, 0, 0)

    unicornhatmini.show()


def main():
    
    rotation = 180
    if len(sys.argv) > 1:
        try:
            rotation = int(sys.argv[1])
        except ValueError:
            print("Usage: {} <rotation>".format(sys.argv[0]))
            sys.exit(1)

    unicornhatmini.set_rotation(rotation)
    display_width, display_height = unicornhatmini.get_shape()

    print("{}x{}".format(display_width, display_height))

    # Do not look at unicornhatmini with remaining eye
    unicornhatmini.set_brightness(0.5)

    # Load a nice 5x7 pixel font
    # Granted it's actually 5x8 for some reason :| but that doesn't matter
    font = ImageFont.truetype("5x7.ttf", 8)

    



    wait = 0
    wait2 = time.time() + 720
    cycle = pingStats_cycle()
    day = pingHistory()
    
    while(True):
        
        time.sleep(1)
        seconds = time.time()
        
        if((wait + 60) < seconds):
            
            wait = time.time()
            fails = 0

            for i in range (0, 15):
                unicornhatmini.set_pixel(i+1, 6, 0, 0, 0) #x, y, r, g, b
            
            for x in range (0, 15):
                unicornhatmini.set_pixel(x+1, 6, 0, 0, 200) #x, y, r, g, b
                unicornhatmini.show()
                
                while True:
                    try:
                        response_list = ping("8.8.8.8", verbose=True, timeout=3, count=1, interval=0)
                    except:
                        time.sleep(1)
                        continue
                    break
                
                fail = int(response_list.packet_loss)
                fails += fail
                if(fail):
                    unicornhatmini.set_pixel(x+1, 6, 200, 0, 0) #x, y, r, g, b
                if(not fail):
                    unicornhatmini.set_pixel(x+1, 6, 0, 200, 0) #x, y, r, g, b
                unicornhatmini.show()

                cycle.ping_total += 1
                cycle.ping_success += int(1 - response_list.packet_loss)
                cycle.ping_failure += fail
                cycle.append_rtt(response_list.rtt_avg_ms)
                time.sleep(1)

            day.queue_fails(fails)

            cycle.print_pingstats()
            print("\nFAILS IN 24 HOURS = " + str(day.total_fails()))
            
            text_draw(font, display_width, display_height, day.total_fails())
            

        if((wait2 + 600) < seconds):
            wait2 = time.time()
            append_file(cycle.ping_total, cycle.ping_success, cycle.ping_failure, cycle.get_avg_rtt())
            cycle.reset_cycle()


main()