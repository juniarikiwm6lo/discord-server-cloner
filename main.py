
import asyncio
import os
import platform
import sys
import time
import traceback

import discord
import inquirer
import psutil
from art import text2art
from cloner import Clone
from colorama import Fore, init, Style
from rich.console import Console
from rich.panel import Panel as RichPanel
from rich.progress import Progress
from rich.table import Table

# Constants
VERSION = 'RELEASE'
CONSOLE = Console()
PYTHON_VERSION = sys.version.split()[0]
client = discord.Client()

# Functions
def loading(seconds):
    with Progress() as progress:
        task = progress.add_task("", total=seconds)
        while not progress.finished:
            progress.update(task, advance=1)
            time.sleep(1)

def clearall():
    os.system('clear' if platform.system() != "Windows" else 'cls')
    ascii_art = text2art("Discord Server Cloner")
    print(f"""{Style.BRIGHT}{Fore.RED}
{ascii_art}
{Style.RESET_ALL}{Fore.RESET}""")

os.system('title Discord Server Cloner')
clearall()

def get_user_preferences():
    preferences = {
        'guild_edit': True,
        'channels_delete': True,
        'roles_create': True,
        'categories_create': True,
        'channels_create': True,
        'emojis_create': False
    }

    def map_boolean_to_string(value):
        return "Yes" if value else "No"

    panel_title = "Config BETA"
    panel_content = "\n".join([
        f"- Change server name and icon: {map_boolean_to_string(preferences['guild_edit'])}",
        f"- Delete destination server channels: {map_boolean_to_string(preferences['channels_delete'])}",
        f"- Clone roles: {map_boolean_to_string(preferences['roles_create'])}",
        f"- Clone categories: {map_boolean_to_string(preferences['categories_create'])}",
        f"- Clone channels: {map_boolean_to_string(preferences['channels_create'])}",
        f"- Clone emojis: {map_boolean_to_string(preferences['emojis_create'])}"
    ])
    
    CONSOLE.print(
        RichPanel(panel_content, title=panel_title, style="bold blue", width=70)
    )

    questions = [
        inquirer.List(
            'reconfigure',
            message='Do you want to reconfigure the default settings?',
            choices=['Yes', 'No'],
            default='No')
    ]
    answers = inquirer.prompt(questions)

    if answers['reconfigure'] == 'Yes':
        questions = [
            inquirer.Confirm('guild_edit', message='Do you want to edit the server icon and name?', default=False),
            inquirer.Confirm('channels_delete', message='Do you want to delete the channels?', default=False),
            inquirer.Confirm('roles_create', message='Do you want to clone roles? (NOT RECOMMENDED TO DISABLE)', default=False),
            inquirer.Confirm('categories_create', message='Do you want to clone categories?', default=False),
            inquirer.Confirm('channels_create', message='Do you want to clone channels?', default=False),
            inquirer.Confirm('emojis_create', message='Do you want to clone emojis? (IT IS RECOMMENDED TO ENABLE THIS SOLO CLONING TO AVOID ERRORS)', default=False)
        ]
        answers = inquirer.prompt(questions)
        preferences.update(answers)

    clearall()
    return preferences

def restart():
    python = sys.executable
    os.execv(python, [python] + sys.argv)

