# RoDrobe - A roblox clothing bot [WIP]
A discord roblox clothing bot for your group.If you have any requests/features in mind which are not already implemented, please let me know.

![](https://cdn.discordapp.com/attachments/1154068857879793674/1155502142161956905/image.png)
## Features
  - Clothing uploader 
  - Group clothing stealer
  - Auto robux to USD converter with configurable rates 
     
    (Shows for every command with robux amount displayed + the sales notifier )
  - Clothing downloader
  - Watermark Remover
  - Sales notifier
  - Group Balance viewer

## Commands
Check out the documentation (located in the "docs" folder if the link doesn't work) for a description on what each command does and how to use them


## Installation
1) Install [python 3.11](https://www.python.org/downloads/release/python-3115/)
2) Open your terminal and run the following:
```console
$ git clone https://github.com/soakingdry/rodrobe
$ cd rodrobe
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
bot_whitelist = [1,21231] # put the whitelisted discord ids in here
# discord bot token
bot_token = ""

[assets]
# The robux price for a shirt/pant which will be used when a shirt/pant is republished
item_price = 5
# # The robux price for a t-shirt which will be used when a tshirt is republished
tshirt_price = 5

[other]
debug_mode=false
# The time the program will retry after if it a ratelimit occurs
ratelimit_wait_time=4
```
4) Rename the  `.toml.example` file to `.toml` once you have filled in the appropriate fields
5) Create a file called `description.txt` in the `config` folder and write a description. This will be used for when the bot uploads clothing
6) Run this main.py file
```console
$ python3 main.py
```

# TODO:
  - Add docs for commands
  - Make uploader & holder globals
  - Add a roblox front page scraper/uploader [WIP]
  - Add color to logs
