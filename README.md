# A simple LaTeX \to Text telegram bot

![demo](/assets/demo.gif)

## Usage

Either go to the [chat](https://t.me/utftexbot) with the bot or type

```
@utftexbot \hbar i
```

## Dependencies

 - [utftex](https://github.com/bartp5/libtexprintf)
 - [pyTelegramBotApi](https://pytba.readthedocs.io/en/latest/index.html)

## Installation

You should have the `BOT_TOKEN` environment variable defined. It should contain your
bot token.

```bash
export BOT_TOKEN="YOURTOKENHERE"
```

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 bot.py
```