async def main():
    clearall()
    while True:
        token = input(f'{Style.BRIGHT}{Fore.MAGENTA}Insert your token to proceed:{Style.RESET_ALL}{Fore.RESET}\n > ')
        guild_s = input(f'{Style.BRIGHT}{Fore.MAGENTA}Insert the ID of the server you want to replicate:{Style.RESET_ALL}{Fore.RESET}\n > ')
        guild = input(f'{Style.BRIGHT}{Fore.MAGENTA}Insert the ID of the destination server to paste the copied server:{Style.RESET_ALL}{Fore.RESET}\n > ')
        clearall()
        
        print(f'{Style.BRIGHT}{Fore.GREEN}The values you inserted are:')
        hidden_token = "*" * len(token)
        print(f'{Style.BRIGHT}{Fore.GREEN}Your token: {Fore.YELLOW}{hidden_token}{Style.RESET_ALL}{Fore.RESET}')
        print(f'{Style.BRIGHT}{Fore.GREEN}Server ID to replicate: {Fore.YELLOW}{guild_s}{Style.RESET_ALL}{Fore.RESET}')
        print(f'{Style.BRIGHT}{Fore.GREEN}Destination server ID to paste the copied server: {Fore.YELLOW}{guild}{Style.RESET_ALL}{Fore.RESET}')
        
        confirm = input(f'{Style.BRIGHT}{Fore.MAGENTA}Are the values correct? {Fore.YELLOW}(Y/N){Style.RESET_ALL}{Fore.RESET}\n > ')
        
        if confirm.upper() == 'Y':
            if not all([guild_s.isnumeric(), guild.isnumeric(), token.strip(), guild_s.strip(), guild.strip(), len(token.strip()) >= 3, len(guild_s.strip()) >= 3, len(guild.strip()) >= 3]):
                clearall()
                print(f'{Style.BRIGHT}{Fore.RED}Invalid input. Please ensure all fields are numeric and contain at least 3 characters.{Style.RESET_ALL}{Fore.RESET}')
                continue
            break
        else:
            clearall()
            print(f'{Style.BRIGHT}{Fore.RED}Invalid option. Please insert Y or N.{Style.RESET_ALL}{Fore.RESET}')
    
    input_guild_id = guild_s
    output_guild_id = guild

    @client.event
    async def on_ready():
        try:
            start_time = time.time()
            table = Table(title="Versions", style="bold magenta", width=85)
            table.add_column("Component", width=35)
            table.add_column("Version", style="cyan", width=35)
            table.add_row("Cloner", VERSION)
            table.add_row("Discord.py", discord.__version__)
            table.add_row("Python", PYTHON_VERSION)
            CONSOLE.print(RichPanel(table))
            CONSOLE.print(RichPanel(f" Successful authentication as {client.user.name}", style="bold green", width=69))
            print(f"\n")
            loading(5)
            clearall()
            
            guild_from = client.get_guild(int(input_guild_id))
            guild_to = client.get_guild(int(output_guild_id))
            preferences = get_user_preferences()

            if not any(preferences.values()):
                preferences = {k: True for k in preferences}

            if preferences['guild_edit']:
                await Clone.guild_edit(guild_to, guild_from)
            if preferences['channels_delete']:
                await Clone.channels_delete(guild_to)
            if preferences['roles_create']:
                await Clone.roles_create(guild_to, guild_from)
            if preferences['categories_create']:
                await Clone.categories_create(guild_to, guild_from)
            if preferences['channels_create']:
                await Clone.channels_create(guild_to, guild_from)
            if preferences['emojis_create']:
                await Clone.emojis_create(guild_to, guild_from)

            duration = time.time() - start_time
            duration_str = time.strftime("%M:%S", time.gmtime(duration))
            print(f"{Style.BRIGHT}{Fore.BLUE} The server was successfully cloned in {Fore.YELLOW}{duration_str}{Style.RESET_ALL}")
            print(f"{Style.BRIGHT}{Fore.BLUE}Ending process and logging out from {Fore.YELLOW}{client.user}")
            await asyncio.sleep(30)
            await client.close()

        except discord.LoginFailure:
            print("Unable to authenticate with the account. Check if the token is correct.")
        except discord.Forbidden:
            print("Cloning failed due to insufficient permissions.")
        except discord.NotFound:
            print("Unable to find one of the elements to be copied (channels, categories, etc.).")
        except discord.HTTPException:
            print("There was a communication error with the Discord API. The code will continue from where it left off in 20 seconds.")
            loading(20)
            await Clone.emojis_create(guild_to, guild_from)
        except asyncio.TimeoutError:
            print("An error occurred: TimeOut")
        except Exception as e:
            print(Fore.RED + "An error occurred:", e)
            print("\n")
            traceback.print_exc()
            panel_text = ("1. Incorrect server ID\n"
                          "2. You are not in the inserted server\n"
                          "3. Inserted server does not exist")
            CONSOLE.print(RichPanel(panel_text, title="Possible Causes and Solutions", style="bold red", width=70))
            print(Fore.YELLOW + "\nThe code will restart in 20 seconds. If you don't want to wait, refresh the page and start again.")
            print(Style.RESET_ALL)
            loading(20)
            restart()
            print(Fore.RED + "Restarting...")

    try:
        client.run(token)
    except discord.LoginFailure:
        print(Fore.RED + "The inserted token is invalid")
        print(Fore.YELLOW + "\n\nThe code will restart in 10 seconds. If you don't want to wait, refresh the page and start again.")
        print(Style.RESET_ALL)
        loading(10)
        restart()
        clearall()
        print(Fore.RED + "Restarting...")

if __name__ == "__main__":
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            asyncio.create_task(main())
        else:
            asyncio.run(main())
    except discord.LoginFailure:
        print(Fore.RED + "The inserted token is invalid")
        print(Fore.YELLOW + "\n\nThe code will restart in 10 seconds. If you don't want to wait, refresh the page and start again.")
        print(Style.RESET_ALL)
        loading(10)
        restart()
        clearall()
        print(Fore.RED + "Restarting...")
