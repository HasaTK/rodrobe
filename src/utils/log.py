import colorama 

from colorama import Fore,Style
from typing   import Optional

def info(content: str, prefix: Optional[str] = "-"):

    color = Fore.LIGHTBLUE_EX
    print(f"{Style.BRIGHT}[{color}{prefix}{Fore.RESET}]: {content} {Style.RESET_ALL}")


def error(content: str, prefix: Optional[str] = "-"):

    color = Fore.LIGHTRED_EX
    print(f"{Style.BRIGHT}[{color}{prefix}{Fore.RESET}]: {content} {Style.RESET_ALL}")

def success(content: str, prefix: Optional[str] = "-"):

    color = Fore.LIGHTGREEN_EX
    print(f"{Style.BRIGHT}[{color}{prefix}{Fore.RESET}]: {content} {Style.RESET_ALL}")