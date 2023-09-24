# Roblox Clothing Bot (WIP)
A roblox clothing bot for discord.

![](https://cdn.discordapp.com/attachments/1154068857879793674/1155502142161956905/image.png)
## Features
  - Auto robux to USD converter with configurable rates
  - Clothing downloader
  - Watermark Remover
  - Sales notifier
  - Group Balance viewer

## Installation
1) Install [the latest version of python](https://www.python.org/)
2) Open your terminal and run the following:
```console
$ git clone https://github.com/soakingdry/roblox-clothing-bot
$ cd roblox-clothing-bot
$ pip3 install -r requirements.txt
```
3) Open the file named `.env.example` and fill in the fields
```env
#  Account Cookies
HOLDER_COOKIE="holder_cookie_here"
UPLOADER_COOKIE="account_cookie_here"

# Group ID
GROUP_ID=100000

# Discord 
DISCORD_WEBHOOK="https://discord.com/api/webhooks/..."
DISCORD_BOT_PREFIX="!"
DISCORD_BOT_WHITELIST=[id1,id2,id3,...]
DISCORD_BOT_TOKEN="bot_token_here"
```
4) Rename the file to `.env`
5) Run this main.py file
```console
$ python3 main.py
```

## TODO:
- Add discord bot loader to main.py
- Add item stealing and mass group downloader
- Add categorys to help command
- Add more clothing/group configurable functions(e.g set price of all/specific clothing, etc..)
- Ratelimit handler