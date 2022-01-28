from PIL import Image

def mod_pixels(new_img, pixels, bin_str):
    width = new_img.width
    x, y = 0, 0
    nb_val = 0

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


def encode():
    img = input("Image: ")
    og_img = Image.open(img, "r")
    message = input("Message to hide: ")
    message_bin = ""
    for char in message:
        message_bin += "{:08b}".format(ord(char))

    new_img = og_img.copy()
    pixels = list(new_img.getdata())

    mod_pixels(new_img, pixels, message_bin)

    new_img_name = input("Modified image name: ")
    new_img.save(new_img_name)

if __name__ == "__main__":
    encode()