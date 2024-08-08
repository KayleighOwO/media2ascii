from PIL import Image, ImageOps
import cv2
import os

# 70 levels of grey
grey_scale_HD = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~i!lI;:,\\^`. "

# 10 levels of grey
grey_scale_SD = "@%#*+=-:. "

def convert_to_ascii(image, highres=False):
    # Resize the image
    width, height = image.size
    aspect_ratio = height / width
    #new_width = 40
    new_width = 378
    new_height = aspect_ratio * new_width * 0.55
    image = image.resize((new_width, int(new_height)))

    # Convert image to greyscale
    image = image.convert("L")
    image = ImageOps.invert(image)

    # Convert to ASCII
    pixels = image.getdata()

    if highres == True:
        new_pixels = [grey_scale_HD[int((len(grey_scale_HD) - 1) * pixel / 255)] for pixel in pixels]
    else:
        new_pixels = [grey_scale_SD[int((len(grey_scale_SD) - 1) * pixel / 255)] for pixel in pixels]

    new_pixels = "".join(new_pixels)

    # Split string of chars into multiple strings of length equal to new width and create a list
    new_pixels_count = len(new_pixels)
    ascii_image = [new_pixels[i:i + new_width] for i in range(0, new_pixels_count, new_width)]
    ascii_image = "\n".join(ascii_image)
    return ascii_image

def video_to_ascii(video_path, highres=False):
    # Open the video file
    cap = cv2.VideoCapture(video_path)

    # Set the frame rate (optional)
    fps = 30

    while True:
        # Read a frame from the video
        ret, frame = cap.read()
        if not ret:
            break

        # Convert the frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Convert the grayscale frame to a PIL Image
        image = Image.fromarray(gray)

        # Convert the image to ASCII art
        ascii_frame = convert_to_ascii(image, highres)

        # Clear the terminal screen
        os.system('cls' if os.name == 'nt' else 'clear')

        # Display the ASCII art frame
        print(ascii_frame)

        # Add a delay to control the frame rate
        cv2.waitKey(int(1000 / fps))

    # Release the video capture object
    cap.release()

def main():
    print("""
1. Image to ASCII
2. Video to ASCII
""")

    try:
        choice = int(input("Choose an option: "))
    except:
        print("Not a valid option. Defaulting to Image to ASCII")
        choice = 1

    match choice:
        case 1:
            print("""
1. SD (Default)
2. HD
            """)

            try:
                definition = int(input("Choose a resolution: "))
            except:
                print("Not a valid option. Defaulting to SD Mode")
                definition = 1

            match definition:
                case 1:
                    highres = False
                case 2:
                    highres = True

            if highres == True:
                print("HD Mode\n")
            else:
                print("SD Mode\n")

            path = input("Enter the path to the image file: ")

            try:
                img = Image.open(path)
                ascii_image = convert_to_ascii(img, highres)
                print(ascii_image)

                # Write to a text file.
                with open("sample_ascii_image.txt", "w") as f:
                    f.write(ascii_image)
            except:
                print(path, "Unable to find image")

        case 2:
            print("""
1. SD (Default)
2. HD
            """)

            try:
                definition = int(input("Choose a resolution: "))
            except:
                print("Not a valid option. Defaulting to SD Mode")
                definition = 1

            match definition:
                case 1:
                    highres = False
                case 2:
                    highres = True

            if highres == True:
                print("HD Mode\n")
            else:
                print("SD Mode\n")

            video_path = input("Enter the path to the video file: ")
            video_to_ascii(video_path, highres)

if __name__ == "__main__":
    main()