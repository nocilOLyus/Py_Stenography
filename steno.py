from PIL import Image

def mod_pixels(new_img, pixels, mode, bin_str=""):
    width = new_img.width
    x, y = 0, 0
    nb_val = 0
    hid_mess = buffer = ""

    if mode == 'e':
        for pixel in pixels:
            new_pixel = list(pixel)

            for index, og_val in enumerate(pixel):
                nb_val += 1
                og_val_bin = "{:08b}".format(og_val)

                if nb_val < 9:
                    val_bin = og_val_bin[:-1] + bin_str[0]
                    bin_str = bin_str[1:]
                else:
                    nb_val = 0
                    if bin_str:
                        val_bin = og_val_bin[:-1] + '0'
                    else:
                        val_bin = og_val_bin[:-1] + '1'
                    
                val = int(val_bin, 2)
                new_pixel[index] = val
        
            new_img.putpixel((x, y), tuple(new_pixel))

            if not bin_str: return

            if x < width - 1: x += 1
            else: x, y = 0, y + 1
    
    elif mode == 'd':
        for pixel in pixels:
            new_pixel = list(pixel)

            for og_val in new_pixel:
                nb_val += 1
                og_val_bin = "{:08b}".format(og_val)

                if nb_val < 9:
                    buffer += og_val_bin[-1]
                else:
                    nb_val = 0
                    hid_mess += chr(int(buffer, 2))
                    buffer = ""
                    
                    if og_val_bin[-1] == '1':
                        return hid_mess

def encode(image):
    og_img = Image.open(image, "r")

    message = input("Message to hide (start with !file:name to choose a file): ")
    while not message:
        message = input("Message to hide (start with !file:name to choose a file): ")

    message_bin = ""
    if message[:6] == "!file:":
        with open(message[6:], "rb") as file:
            byte = file.read(1)
            while byte:
                message_bin += "{:08b}".format(ord(byte))
                byte = file.read(1)
    else:
        for char in message:
            message_bin += "{:08b}".format(ord(char))

    new_img = og_img.copy()
    pixels = iter(new_img.getdata())

    mod_pixels(new_img, pixels, 'e', message_bin)

    new_img_name = input("Modified image name: ")
    new_img.save(new_img_name)

def decode(image):
    og_img = Image.open(image)
    new_img = og_img.copy()
    pixels = iter(new_img.getdata())
    message = mod_pixels(new_img, pixels, 'd')
    print(f"\nHidden message: {message}\n")

if __name__ == "__main__":
    mode = input("Modes:\n\t1: Hide\n\t2: Seek\nSelection: ")
    while mode.lower() not in ["1", "2", "hide", "seek"]:
        mode = input("Modes:\n\t1: Hide\n\t2: Seek\nSelection: ")

    image = input("\nImage: ")

    if mode.lower() in ["1", "hide"]:
        encode(image)
    elif mode.lower() in ["2", "seek"]:
        decode(image)
