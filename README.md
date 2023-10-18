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

## Commands
The bot will tell you if you are missing an argument. For more guidance on these commands, type !command_here. 
- steal  - Uploads the asset to your group
- revenue - Gives an overview of the groups revenue(conversion included)
- download - Shows template of an asset
- get - Gets the config specified
- set - Sets the config specified to a given value 
- help - Gives a list of all commands
- sgroup - Republishes all the assets an existing group has to your group

## Installation
1) Install [the latest version of python](https://www.python.org/)
2) Open your terminal and run the following:
```console
$ git clone https://github.com/soakingdry/roblox-clothing-bot
$ cd roblox-clothing-bot
$ pip3 install -r requirements.txt
```
3) Open the file named `.toml.example` and fill in the fields appropriately (example)
-  it is adviced not to use your main account for the UPLOADER cookie since there is a risk of termination

```toml
[group]
holder_cookie = "holder account cookie here"
# dont use your main account or the uploader
uploader_cookie = "uploader account cookie" 
# your group id
group_id = 0

[discord]
# the webhook used for sales notifications
sales_webhook = ""
# prefix of the bot.. slash commands may be supported in the future
bot_prefix = "!"
bot_whitelist = [your_discord_id_here,21231,...]
# discord bot token
bot_token = ""

[assets]
# The robux price for a shirt/pant which will be used when a shirt/pant is republished
item_price = 5
# # The robux price for a t-shirt which will be used when a tshirt is republished
tshirt_price = 5
```
4) Rename the  `.toml.example` file to `.toml` once you have filled in the appropriate fields
5) Create a file called `description.txt` in the `config` folder and write a description. This will be used for when the bot uploads clothing
6) Run this main.py file
```console
$ python3 main.py
```

## TODO:
- Add more clothing/group configurable functions
- Ratelimit handler