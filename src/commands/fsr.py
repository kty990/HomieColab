import sys
import os
import random

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.lib import event
from src.lib.embed import new_embed
from src.lib import discord_integration

prompts = [
    "You shouldn't do in public",
    "Things you wouldn't want to find in your bed",
    "Words to describe your private parts",
    "Types of people who should be sterilized",
    "Types of people who should be deported",
    "Ways to use a vibrator without it turning you on",
    "Things you wouldn't want to see your parents doing",
    "Things you shouldn't do with your partner's parents",
    "Ways to get out of a traffic ticket",
    "Things that can make you go blind",
    "Things you wouldn't want to find in your food",
    "Things you wouldn't want to do in a public restroom",
    "Things you wouldn't want to hear from your boss",
    "Things you shouldn't say to a police officer",
    "Things you shouldn't do during a job interview",
    "Things you shouldn't do on a first date",
    "Things you wouldn't want to hear from your gynecologist",
    "Things you wouldn't want to hear from your proctologist",
    "Things you wouldn't want to hear from your dentist",
    "Things you wouldn't want to hear from your accountant",
    "Things you wouldn't want to hear from your lawyer",
    "Things you wouldn't want to hear from your therapist",
    "Things you wouldn't want to hear from your mechanic",
    "Things you wouldn't want to hear from your hairdresser",
    "Things you wouldn't want to hear from your tattoo artist",
    "Things you wouldn't want to hear from your bartender",
    "Things you wouldn't want to hear from your flight attendant",
    "Things you wouldn't want to hear from your waiter",
    "Things you wouldn't want to hear from your landlord",
    "Things you wouldn't want to hear from your neighbor",
    "Things you wouldn't want to hear from your in-laws",
    "Things you wouldn't want to hear from your spouse",
    "Things you wouldn't want to hear from your child",
    "Things you wouldn't want to hear from your pet",
    "Things you wouldn't want to hear from your doctor",
    "Things you wouldn't want to hear from your nurse",
    "Things you wouldn't want to hear from your pharmacist",
    "Things you wouldn't want to hear from your teacher",
    "Things you wouldn't want to hear from your boss's boss",
    "Things you wouldn't want to hear on a first date",
    "Things you wouldn't want to find in your parents' bedroom",
    "Things you wouldn't want to hear from your parents about their sex life",
    "Things you wouldn't want to hear from your parents about their drug use",
    "Things you wouldn't want to hear from your therapist about your childhood",
    "Things you wouldn't want to hear from your partner about their ex",
    "Things you wouldn't want to hear from your partner about your ex",
    "Things you wouldn't want to hear from your partner about their sexual history",
    "Things you wouldn't want to hear from your partner about your sexual history",
    "Things you wouldn't want to find in your partner's browser history",
    "Things you wouldn't want to find in your partner's phone",
    "Things you wouldn't want to hear from your partner while having sex",
    "Things you wouldn't want to hear from your partner while cuddling",
    "Things you wouldn't want to hear from your partner while fighting",
    "Things you wouldn't want to hear from your partner's parents about your relationship",
    "Things you wouldn't want to hear from your partner's ex about your relationship",
    "Things you wouldn't want to hear from your partner's current lover about your relationship",
    "Things you wouldn't want to hear from your partner's previous lover about your relationship",
    "Things you wouldn't want to hear from your partner's therapist about your relationship",
    "Things you wouldn't want to hear from your partner's lawyer about your relationship",
    "Things you wouldn't want to hear from your partner's boss about your relationship",
    "Things you wouldn't want to hear from your partner's best friend about your relationship",
    "Things you wouldn't want to hear from your partner's worst enemy about your relationship",
    "Things you wouldn't want to hear from your partner's siblings about your relationship",
    "Things you wouldn't want to hear from your partner's children about your relationship",
    "Things you wouldn't want to hear from your partner's pets about your relationship",
    "Things you wouldn't want to hear from your partner's ex about your sex life",
    "Things you wouldn't want to hear from your partner's current lover about your sex life",
    "Things you wouldn't want to hear from your partner's previous lover about your sex life",
    "Things you wouldn't want to hear from your partner's therapist about your sex life",
    "Things you wouldn't want to hear from your partner's lawyer about your sex life",
    "Things you wouldn't want to hear from your partner's boss about your sex life",
    "Things you wouldn't want to hear from your partner's best friend about your sex life",
    "Things you wouldn't want to hear from your partner's worst enemy about your sex life",
    "Things you wouldn't want to hear from your partner's siblings about your sex life",
    "Things you wouldn't want to hear from your partner's children about your sex life",
    "Things you wouldn't want to hear from your partner's pets about your sex life",
    "Things you wouldn't want to hear from your partner's ex about your private parts",
    "Things you wouldn't want to hear from your partner's current lover about your private parts",
    "Things you wouldn't want to hear from your partner's previous lover about your private parts",
    "Things you wouldn't want to hear from your partner's therapist about your private parts",
    "Things you wouldn't want to hear from your partner's lawyer about your private parts",
    "Things you wouldn't want to hear from your partner's boss about your private parts",
    "Things you wouldn't want to hear from your partner's best friend about your private parts",
    "Things you wouldn't want to hear from your partner's worst enemy about your private parts",
    "Things you wouldn't want to hear from your partner's siblings about your private parts",
    "Things you wouldn't want to hear from your partner's children about your private parts",
    "Things you wouldn't want to hear from your partner's pets about your private parts",
    "Things you wouldn't want to hear from your therapist about your fantasies",
]

#Convert to lowercase
prompts = [x.lower() for x in prompts]

description = """Five Second Rule: Uncensored. A game where you must say 3 things about a given category before 5 seconds elapses. WIP."""

async def run(ctx, *args):
    e = new_embed("Five Second Rule!","Sorry, but this command/game is currently in development and not ready to be tested. Check back later!",0xff0000)
    await discord_integration.send_message(ctx,None,e)