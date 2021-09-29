import cv2
import math
import random
import numpy as np

EOF = "====="

def convert_to_binary(input) -> str:
    '''
    This function convert input to byte (8 bit) representation with type string.
    '''

    if type(input) == str:
        return ''.join([format(ord(char), '08b') for char in input])
    if type(input) == int or type(input) == np.uint8:
        return format(input, '08b')
    if type(input) == np.ndarray:
        return [format(el, '08b') for el in input]
    
    raise TypeError("Input type not support")

def lsb_embed(image: np.ndarray, secret_message: str, seed: int = 0) -> np.ndarray:
    '''
    This function will embed any type of secret_message to cover image using lsb method.
    This function will return new cover image.
    '''

    image_width, image_height, _ = image.shape
    message_max_bytes = (image_width * image_height * 3) // 8

    if message_max_bytes < len(secret_message):
        raise ValueError('Need bigger image to cover this message')
    
    # Add EOF
    secret_message += EOF

    bin_secret_message = convert_to_binary(secret_message)
    bin_secret_message_length = len(bin_secret_message)

    flat_image = image.flatten()
    flat_image_length = len(flat_image)
    
    seed_bin = convert_to_binary(seed % 256)
    for pos in range(8):
        curr_byte = convert_to_binary(flat_image[pos])
        flat_image[pos] = int(curr_byte[:-1] + seed_bin[pos], 2)

    # Sequential
    if seed == 0:
        for pos in range(bin_secret_message_length):
            curr_byte = convert_to_binary(flat_image[pos + 8])
            flat_image[pos + 8] = int(curr_byte[:-1] + bin_secret_message[pos], 2)
    
    # Random
    else:
        indices = [pos for pos in range(8, flat_image_length)]
        random.Random(seed).shuffle(indices)
        for pos in range(bin_secret_message_length):
            curr_byte = convert_to_binary(flat_image[indices[pos]])
            flat_image[indices[pos]] = int(curr_byte[:-1] + bin_secret_message[pos], 2)
    
    return np.reshape(flat_image, (image_width, image_height, 3))

def lsb_extract(image: np.ndarray) -> str:
    '''
    This function will extract any type of secret_message from cover image using lsb method.
    This function will return secret_message with type string.
    '''

    flat_image = image.flatten()
    flat_image_length = len(flat_image)

    seed_bin = ''
    for i in range(8):
        curr_byte = convert_to_binary(flat_image[i])
        seed_bin += curr_byte[-1]

    seed = int(seed_bin, 2)
    secret_message = ''
    lsb_image = ''

    # Sequential
    if seed == 0:
        for i in range(8, flat_image_length):
            curr_byte = convert_to_binary(flat_image[i])
            lsb_image += curr_byte[-1]

    # Random
    else:
        indices = [pos for pos in range(8, flat_image_length)]
        random.Random(seed).shuffle(indices)

        for pos in indices:
            curr_byte = convert_to_binary(flat_image[pos])
            lsb_image += curr_byte[-1]

    lsb_image_length = len(lsb_image)
    lsb_image_bytes = [lsb_image[i:i+8] for i in range(0, lsb_image_length, 8)]

    for byte in lsb_image_bytes:
        curr_char = chr(int(byte, 2))
        secret_message += curr_char
        if secret_message.endswith(EOF):
            break
        
    return secret_message[:-len(EOF)]

def get_image_psnr(image1: np.ndarray, image2: np.ndarray) -> float:
    flat_image_1 = image1.flatten()
    flat_image_2 = image2.flatten()

    diff_sum = np.sum(np.absolute(flat_image_1 - flat_image_2))
    rms = (diff_sum / len(flat_image_1)) ** 0.5
    psnr = 20 * math.log(255/rms)

    return psnr


if __name__ == "__main__":
    # Embed
    image = cv2.imread('../test/poke.png')
    f = open('../test/message.txt', 'rb')
    secret_message = ''.join([chr(x) for x in f.read()])
    new_image = lsb_embed(image, secret_message, 3)
    cv2.imwrite('../test/poke_stego.png', new_image)

    # Extract
    image = cv2.imread('../test/poke_stego.png')
    secret_message = lsb_extract(image)
    secret_message = bytes([ord(x) for x in secret_message])
    f = open('../test/message_res_2.txt', 'wb')
    f.write(secret_message)

    # Calculate psnr
    image1 = cv2.imread('../test/poke.png')
    image2 = cv2.imread('../test/poke_stego.png')
    psnr = get_image_psnr(image1, image2)