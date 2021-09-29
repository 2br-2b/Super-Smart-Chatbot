"""
A discord bot which responds to messages by generating a response using a GPT model.
When a message is sent in a channel with a channel id in the list CHANNEL_IDS, the bot will generate a response and respond to the message
The bot should train itself on the messages it has already seen
The bot should import the token from token.txt
The bot should import the list of channels from channels.txt
"""

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

# Sets the seed for the random number generator
set_seed(42)

class Respond_to_message(commands.Cog):
    """
    A class which contains the bot's commands
    """

    def __init__(self, bot):
        self.bot = bot

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
        if channel_id in CHANNEL_IDS:
            # Generates a response
            response = generate_response(message)
            # Responds to the message
            await ctx.send(response)
        # If the channel id is not in the list of channel ids, do nothing
        else:
            pass


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
    response = the_pipeline(full_context_string, max_length=200, num_return_sequences=1)
    # Returns the response
    return response[0]['generated_text']


def setup(bot):
    """
    Sets up the bot
    :param bot: The bot to set up
    :return: None
    """
    bot.add_cog(Respond_to_message(bot))


if __name__ == "__main__":
    # Sets up the bot
    bot = commands.Bot(command_prefix="!")
    setup(bot)
    # Starts the bot
    bot.run(TOKEN)
    