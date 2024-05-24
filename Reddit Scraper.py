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
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv, find_dotenv
import random

# A discord bot token will have to be provided
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Sets up the client to start the bot
client = discord.Client(intents=discord.Intents.default())

# When the bot goes online, print to the console
@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

# Set up commands for the bot
intents = discord.Intents.all()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Command that takes a subreddit and grabs a random picture from it, and sends it as a message in discord
@bot.command()
async def meme(ctx, arg):
    print("success")
    posts = []
    posts_grabbed = 0
    # To test you must visit https://www.reddit.com/prefs/apps and create an app and input given data
    reddit_dis = asyncpraw.Reddit(client_id="----------------", client_secret="---------------",
                              user_agent="------------")
    # Set the subreddit to be searched
    subreddit = await reddit_dis.subreddit(str(arg))
    # Grab the first 50 hot posts and select those with images
    async for submission in subreddit.hot(limit=50):
        if ".jpeg" in str(submission.url) or ".jpg" in str(submission.url) or ".png" in str(submission.url):
            # Add them to a dictionary
            posts.append({
                "title": submission.title,
                "author": str(submission.author),
                "image": submission.url
            })
            posts_grabbed += 1

    # Turn the image urls into data that can be used
    for i in range(posts_grabbed):
        with urllib.request.urlopen(posts[i]["image"]) as u:
            raw_data = u.read()
        posts[i]["image"] = raw_data

    # Create a random number to select a post to be displayed
    random_num = random.randrange(posts_grabbed)

    #Send the image and title
    image = io.BytesIO(posts[random_num]["image"])
    print("photo sent")
    await ctx.send(posts[random_num]["title"])
    await ctx.send(file=discord.File(image, 'cool_image.jpeg'))

# run the bot
bot.run(TOKEN)
client.run(TOKEN)




'''
# root window
root = Tk()

# Title of app
root.title("Reddit Scraper")

# Set size of window
root.geometry('900x600')

# Create the main frame
main_frame = Frame(root)
main_frame.pack(fill=BOTH,expand=1)

# Create canvas
my_canvas = Canvas(main_frame)
my_canvas.pack(side=LEFT,fill=BOTH,expand=1)

# Create scrollbar
y_scrollbar = Scrollbar(main_frame,orient=VERTICAL,command=my_canvas.yview)
y_scrollbar.pack(side=RIGHT, fill=Y)

my_canvas.configure(yscrollcommand=y_scrollbar.set)
my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion=my_canvas.bbox("all")))

# Create second frame to hold pictures
second_frame = Frame(my_canvas,width=10, height=10)
my_canvas.create_window((0,0), window=second_frame,anchor="nw")

# List to hold the posts and the number of posts to grab
posts = []

print(r"What subreddit do you want to browse(without 'r/'): ", end='')
newline_sub = input()
user_sub = newline_sub.strip()

print("How many posts do you want to be searched through: ", end='')
newline_num_posts = input()
num_posts = newline_num_posts.strip()
num_posts = int(num_posts)

# Set up the banner
banner = Label(second_frame, text="r/" + user_sub,bg="#FF4500", height=1, width=500, anchor=W,
               font=("Times New Roman", 32, "bold"), padx=10)
banner.pack()


async def main():
    # The number of post actually being used, as we discard videos
    posts_grabbed = 0

    # To test you must visit https://www.reddit.com/prefs/apps and create an app and input given data
    reddit = asyncpraw.Reddit(client_id="----------------", client_secret="---------------",
                              user_agent="------------")

    # Gets the subreddit and loads in the hot submissions into a dictionary
    subreddit = await reddit.subreddit(str(user_sub))
    async for submission in subreddit.hot(limit=num_posts):
        if ".jpeg" in str(submission.url) or ".jpg" in str(submission.url) or ".png" in str(submission.url):
            #print(str(submission.url))
            posts.append({
                "title": submission.title,
                "author": str(submission.author),
                "image": submission.url
            })
            posts_grabbed += 1

    for i in range(posts_grabbed):
        # Puts the post text above the picture
        title_text = Text()
        text_label = Label(second_frame, text=posts[i]["title"], font=("Times New Roman", 20), wraplength=800, padx=50)
        text_label.pack(anchor="w")

        # converts the posts grabbed to raw data to then be put in an image object
        with urllib.request.urlopen(posts[i]["image"]) as u:
            raw_data = u.read()

        image = Image.open(io.BytesIO(raw_data))

        # image is reduced to a smaller size but with same dimesions
        image.thumbnail((550,550))
        photo = ImageTk.PhotoImage(image)
        label = Label(second_frame, image=photo, height=560, width=900)
        label.image = photo
        label.pack(anchor="w")

    await reddit.close()


def regular():
    asyncio.run(main())


regular()

root.mainloop()
'''