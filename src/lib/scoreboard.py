from PIL import Image, ImageDraw, ImageFont
import discord
import time
import math
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.lib.util import remove_files_by_pattern

scoreboards = []

class Scoreboard:
    def __init__(self):
        self.id = str(round(time.time() / 1000,2))
        print(f"ID: {self.id}")

    def draw_rounded_rect(self, draw, x1, x2, y1, y2, radius, color="blue"):
        # Draw the rounded rectangle
        draw.rectangle([(x1 + radius, y1), (x2 - radius, y2)], fill=color)
        draw.rectangle([(x1, y1 + radius), (x2, y2 - radius)], fill=color)
        draw.pieslice([(x1, y1), (x1 + radius * 2, y1 + radius * 2)], 180, 270, fill=color)
        draw.pieslice([(x2 - radius * 2, y2 - radius * 2), (x2, y2)], 0, 90, fill=color)
        draw.pieslice([(x1, y2 - radius * 2), (x1 + radius * 2, y2)], 90, 180, fill=color)
        draw.pieslice([(x2 - radius * 2, y1), (x2, y1 + radius * 2)], 270, 360, fill=color)


    async def create(self, team1, team2, score1, score2):
        # Create a blank image
        WIDTH = 800
        HEIGHT = 200
        image = Image.open("./res/scoreboard.png")

        # Specify the font sizes
        score_font_size = 40
        team_font_size = 50

        # Specify the fonts
        team_font = ImageFont.truetype('arial.ttf', size=team_font_size)
        score_font = ImageFont.truetype('arial.ttf', size=score_font_size)

        def modify_text(text, MAX_WIDTH):
            current_w = 0
            result = []
            for char in text:
                w,_ = team_font.getsize(char)
                if current_w + w < MAX_WIDTH:
                    result.append(char)
                    current_w += w
                else:
                    result.append("(...)")
                    break
            return ''.join(result)

        team1 = modify_text(team1, WIDTH/2).upper()
        team2 = modify_text(team2, WIDTH/2).upper()
        score1 = modify_text(score1, 100).replace("(...)","")
        score2 = modify_text(score2, 100).replace("(...)","")

        PADDING = 35

        # Create a drawing context
        draw = ImageDraw.Draw(image)

        

        # Determine the positions for team names and scores
        team1_x = PADDING 
        team1_y = 30

        team2_x = PADDING 
        team2_y = image.height - 80

        score1_x = 650
        score1_y = team1_y + 3

        score2_x = 650
        score2_y = team2_y + 3

        # Draw the team names and scores on the image
        draw.text((team1_x, team1_y), team1, fill=(0, 0, 0), font=team_font)
        draw.text((team2_x, team2_y), team2, fill=(0, 0, 0), font=team_font)
        draw.text((score1_x, score1_y), str(score1), fill=(0, 0, 0), font=score_font)
        draw.text((score2_x, score2_y), str(score2), fill=(0, 0, 0), font=score_font)

        # Save the image to a file
        image.save(str(self.id) + 'scoreboard.png')

    def get_image(self):
        image = None
        try:
            image = discord.File(str(self.id) + 'scoreboard.png')
        except Exception as e:
            print(e)
        return image
    
    def __del__(self):
        remove_files_by_pattern('./',str(self.id) + 'scoreboard.png')
