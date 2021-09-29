"""
A discord bot which responds to messages by generating a response using a GPT model.
When a message is sent in a channel with a channel id in the list CHANNEL_IDS, the bot will generate a response and respond to the message
The bot should import the token from token.txt
The bot should import the list of channels (CHANNEL_IDS) from channels.txt
"""

import discord
from discord.ext import commands
from transformers import pipeline, set_seed
import random
import json
import os

# Imports the token from token.txt
with open("token.txt", "r") as token_file:
    TOKEN = token_file.read().strip()

# Imports the list of channels from channels.txt
with open("channels.txt", "r") as channels_file:
    CHANNEL_IDS = channels_file.read().strip().split("\n")

# Imports the owner's id from owner.txt
with open("owner.txt", "r") as owner_file:
    OWNER_ID = owner_file.read().strip()

# Imports a list of bad words from bad_words.txt
with open("bad_words.txt", "r") as bad_words_file:
    BAD_WORDS = bad_words_file.read().strip().split("\n")

# Sets the seed for the random number generator
set_seed(random.randint(0, 1000000))

class Respond_to_message(commands.Cog):
    """
    A class which contains the bot's commands
    """

    def __init__(self, bot, context_string):
        self.bot = bot
        self.context_string = context_string
        self.model = pipeline('text-generation', model='gpt2')

    @commands.command(name="generate_response")
    async def generate_response(self, ctx, *, message: str):
        """
        Generates a response to the given message
        :param ctx: The context of the command
        :param message: The message to respond to
        :return: None
        """
        
        # Gets the channel id of the channel the message was sent in
        channel_id = ctx.channel.id
        # If the channel id is in the list of channel ids, generate a response and respond to the message
        if str(channel_id) in CHANNEL_IDS:
            # Generates a response
            response = generate_response(message, self.context_string, self.model)
            # Responds to the message
            await ctx.send(response)
        # If the channel id is not in the list of channel ids, do nothing
        else:
            pass
    
    # A method which allows the owner to change the context string
    @commands.command(name="change_context")
    async def change_context(self, ctx, *, context_string: str):
        """
        Changes the context string
        :param ctx: The context of the command
        :param context_string: The new context string
        :return: None
        """
        
        # Check if the user's id is the owner's id
        if str(ctx.author.id) == OWNER_ID:
            # Change the context string
            self.context_string = context_string
            # Send a message to the user
            await ctx.send("Context string changed")

def generate_response(message: str, context_string: str, the_pipeline: pipeline = pipeline) -> str:
    """
    Generates a response to the given message
    :param message: The message to respond to
    :param the_pipeline: The pipeline to use for the generation
    :return: The generated response
    """
    # Creates a dictionary with the message and the context
    full_context_string = context_string.replace("INPUT", message)

    # Generates a response using the model
    response = the_pipeline(full_context_string, max_length=100, num_return_sequences=1)

    response = response[0]['generated_text']

    # Append the response to responses.txt
    with open("responses.txt", "a") as responses_file:
        responses_file.write(response + "\n---\n")

    response = response[len(full_context_string):]

    response = response[:response.find("\"")]

    if(response == ""):
        response = "I don't know what to say"
    
    if(contains_bad_words(response)):
        return generate_response(message, context_string, the_pipeline)

    # Returns the response
    return response


def contains_bad_words(response: str) -> bool:
    """
    Checks if the response contains a bad word
    :param response: The response to check
    :return: True if the response contains a bad word, False otherwise
    """
    for word in BAD_WORDS:
        if word in response:
            return True
    return False

def setup(bot):
    """
    Sets up the bot
    :param bot: The bot to set up
    :return: None
    """
    bot.add_cog(Respond_to_message(bot, "Me: \"INPUT\"\nBot: \""))

if __name__ == "__main__":
    # Sets up the bot
    bot = commands.Bot(command_prefix="!")
    setup(bot)
    # Starts the bot
    bot.run(TOKEN)

