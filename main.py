import cv2
import random
import numpy as np

def messageToBinary(message):
  if type(message) == str:
    return ''.join([format(ord(i), "08b") for i in message])
  elif type(message) == bytes or type(message) == np.ndarray:
    return [format(i, "08b") for i in message]
  elif type(message) == int or type(message) == np.uint8:
    return format(message, "08b")

def lsb_method_encode(image, message, isRandom = False, seed = 10):
    max_bytes = image.shape[0] * image.shape[1] * 3 // 8
    if(len(message) > max_bytes):
        raise ValueError("Image cover size not fit")
    
    message += "#####" # This delimiter is used for decode
    
    bin_message_idx = 0
    bin_message = messageToBinary(message)
    bin_message_len = len(bin_message)

    if not(isRandom):
        for values in image:
            for pixel in values:
                r, g, b = messageToBinary(pixel)
                if bin_message_idx < bin_message_len:
                    pixel[0] = int(r[:-1] + bin_message[bin_message_idx], 2)
                    bin_message_idx += 1
                if bin_message_idx < bin_message_len:
                    pixel[1] = int(g[:-1] + bin_message[bin_message_idx], 2)
                    bin_message_idx += 1
                if bin_message_idx < bin_message_len:
                    pixel[2] = int(b[:-1] + bin_message[bin_message_idx], 2)
                    bin_message_idx += 1
                if bin_message_idx >= bin_message_len:
                    break
    else:
        random.seed(seed)
        random_position = random.sample(range(0, max_bytes), bin_message_len)

        x = []
        for values in image:
            for pixel in values:
                r, g, b = messageToBinary(pixel)
                x.append(r)
                x.append(g)
                x.append(b)

        print(len(image))
        print(len(image[0]))
        print(random_position)
        print(x)
        # print(random.randint(0, max_bytes))
        # print(random.randint(0, max_bytes))
    
    # cv2.imwrite('lena-stego.png', image)


def lsb_method_decode(image):
    bin_data = ""
    for values in image:
        for pixel in values:
            r, g, b = messageToBinary(pixel)
            bin_data += r[-1]
            bin_data += g[-1]
            bin_data += b[-1]
    
    all_bytes = [bin_data[i:i+8] for i in range(0, len(bin_data), 8)]

    decoded_data = ""
    for byte in all_bytes:
        decoded_data += chr(int(byte, 2))
        print(decoded_data)
        if decoded_data[-5:] == '#####':
            break


def main():
    image = cv2.imread('lena-stego.png')
    lsb_method_encode(image, "karel", isRandom = True)

    # lsb_method_decode(image)
    # print(image.shape[0], image.shape[1])
    # max_bytes = image.shape[0] * image.shape[1] // 8
    # print(max_bytes)

if __name__ == "__main__":
    main()