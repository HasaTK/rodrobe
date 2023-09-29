# Roblox Clothing Bot (WIP)
A discord roblox clothing bot for your group. 

![](https://cdn.discordapp.com/attachments/1154068857879793674/1155502142161956905/image.png)
## Features
  - Clothing uploader 
  - Group clothing stealer
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
3) Open the file named `.env.example` and fill in the fields appropriately (example)
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

# Asset Prices

# The robux price for shirts and pants which will be used when a shirt/pant is republished
ITEM_PRICE = 5  
# The robux price for a t-shirt which will be used when a tshirt is republished
TSHIRT_PRICE = 3 
```
4) Rename the file to `.env`
5) Create a file called `description.txt` in the `config` folder and write a description. This will be used for when the bot uploads clothing
6) Run this main.py file
```console
$ python3 main.py
```

## TODO:
- Add more clothing/group configurable functions
- Ratelimit handler