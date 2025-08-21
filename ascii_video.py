import os
import cv2
import time
import argparse

class AsciiPlayer:

    def __init__(self,video_path,width):
        self.video_path = video_path
        self.ascii_table = "     .'`^\",:;Il!i><~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"
        self.clip = cv2.VideoCapture(video_path)
        if not self.clip.isOpened():
            raise IOError(f"Error: Couldn't open video")
        self.width_is_dynamic = (width is None)
        if self.width_is_dynamic:
            self.new_width = os.get_terminal_size().columns
        else:
            self.new_width = width
        self.fps = self.clip.get(cv2.CAP_PROP_FPS)
        self.delay = 1/self.fps if self.fps > 0 else 0.04

    def resize(self,frame):
        if len(frame.shape) == 3:
            height, width, _ = frame.shape
        else:
            height, width = frame.shape   
        aspect_ratio = height / width
        # adjust with correction factor for terminal characters
        correction = 0.55  
        self.new_height = int(self.new_width * aspect_ratio * correction)

        return cv2.resize(frame, (self.new_width, self.new_height))


    def frame_to_ascii(self,frame):
        # convert frame to grayscale
        gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        # resize it to terminal window
        resized_frame = self.resize(gray)
        # get intensity
        pixels = resized_frame.flatten()
        # map with ascii characters
        ascii_string = "".join([self.ascii_table[int(pixel)*len(self.ascii_table) // 256] for pixel in pixels])
        ascii_image = "\n".join(ascii_string[i:i+self.new_width] for i in range(0,len(pixels),self.new_width))
        return ascii_image

    def play(self):
        frame_count = 0
        print(f"Playing... Press Ctrl+C to stop.")
        time.sleep(2)
        while True:
            ret,frame = self.clip.read()
            if ret:
                if self.width_is_dynamic:
                    self.new_width = os.get_terminal_size().columns
                ascii_art = self.frame_to_ascii(frame)
                frame_count += 1
                os.system('cls' if os.name == 'nt' else 'clear')
                print(ascii_art)
            else:
                break
            time.sleep(self.delay)
        self.clip.release()
        return frame_count


# command line arguments
parser = argparse.ArgumentParser(description="Play videos as ASCII art in terminal.")
parser.add_argument("video_path",help="The path of the video file to play.") 
parser.add_argument("-w","--width",
                    type=int,
                    default=None,
                    help="Width of the video output. Defaults to the current terminal width")
args = parser.parse_args()


if __name__ == "__main__":
    try:
        player = AsciiPlayer(args.video_path,args.width)
        frame_count = player.play()
        print(f"Processed: {frame_count} frames")
    except IOError as e:
        print(e)
    except KeyboardInterrupt:
        print("\nPlayback stopped")
    finally:
        player.clip.release()
    