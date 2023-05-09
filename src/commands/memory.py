import sys
import os
import random
import asyncio
import copy
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.lib import event
from src.lib.embed import new_embed
from src.lib import discord_integration

description = """"""

sequences = {
    'easy': [1, 3, 5, 7, 9, 11, 13, 15, 17, 19],
    'medium': ['abacus', 'billiards', 'cabana', 'diorama', 'ephemeral', 'fjord', 'gazebo', 'hyacinth', 'impromptu', 'jejune'],
    'hard': ['pneumonoultramicroscopicsilicovolcanoconiosis', 'floccinaucinihilipilification', 'antidisestablishmentarianism', 'supercalifragilisticexpialidocious', 'hippopotomonstrosesquippedaliophobia'],
    'expert': ['Greece', 'Ireland', 'Switzerland', 'Denmark', 'Netherlands', 'Sweden', 'Norway', 'Finland', 'Austria', 'Belgium'],
    'ultimate': ['mercury', 'venus', 'earth', 'mars', 'jupiter', 'saturn', 'uranus', 'neptune', 'pluto (dwarf planet)'],
    'challenging': ['aleph', 'beth', 'gimel', 'daleth', 'he', 'waw', 'zayin', 'heth', 'teth', 'yodh'],
    'difficult': ['rhinoceros', 'hippopotamus', 'crocodile', 'alligator', 'giraffe', 'elephant', 'penguin', 'gorilla', 'orangutan', 'lemur', 'okapi', 'tapir', 'wombat', 'platypus', 'sloth'],
    'advanced': ['magenta', 'turquoise', 'vermilion', 'chartreuse', 'scarlet', 'lavender', 'teal', 'maroon', 'goldenrod', 'crimson', 'indigo', 'fuchsia', 'amethyst', 'periwinkle', 'coral'],
    'pro': ['durian', 'jackfruit', 'lychee', 'passionfruit', 'rambutan', 'starfruit', 'dragonfruit', 'kiwano', 'mangosteen', 'custard apple', 'carambola', 'jabuticaba', 'mamey sapote', 'persimmon', 'cherimoya']
}


async def run(ctx, *args):
    await discord_integration.send_message(ctx,None,new_embed("Memory","This game is currently in early stages. Please check back later.",0xff0000))