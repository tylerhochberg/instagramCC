username = ""
password = ""
accounts_to_copy_from = [] # String array of all the accounts to copy from.
base_directory = "" # Input the path of the folder this file is located in
captionStr = "" # The caption of the post




#    -----------   DON'T TOUCH ANYTHING BELOW THIS LINE -------------





# ---------- SETUP ---------- #
import PIL.Image
import instaloader
import send2trash, os, random
from instagrapi import Client
from datetime import datetime
client = Client()
loader = instaloader.Instaloader()
today = datetime.now()
# ----------       ---------- #
# ---------- VARIABLES ---------- #
img_ext = ["png", "jpg", "jpeg"]
album_ext = ["png", "jpg", "jpeg", "mp4"]
videos = []
images = []
album_list = []
downloading = -1
# ----------         ---------- #
# ---------- GATHER POST ---------- #

loader.login(username, password)
random_num = random.randint(0,len(accounts_to_copy_from)-1)
chosen_account = accounts_to_copy_from[random_num]
print(f"Chosen: {chosen_account}")
profile = instaloader.Profile.from_username(loader.context, chosen_account)
posts_to_skip = 3
videoTypeSelection = ""
while videoTypeSelection not in ["video", "image", "album"]:
    videoTypeSelection = input("Please select (video, image, album)\n")
try:
    send2trash.send2trash(f"{base_directory}\\{profile.username}")
except:
    print("Nothing Trashed")
for post in profile.get_posts():
    if posts_to_skip != 0:
        posts_to_skip-=1
        continue
    if not len(post.caption_mentions) > 0:
        if not post.is_sponsored:
            if post.typename == "GraphImage" and videoTypeSelection == "image":
                print("Downloading Img")
                loader.download_post(post, target=profile.username)
                image_dir = os.listdir(f"{base_directory}\\{profile.username}")
                new_dir = f"{base_directory}\\{profile.username}"
                images = []
                for image in image_dir:
                    for ext in img_ext:
                        if ext in image:
                            images.append(image)
                print("IMAGE:   " + str(new_dir) + images[0])
                show_image = PIL.Image.open(f"{new_dir}\\{images[0]}")
                show_image.show()
                response = ""
                while response not in ['y', 'n']:
                    response = input("Do you like this image? (y,n)\n")
                if response == 'y':
                    downloading = 0
                    break
                else:
                    send2trash.send2trash(new_dir)
                    continue
            elif post.typename == "GraphSidecar" and videoTypeSelection == "album": 
                print("Downloading Sidecar")
                loader.download_post(post, target=profile.username)
                image_list = []
                sidecar_dir = os.listdir(f"{base_directory}\\{profile.username}")
                new_dir = f"{base_directory}\\{profile.username}"
                for image in sidecar_dir:
                    for ext in album_ext:
                        if ext in image:
                            image_list.append(f"{base_directory}\\{profile.username}\\{image}")
                response = ""
                while response not in ['y', 'n']:
                    response = input("Do you like this album (manually look)? (y,n)\n")
                if response == 'y':
                    downloading = 2
                    break
                else:
                    send2trash.send2trash(new_dir)
                    continue
            elif post.typename == "GraphVideo" and videoTypeSelection == "video":
                print("Downloading Video")
                loader.download_post(post, target=profile.username)
                video_dir = os.listdir(f"{base_directory}\\{profile.username}")
                new_dir = f"{base_directory}\\{profile.username}"
                videos = []
                for video in video_dir:
                    if '.mp4' in video:
                        videos.append(video)
                print("VIDEO:   " + str(new_dir) + videos[0])
                os.startfile(f"{new_dir}\\{videos[0]}") # Play video
                response = ''
                while response not in ['y', 'n']:
                    response = input("Do you like this video? (y,n)     ")
                if response == 'y':
                    downloading = 1
                    break
                else:
                    send2trash.send2trash(new_dir)
                    continue
            else:
                continue
        else:
            continue
    else:
        continue
# ----------       ---------- #
# ---------- POST TO INSTAGRAM ---------- #
try:
    client.login(username, password)
    print("Login Success")
except:
    print("Login Failed")
if downloading == 0:
    client.photo_upload(f"{base_directory}\\{profile.username}\\{images[0]}", caption=captionStr)
    print("UPLOADED PHOTO")
elif downloading == 1:
    client.clip_upload(f"{base_directory}\\{profile.username}\\{videos[0]}", caption=captionStr) #
    print("UPLOADED REEL")
elif downloading == 2:
    client.album_upload(image_list, caption=captionStr)
else:
    print("Error Uploading")
print("Trashing File . . .")
send2trash.send2trash(f"{base_directory}\\{profile.username}")
print("File Trashed")
print("Completed.")
