import io
import urllib.request
from tkinter import *
import time
import asyncpraw
import urllib3
import asyncio
from PIL import ImageTk, Image
import requests
from io import BytesIO



# root window
root = Tk()

# Title of app
root.title("Reddit Scraper")

# Set size of window
root.geometry('1000x600')

#Create the main frame
main_frame = Frame(root)
main_frame.pack(fill=BOTH,expand=1)

#Create canvas
my_canvas = Canvas(main_frame)
my_canvas.pack(side=LEFT,fill=BOTH,expand=1)

#Create scrollbar
y_scrollbar = Scrollbar(main_frame,orient=VERTICAL,command=my_canvas.yview)
y_scrollbar.pack(side=RIGHT, fill=Y)

my_canvas.configure(yscrollcommand=y_scrollbar.set)
my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion=my_canvas.bbox("all")))

second_frame = Frame(my_canvas,width=10, height=10, bg="lightblue")
my_canvas.create_window((0,0), window=second_frame,anchor="nw")

posts = []
numPosts = 30

# Set up the banner
banner = Label(second_frame, text="Subbreddit goes here",bg="#FF4500", height=1, width=500, anchor=W,
font=("Times New Roman", 32, "bold"))
banner.pack()

#To test you must visit https://www.reddit.com/prefs/apps and create an app and input given data
async def main():
    postsGrabbed = 0

    reddit = asyncpraw.Reddit(client_id="----------------", client_secret="---------------",
                              user_agent="------------")

    #print(reddit.read_only)

    #posts = []
    subreddit = await reddit.subreddit("cats")
    async for submission in subreddit.hot(limit=numPosts):
        if ".jpeg" in str(submission.url) or ".jpg" in str(submission.url) or ".png" in str(submission.url):
            print(str(submission.url))
            posts.append({
                "title": submission.title,
                "author": str(submission.author),
                "image": submission.url
            })
            postsGrabbed += 1



    for i in range(postsGrabbed):
        with urllib.request.urlopen(posts[i]["image"]) as u:
            raw_data = u.read()

        image = Image.open(io.BytesIO(raw_data))
        #resizedImage = image.resize((853, 480))
        image.thumbnail((500,500))
        photo = ImageTk.PhotoImage(image)
        label = Label(second_frame, image=photo, height=510, width=900)
        label.image = photo
        label.pack(anchor="w")



    await reddit.close()

#print("Display Name: ", reddit.subreddit.)

def regular():
    asyncio.run(main())

regular()








root.mainloop()