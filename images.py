from memories import Memory
import requests
import os
from PIL import Image
import io
import numpy as np
# import matplotlib.pyplot as plt
import cv2
from tqdm import tqdm

def overlay_images(back_img,front_img,RESIZE_FACTOR=0.3,OFFSET=30):
    result = front_img.copy()

    # Resize image B to % of its original size
    height, width, _ = back_img.shape
    new_width = int(width * RESIZE_FACTOR)
    new_height = int(height * RESIZE_FACTOR)
    resized_back_img = cv2.resize(back_img, (new_width, new_height))

    # Calculate the top-right coordinates for overlapping
    top_left_x = result.shape[1] - resized_back_img.shape[1]
    top_left_y = 0

    # Paste the resized image B onto the result
    # Calculate the top-left coordinates for overlapping
    top_left_x = result.shape[1] - resized_back_img.shape[1] - OFFSET
    top_left_y = OFFSET

    # Paste the resized image B onto the result
    result[top_left_y:top_left_y + resized_back_img.shape[0], top_left_x:top_left_x + resized_back_img.shape[1]] = resized_back_img

    return result


def fetch_images(memory:Memory):
    front_img = requests.get(url=memory.secondary.url)
    back_img = requests.get(url=memory.primary.url)

    if front_img.status_code == 200 and back_img.status_code == 200:
        front_img = Image.open(io.BytesIO(front_img.content))
        # Convert the front image to RGBA format if it's not already
        if front_img.mode != 'RGBA':
            front_img = front_img.convert('RGBA')
        front_img = np.array(front_img)

        back_img = Image.open(io.BytesIO(back_img.content))
        if back_img.mode != 'RGBA':
            back_img = back_img.convert('RGBA')
        back_img = np.array(back_img)

    else:
        raise ValueError("Failed to fetch one or more images...")

    return front_img,back_img


def generate_memory_images(memory_feed:list[Memory],phone_num:str) -> list[str]:

    if not os.path.exists(f'./{phone_num}/'):
        os.mkdir(f'./{phone_num}')

    image_paths = []
    for memory in tqdm(memory_feed,total=len(memory_feed),desc='Fetching Images...'):
        image_path = f'./{phone_num}/{memory.memoryDay}.png'
        if not os.path.exists(image_path):
            front,back = fetch_images(memory)
            result = overlay_images(back,front)

            # Convert the RGB image to BGR format
            result = cv2.cvtColor(result, cv2.COLOR_RGB2BGR)
            cv2.imwrite(image_path,result)

        image_paths.append(image_path)

    return image_paths

def determine_image_size(image_paths:list[str]) -> tuple[int,int]:

    image_sizes = [(img.width,img.height) for img in 
        (Image.open(image_path) for image_path in image_paths)]

    max_width = max(image_sizes,key=lambda x:x[0])[0]
    max_height = max(image_sizes,key=lambda x:x[1])[1]

    #TODO: Could insert some logic to pick new default size (min or max)
    return (max_width,max_height)

def resize_images(image_paths:list[str],max_width:int,max_height:int) -> None:

    for image_path in tqdm(image_paths,total=len(image_paths),desc='Resizing Images...'):
        image = Image.open(image_path)

        if (image.width != max_width) or (image.height != max_height):
            image = image.resize((max_width,max_height))
            image.save(image_path,'png')