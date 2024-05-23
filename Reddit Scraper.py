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
posts = []

# Set up the banner
banner = Label(root, text="Subbreddit goes here",bg="#FF4500", height=1, width=500, anchor=W,
font=("Times New Roman", 32, "bold"))
banner.pack()

async def main():
    reddit = asyncpraw.Reddit(client_id="----------------", client_secret="---------------",
                              user_agent="------------")

    #print(reddit.read_only)

    #posts = []
    subreddit = await reddit.subreddit("memes")
    async for submission in subreddit.hot(limit=10):
        posts.append({
            "title": submission.title,
            "author": str(submission.author),
            "image": submission.url
        })

    for i in range(10):
        print(posts[i])

    print(posts[4]["image"])

    with urllib.request.urlopen("https://i.redd.it/y2r4uhez26sc1.gif") as u:
        raw_data = u.read()

    image = Image.open(io.BytesIO(raw_data))
    photo = ImageTk.PhotoImage(image)
    label = Label(root, image=photo)
    label.image = photo
    label.pack()

    await reddit.close()

#print("Display Name: ", reddit.subreddit.)

def regular():
    asyncio.run(main())

regular()








root.mainloop()