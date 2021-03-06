from PIL import Image, ImageDraw, ImageFont, ImageChops

def decode_image(path_to_png):
    """
    Input: path_to_png: String
    Output: None
    Description: Decodes the hidden message in a png image file.
    Takes the image, looks at the red channel of the given image and
    creates a new black and white image based on the least significant bit (LSB)
    for each pixel in the original image. 
    ==> (If the LSB is 1, the new image's pixel will be white, else the pixel will be black)
    """
    # Open the image using PIL:
    encoded_image = Image.open(path_to_png)

    # Separate the red channel from the rest of the image:
    red_channel = encoded_image.split()[0]

    # Create a new PIL image with the same size as the encoded image:
    decoded_image = Image.new("RGB", encoded_image.size)
    pixels = decoded_image.load()
    x_size, y_size = encoded_image.size

    # loop through x_size and y_size
    for x in range(x_size):
        for y in range(y_size):
            # => .getpixel returns the pixel value at a given position
            # CONFUSED on what the & operator is doing...
            # convert each red channel pixel value into a binary string, then check if the string ends in 0 or 1

            # if pixel string ends with 0, the pixel at x_size, y_size == black
            if bin(red_channel.getpixel((x, y)))[-1] == '0':
                pixels[x, y] = (0, 0, 0)
            # if ends with 1, the pixel at x_size, y_size == white
            else:
                pixels[x, y] = (255, 255, 255)
                
    # print(red_channel)  # Start coding here!

    # DO NOT MODIFY. Save the decoded image to disk:
    decoded_image.save("my_decoded_text.png")


def encode_image(encode_text, path_to_png="my_encoded_img.png"):
    """
    Input: encode_text: String, path_to_png: String
    Output: None
    Description: Encodes a secret message in the red channel into a separate copy 
    of the desired image and saves it to the img file.
    """
    # grab the original image
    orig_img = Image.open(path_to_png)

    # Split the different color channels into variables
    red_channel = orig_img.split()[0]
    green_channel = orig_img.split()[1]
    blue_channel = orig_img.split()[2]

    x_size = orig_img.size[0]
    y_size = orig_img.size[1]

    image_text = write_text(orig_img.size, encode_text)

    # make blank image for text
    encoded_img = Image.new('RGB', (x_size, y_size))
    pixels = orig_img.load()

    # loop through x_size and y_size
    for x in range(x_size):
        for y in range(y_size):
            # get channel values for pixels at x and y
            red_channel_pix = red_channel.getpixel((x,y))
            green_channel_pix = green_channel.getpixel((x,y))
            blue_channel_pix = blue_channel.getpixel((x,y))
            # set the new image's pixel value for x and y to be the same as the base img
            encoded_img.putpixel((x,y), (red_channel_pix, green_channel_pix, blue_channel_pix))
            # check if red channel is odd number
            if red_channel_pix % 2 == 1:
                # make the pixel even
                red_channel_pix -= 1
                # reset our new image's x and y pixel to the new value
                encoded_img.putpixel((x,y), (red_channel_pix, green_channel_pix, blue_channel_pix))
            # combine the new image and secret image
    new_img = ImageChops.add(encoded_img, image_text)

    new_img.save("my_encoded_img.png")

def write_text(img_size, desired_text):
    """
    Input: img_size: Tuple, desired_text: String
    Output: Image
    Description: Writes a text in black to a white image and returns it.
    """
    # create an image
    img_txt = Image.new('RGB', img_size, (1,0,0))

    # get a drawing context
    draw = ImageDraw.Draw(img_txt)

    # write black text
    draw.multiline_text((10,10), desired_text, fill=(0,0,0))
    return img_txt


encode_text = "You sneaky little programmer..."
path_to_png = "my_encoded_img.png"
# encode_image(encode_text, path_to_png)
decode_image(path_to_png)
