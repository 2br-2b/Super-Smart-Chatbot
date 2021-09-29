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
import names
from better_profanity import profanity

# Imports the token from token.txt
with open("token.txt", "r") as token_file:
    TOKEN = token_file.read().strip()

# Imports the list of channels from channels.txt
with open("channels.txt", "r") as channels_file:
    CHANNEL_IDS = channels_file.read().strip().split("\n")

# Imports the owner's id from owner.txt
with open("owner.txt", "r") as owner_file:
    OWNER_ID = owner_file.read().strip()

# Imports a list of prompts from prompts.txt
with open("prompts.txt", "r") as prompts_file:
    PROMPTS = prompts_file.read().strip().split("\n")

# Sets the seed for the transformers library
set_seed(random.randint(0, 1000000))

# Add censor words to the profanity filter from a file
with open("bad_words.txt", "r") as bad_words_file:
    BAD_WORDS = bad_words_file.read().strip().split("\n")
profanity.add_censor_words(BAD_WORDS)

class Respond_to_message(commands.Cog):
    """
    A class which contains the bot's commands
    """

    def __init__(self, bot):
        self.bot = bot
        self.model = pipeline('text-generation', model='gpt2')


    @commands.command(name="generate_response", help="Generates a response to a message", aliases=["gr"])
    async def generate_response(self, ctx, *, message: str):
        """
        Generates a response to the given message
        :param ctx: The context of the command
        :param message: The message to respond to
        :return: None
        """
        
        # Imports a list of prompts from prompts.txt
        with open("prompts.txt", "r") as prompts_file:
            PROMPTS = prompts_file.read().strip().split("\n")

        async with ctx.channel.typing():
            # Generates a response
            response = generate_response(message, self.model)
            # Responds to the message
            await ctx.reply(response)

    # On each new message in a channel whose ID is in the list CHANNEL_IDS, the bot will generate a response and respond to the message
    @commands.Cog.listener()
    async def on_message(self, message):
        """
        On each new message in a channel whose ID is in the list CHANNEL_IDS, the bot will generate a response and respond to the message
        :param message: The message to respond to
        :return: None
        """

        # If the message is in a channel whose ID is in the list CHANNEL_IDS, the bot will generate a response and respond to the message
        # It should not respond to its own messages
        if str(message.channel.id) in CHANNEL_IDS and message.author.id != self.bot.user.id:
            async with message.channel.typing():
                # Generates a response
                response = generate_response(message.content, self.model)
                # Responds to the message
                await message.channel.send(response)

    # A command which send a message in a channel whose ID is mentioned in the command
    @commands.command(name="send_message", help="Sends a message in a channel whose ID is mentioned in the command", aliases=["sm"])
    async def send_message(self, ctx, channel_id: int, *, message: str):
        """
        Sends a message in a channel whose ID is mentioned in the command
        :param ctx: The context of the command
        :param channel_id: The channel to send the message in
        :param message: The message to send
        :return: None
        """

        if str(channel_id) not in CHANNEL_IDS:
            return

        # Make sure that the message was sent by the bot owner
        if ctx.author.id != OWNER_ID:
            return

        # Sends a message in a channel whose ID is mentioned in the command
        channel = self.bot.get_channel(channel_id)
        await channel.send("message")

def generate_response(message: str, the_pipeline: pipeline, recursion_count: int = 0) -> str:
    """
    Generates a response to the given message
    :param message: The message to respond to
    :param the_pipeline: The pipeline to use for the generation
    :return: The generated response
    """

    if recursion_count > 10:
        return "Error: could not generate a proper response!"

    # Creates a dictionary with the message and the context
    full_context_string = random.choice(PROMPTS).replace("INPUT", message).replace("\\n", "\n")

    while "NAME" in full_context_string:
        full_context_string = full_context_string.replace("NAME", names.get_first_name(), 1)

    # Generates a response using the model
    response = the_pipeline(full_context_string, max_length=100, num_return_sequences=1)

    response = response[0]['generated_text']

    if(contains_bad_words(response)):
        return generate_response(message, the_pipeline, recursion_count + 1)

    # Append the response to responses.txt
    with open("responses.txt", "a") as responses_file:
        responses_file.write(response + "\n---\n")

    response = response[len(full_context_string):]

    response = response[:response.find("\"")]

    if(response == ""):
        return generate_response(message, the_pipeline, recursion_count + 1)

    # Returns the response
    return response


def contains_bad_words(response: str) -> bool:
    """
    Checks if the response contains a bad word
    :param response: The response to check
    :return: True if the response contains a bad word, False otherwise
    """
    return profanity.contains_profanity(response)
    
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

