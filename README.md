# Super-Smart-Chatbot
A discord bot which responds to messages using [GPT-2](https://huggingface.co/gpt2).

![image](https://user-images.githubusercontent.com/43968991/206881069-42076bc8-5b5d-42ae-b215-b7b3aea570c1.png)
![image](https://user-images.githubusercontent.com/43968991/206881082-f2d8fff8-12c1-4e13-a8c6-9eed5c85d142.png)

Is it perfect? Absolutely not! This was being done as more of a tech demo/experiment than as a final product, and for that, it works amazingly!

## Running the bot

To set up the bot:

```bash
git clone https://github.com/2br-2b/Super-Smart-Chatbot/
cd Super-Smart-Chatbot
pip install -r requirements.txt
```

Then, create the file `token.txt` which contains soley the bot's token.

Create `channels.txt`. In this file, put any number of channel ids separated by line breaks. The bot will automatically respond to any message sent in these channels in addition to DMs and commands.

Create `owner.txt`. In this file, put one user id number, the id number of the bot's owner.

**Even if you don't plan on using any channels or having a bot owner, create these files and leave them empty.**

To run the bot, write:
```python
python3 main.py
```
