import os
import cv2
import time

def get_terminal_width():
    term_size = os.get_terminal_size()
    return (term_size.columns)



def resize(frame,new_width):
    # Handle grayscale or color frame
    if len(frame.shape) == 3:
        height, width, _ = frame.shape
    else:
        height, width = frame.shape   
    aspect_ratio = height / width
    # adjust with correction factor for terminal characters
    correction = 0.55  
    new_height = int(new_width * aspect_ratio * correction)

    return cv2.resize(frame, (new_width, new_height))


def frame_to_ascii(frame):
    # convert frame to grayscale
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    # resize it to terminal window
    term_width = get_terminal_width()
    resized_frame = resize(gray,term_width)
    # get intensity
    pixels = resized_frame.flatten()
    # map with ascii characters
    ascii_string = "".join([ascii_table[int(pixel)*len(ascii_table) // 256] for pixel in pixels])
    ascii_image = "\n".join(ascii_string[i:i+term_width] for i in range(0,len(pixels),term_width))

    return ascii_image




video_path = r"C:\Users\hbggy\Downloads\sm.mp4"
ascii_table = "     .'`^\",:;Il!i><~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"
clip = cv2.VideoCapture(video_path)

if not clip.isOpened():
    print(f"Error: Couldn't open video")

fps = clip.get(cv2.CAP_PROP_FPS)
delay = 1/fps if fps > 0 else 0.04

frame_count = 0
print(f"Playing... Press Ctrl+C to stop.")
time.sleep(2)
try:
    while True:
        ret,frame = clip.read()
        if ret:
            ascii_art = frame_to_ascii(frame)
            frame_count += 1
            os.system('cls' if os.name == 'nt' else 'clear')
            print(ascii_art)
        else:
            break
        time.sleep(delay)

except KeyboardInterrupt:
    print("\nPlayback stopped")
finally:
    print(f"Processed: {frame_count} frames")
    clip.release()


# import argpase
# add audio