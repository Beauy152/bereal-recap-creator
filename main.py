import argparse
import phonenumbers
from login import handle_login
from memories import fetch_user_memories,filter_memories,str_to_date
from images import generate_memory_images,determine_image_size,resize_images
from video import create_video_from_images

def main(args):
    BASE_URL = args.base_url
    # Using mobile code, login user & grab token
    user_token = handle_login(BASE_URL,args.phone)

    # Fetch Memories JSON
    memories_feed = fetch_user_memories(BASE_URL,user_token)
    memories_feed = filter_memories(memories_feed,args.year)
    memories_feed.sort(key=lambda x:str_to_date(x.memoryDay))

    # Download images
    image_paths = generate_memory_images(memories_feed,args.phone)

    # Verify image sizes (mins & maxs) & Resize
    max_width,max_height = determine_image_size(image_paths)
    resize_images(image_paths,max_width,max_height)

    create_video_from_images(image_paths,args.phone,args.fps)




def init_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        usage="%(prog)s [OPTION] [FILE]...", 
        description="desc tbd."
    )
    parser.add_argument(
        "-u","--url",default="http://localhost:3000",dest='base_url'
    )
    parser.add_argument(
        "-p","--phone",required=True,dest='phone'
    )
    parser.add_argument(
        "-y","--year",required=True,dest='year',type=int
    )
    parser.add_argument(
        "-f","--fps",default=4,dest='fps',type=int
    )

    return parser


def validate_phone_number(phone_num_str:str) -> str:
    # Check for leading '+'
    if phone_num_str[0] != '+':
        phone_num_str = '+' + phone_num_str

    phone_num = phonenumbers.parse(phone_num_str)
    if not phonenumbers.is_valid_number(phone_num):
        raise ValueError("Invalid Phone number.\nPlease follow the standard mobile number formatting:\n+<country code> <number>")
    
    return phone_num_str

if __name__ == '__main__':
    # Extract args here: 
    parser = init_arg_parser()
    args = parser.parse_args()

    # Validate Phone Numbers
    args.phone = validate_phone_number(args.phone)

    main(args)