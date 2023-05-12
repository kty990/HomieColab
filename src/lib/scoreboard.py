from PIL import Image, ImageDraw, ImageFont, ImageOps
import discord
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

scoreboards = []

GRAYSCALE = [(x,x,x) for x in range(0,256)]

class Scoreboard:
    def __init__(self, custom_id_prefix=""):
        self.id = custom_id_prefix + str(len(scoreboards) + 1)

    def draw_rounded_rect(self, draw, x1, x2, y1, y2, radius, color="blue"):
        # Draw the rounded rectangle
        draw.rectangle([(x1 + radius, y1), (x2 - radius, y2)], fill=color)
        draw.rectangle([(x1, y1 + radius), (x2, y2 - radius)], fill=color)
        draw.pieslice([(x1, y1), (x1 + radius * 2, y1 + radius * 2)], 180, 270, fill=color)
        draw.pieslice([(x2 - radius * 2, y2 - radius * 2), (x2, y2)], 0, 90, fill=color)
        draw.pieslice([(x1, y2 - radius * 2), (x1 + radius * 2, y2)], 90, 180, fill=color)
        draw.pieslice([(x2 - radius * 2, y1), (x2, y1 + radius * 2)], 270, 360, fill=color)


    async def create(self, team1, score1, RGB=(100,99,100,255)):
        # Create a blank image
        WIDTH = 800
        HEIGHT = 100
        image = Image.open("./res/scoreboard.png")
        image = image.convert("RGBA")

        def change_color(old_color, new_color):
            if isinstance(old_color,list):
                for x in range(image.width):
                    for y in range(image.height):
                        r,g,b,a = image.getpixel((x,y))
                        if (r,g,b) in old_color:
                            image.putpixel((x, y),new_color)
            else:
                for x in range(image.width):
                    for y in range(image.height):
                        r,g,b,a = image.getpixel((x,y))
                        if (r,g,b) == old_color:
                            image.putpixel((x, y),new_color)

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

        team1 = modify_text(team1, WIDTH/5*2).upper()
        score1 = modify_text(score1, 100).replace("(...)","")

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
        draw.text((score1_x, score1_y), str(score1), fill=(0, 0, 0), font=score_font)

        change_color((255,255,255),RGB)
        change_color(GRAYSCALE,(0,0,0,0))
        

        # Save the image to a file
        image.save(str(self.id) + 'scoreboard.png')
        image.close()

    def get_image(self):
        image = None
        try:
            image = discord.File(str(self.id) + 'scoreboard.png')
        except Exception as e:
            print(e)
        return image
    
    async def stack(self, *args):
        imgs = []
        output_w, output_h = 0, 0
        for sb in args:
            i = Image.open(str(sb.id) + "scoreboard.png")
            print(f"{str(sb.id)}: {i.height}")
            imgs.append(i)
            if i.width > output_w:
                output_w = i.width
            output_h += i.height
        img = Image.new("RGB", (output_w, output_h))
        print(f"Final height: {output_h}")
        curr_h = 0
        for i in imgs:
            img.paste(i, (0, curr_h))
            curr_h += i.height
            i.close()
        img.save(str(self.id) + "stacked_scoreboard.png")
        img.close()