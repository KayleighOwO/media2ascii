from PIL import Image, ImageOps, ImageGrab
import cv2
import os
import time
import pyautogui as pag

# 70 levels of grey
grey_scale_HD = r'$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,"^`. '

# 10 levels of grey
grey_scale_SD = r'@%#*+=-:. '

# Code to convert image to ASCII
def convert_to_ascii(image, highres=False):
    try:
        # Resize the image
        width, height = image.size
        aspect_ratio = height / width
        #new_width = 378    CHANGE BACK
        new_width = 132
        new_height = aspect_ratio * new_width * 0.55
        image = image.resize((new_width, int(new_height)))

        # Convert image to greyscale
        image = image.convert('L')
        image = ImageOps.invert(image)

        # Convert to ASCII
        pixels = image.getdata()

        if highres:
            new_pixels = [grey_scale_HD[int((len(grey_scale_HD) - 1) * pixel / 255)] for pixel in pixels]
        else:
            new_pixels = [grey_scale_SD[int((len(grey_scale_SD) - 1) * pixel / 255)] for pixel in pixels]

        new_pixels = ''.join(new_pixels)

        # Split string of chars into multiple strings of length equal to new width and create a list
        new_pixels_count = len(new_pixels)
        ascii_image = [new_pixels[i:i + new_width] for i in range(0, new_pixels_count, new_width)]
        ascii_image = '\n'.join(ascii_image)
        return ascii_image
    except Exception as e:
        print(f'Error converting image to ASCII: {e}')
        return None

class VideoToASCII:
    def __init__(self):
        self.choice = None
        self.resolution = None

    def get_user_choice(self):
        while True:
            print('Choose an option:')
            print('1. Input a video file')
            print('2. Use recorded video')
            print('3. Convert an image to ASCII')

            try:
                self.choice = int(input('Choose an option: '))
                if self.choice not in [1, 2, 3]:
                    print('Invalid choice. Please choose 1, 2, or 3.')
                else:
                    break
            except ValueError:
                print('Invalid input. Please enter a number.')

        while True:
            print('Choose a resolution:')
            print('1. HD (High resolution)')
            print('2. SD (Low resolution)')
            
            try:
                resolution_choice = int(input('Choose a resolution: '))
                if resolution_choice == 1:
                    self.resolution = True
                    break
                elif resolution_choice == 2:
                    self.resolution = False
                    break
                else:
                    print('Invalid choice. Please choose 1 or 2.')
            except ValueError:
                print('Invalid input. Please enter a number.')

    # Using convert_to_ascii() method, convert frames of a video to ASCII
    def video_to_ascii(self):
        if self.choice == 1:
            video_path = input('Enter the path to the video file: ')
            if not os.path.exists(video_path):
                print('Video file not found.')
                return

            # Open the video file
            capture = cv2.VideoCapture(video_path)

            # Set the frame rate (optional)
            fps = 30

            while True:
                # Read a frame from the video
                frame_exists, frame = capture.read()
                if not frame_exists:
                    break

                # Convert the frame to grayscale
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                # Convert the grayscale frame to a PIL Image
                image = Image.fromarray(gray)

                # Convert the image to ASCII art
                ascii_frame = convert_to_ascii(image, self.resolution)

                # Clear the terminal screen
                os.system('cls' if os.name == 'nt' else 'clear')

                # Display the ASCII art frame
                print(ascii_frame)

                # Add a delay to control the frame rate
                cv2.waitKey(int(1000 / fps))

            # Release the video capture object
            capture.release()

        elif self.choice == 2:
            fps = int(input('Enter the frames per second: '))

            # Initialize previous time
            prev = time.time()

            while True:
                try:
                    time_elapsed = time.time() - prev
                    img = pag.screenshot('fb.png')

                    if time_elapsed > 1.0/fps:
                        prev = time.time()

                        # Convert the image to ASCII art
                        ascii_frame = convert_to_ascii(img, self.resolution)

                        # Clear the terminal screen
                        os.system('cls' if os.name == 'nt' else 'clear')

                        # Display the ASCII art frame
                        print(ascii_frame)

                except KeyboardInterrupt:
                    print('Recording stopped by user.')
                    break
                except Exception as e:
                    print(f'Error recording screen: {e}')
                    break

        elif self.choice == 3:
            image_path = input('Enter the path to the image file: ')
            if not os.path.exists(image_path):
                print('Image file not found.')
                return

            image = Image.open(image_path)
            ascii_image = convert_to_ascii(image, self.resolution)
            print(ascii_image)

def main():
    try:
        video_to_ascii = VideoToASCII()
        video_to_ascii.get_user_choice()
        video_to_ascii.video_to_ascii()
    except Exception as e:
        print(f'Error: {e}')

if __name__ == '__main__':
    main()