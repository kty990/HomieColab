import re
import requests
import time
from validators import url
import glob
import os


async def DEFAULT_COMMAND_ACTION(ctx):
    await ctx.send('Hello, world!')

def is_url(str):
    try:
        if url(str):
            return True
        else:
            return False
    except Exception as e:
        print(f"Error processing is_url({str}): {e}")
        return False

def remove_files_by_pattern(directory, pattern):
    files = glob.glob(os.path.join(directory, pattern))
    for file in files:
        os.remove(file)

async def GenerateURL(query):
    print("GenerateURL called.")
    # regex: (?:https?:\/\/)?(?:www\.)?youtu(?:\.be\/|be.com\/\S*(?:watch|embed)(?:(?:(?=\/[-a-zA-Z0-9_]{11,}(?!\S))\/)|(?:\S*v=|v\/)))([-a-zA-Z0-9_]{11,})
    videoRegex = "(?:https?:\/\/)?(?:www\.)?youtu\.?be(?:\.com)?\/?.*(?:watch|embed)?(?:.*v=|v\/|\/)([\w\\-_]+)\&?"
    if re.search(videoRegex, query):
        print("Returning url")
        return query
    elif re.search("(?:https?:\/\/)?(?:www\.)?youtube\.com\/playlist\?list=[\w\-]+", query):
        print("playlist")
        # Generate a valid URL
        queryURL = query  # playlist URL

        data = []
        finished = False
        res = requests.get(queryURL)
        body = res.content.decode('utf-8')
        firstVideoIndex = body.lower().find('watch?v=')
        try:
            while firstVideoIndex != -1:
                videoId = body[firstVideoIndex:firstVideoIndex + 19]
                ap = '\''
                v = videoId.split(ap)[0].split('\\u0026')[0]
                link = f"https://www.youtube.com/{v}"
                print(f"Link: {link}")
                if link not in data:
                    data.append(link)
                firstVideoIndex = body.lower().find('watch?v=', firstVideoIndex + 1)
                print(f"Attempting to get next video with firstVideoIndex: {firstVideoIndex}")
            finished = True
        except Exception as e:
            print(e)

        while not finished:
            time.sleep(0.5)

        print(f"Returning: {data or None}")
        return data or None
    else:
        print("query")
        # Generate a valid URL
        localQuery = query.replace(" ", "+")
        queryURL = f"https://www.youtube.com/results?search_query={localQuery}"

        data = None

        res = requests.get(queryURL)
        body = res.content.decode('utf-8')
        try:
            firstVideoIndex = body.lower().find('watch?v=')
            videoId = body[firstVideoIndex:firstVideoIndex + 19]
            ap = '\''
            data = videoId.split(ap)[0].split('\\u0026')[0]
            link = f"https://www.youtube.com/{data}"
            print(f"Link: {link}")
            data = link
        except Exception as e:
            print(e)

        while not data:
            time.sleep(0.5)

        print(f"Returning: {data or None}")
        return data or None
