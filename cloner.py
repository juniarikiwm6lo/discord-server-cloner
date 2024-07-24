# Imports
import asyncio
import random

import discord
import requests
from colorama import Fore, init, Style

# Initialize Colorama
init(autoreset=True)

# Cloner Class
class Clone:
    @staticmethod
    async def roles_delete(guild_to: discord.Guild):
        for role in guild_to.roles:
            if role.name == "@everyone":
                continue
            try:
                await role.delete()
                print_delete(f"{Fore.YELLOW}{role.name}{Fore.BLUE} has been deleted")
                await asyncio.sleep(random.uniform(0.10, 0.15))
            except discord.Forbidden:
                print_error(f"Error when deleting role: {Fore.YELLOW}{role.name}{Fore.RESET}")
            except discord.HTTPException as e:
                if e.status == 429:
                    print_warning(f"Many requests were made. Waiting 60 seconds. Details: {e}")
                    await asyncio.sleep(60)

    @staticmethod
    async def roles_create(guild_to: discord.Guild, guild_from: discord.Guild):
        roles = [role for role in guild_from.roles if role.name != "@everyone"][::-1]
        for role in roles:
            try:
                await guild_to.create_role(
                    name=role.name,
                    permissions=role.permissions,
                    colour=role.colour,
                    hoist=role.hoist,
                    mentionable=role.mentionable
                )
                print_add(f"{Fore.YELLOW}{role.name}{Fore.BLUE} has been created")
                await asyncio.sleep(random.uniform(0.3, 0.6))
            except discord.Forbidden:
                print_error(f"Error when creating role: {Fore.YELLOW}{role.name}{Fore.RESET}")
                await asyncio.sleep(random.uniform(0.20, 0.40))
            except discord.HTTPException as e:
                if e.status == 429:
                    print_warning(f"Many requests were made. Waiting 60 seconds. Details: {e}")
                    await asyncio.sleep(60)

    @staticmethod
    async def channels_delete(guild_to: discord.Guild):
        for channel in guild_to.channels:
            try:
                await channel.delete()
                print_delete(f"{Fore.YELLOW}{channel.name}{Fore.BLUE} has been deleted")
                await asyncio.sleep(0.6)
            except discord.Forbidden:
                print_error(f"Error when deleting channel: {Fore.YELLOW}{channel.name}{Fore.RESET}")
                await asyncio.sleep(random.uniform(2, 3))
            except discord.HTTPException as e:
                if e.status == 429:
                    print_warning(f"Many requests were made. Waiting 60 seconds. Details: {e}")
                    await asyncio.sleep(60)
            except Exception as e:
                print_error(f"Error when deleting channel: {Fore.YELLOW}{channel.name}{Fore.RESET}. Details: {e}")
                await asyncio.sleep(random.uniform(9, 12))

    @staticmethod
    async def categories_create(guild_to: discord.Guild, guild_from: discord.Guild):
        for channel in guild_from.categories:
            try:
                overwrites_to = {discord.utils.get(guild_to.roles, name=key.name): value for key, value in channel.overwrites.items()}
                new_channel = await guild_to.create_category(name=channel.name, overwrites=overwrites_to)
                await new_channel.edit(position=channel.position)
                print_add(f"The category {Fore.YELLOW}{channel.name}{Fore.BLUE} has been created")
                await asyncio.sleep(random.uniform(1, 3))
            except discord.Forbidden:
                print_error(f"Error creating category: {Fore.YELLOW}{channel.name}{Fore.RESET}")
                await asyncio.sleep(random.uniform(2, 3))
            except discord.HTTPException as e:
                if e.status == 429:
                    print_warning(f"Many requests were made. Waiting 60 seconds. Details: {e}")
                    await asyncio.sleep(60)
            except Exception as e:
                print_error(f"Unable to create category {Fore.YELLOW}{channel.name}{Fore.RESET}. Details: {e}")
                await asyncio.sleep(random.uniform(9, 12))

    @staticmethod
    async def channels_create(guild_to: discord.Guild, guild_from: discord.Guild):
        for channel_text in guild_from.text_channels:
            try:
                category = next((cat for cat in guild_to.categories if cat.name == channel_text.category.name), None)
                overwrites_to = {discord.utils.get(guild_to.roles, name=key.name): value for key, value in channel_text.overwrites.items()}
                new_channel = await guild_to.create_text_channel(
                    name=channel_text.name,
                    overwrites=overwrites_to,
                    position=channel_text.position,
                    topic=channel_text.topic,
                    slowmode_delay=channel_text.slowmode_delay,
                    nsfw=channel_text.nsfw
                )
                if category:
                    await new_channel.edit(category=category)
                print_add(f"The text channel {Fore.YELLOW}{channel_text.name}{Fore.BLUE} has been created")
                await asyncio.sleep(0.59)
            except discord.Forbidden:
                print_error(f"Error creating text channel: {channel_text.name}")
                await asyncio.sleep(random.uniform(8, 10))
            except discord.HTTPException as e:
                if e.status == 429:
                    print_warning(f"Many requests were made. Waiting 60 seconds. Details: {e}")
                    await asyncio.sleep(60)
                    new_channel = await guild_to.create_text_channel(
                        name=channel_text.name,
                        overwrites=overwrites_to,
                        position=channel_text.position
                    )
                    if category:
                        await new_channel.edit(category=category)
                    print_add(f"The channel {Fore.YELLOW}{channel_text.name}{Fore.BLUE} has been created")
            except Exception as e:
                print_error(f"Error creating text channel: {channel_text.name}. Details: {e}")
                await asyncio.sleep(random.uniform(9, 12))

        for channel_voice in guild_from.voice_channels:
            try:
                category = next((cat for cat in guild_to.categories if cat.name == channel_voice.category.name), None)
                overwrites_to = {discord.utils.get(guild_to.roles, name=key.name): value for key, value in channel_voice.overwrites.items()}
                new_channel = await guild_to.create_voice_channel(
                    name=channel_voice.name,
                    overwrites=overwrites_to,
                    position=channel_voice.position,
                    bitrate=channel_voice.bitrate,
                    user_limit=channel_voice.user_limit
                )
                if category:
                    await new_channel.edit(category=category)
                print_add(f"The voice channel {Fore.YELLOW}{channel_voice.name}{Fore.BLUE} has been created")
                await asyncio.sleep(0.48)
            except discord.Forbidden:
                print_error(f"Error creating voice channel: {channel_voice.name}")
                await asyncio.sleep(random.uniform(6, 7))
            except discord.HTTPException as e:
                if e.status == 429:
                    print_warning(f"Many requests were made. Waiting 60 seconds. Details: {e}")
                    await asyncio.sleep(60)
                    new_channel = await guild_to.create_voice_channel(
                        name=channel_voice.name,
                        overwrites=overwrites_to,
                        position=channel_voice.position
                    )
                    if category:
                        await new_channel.edit(category=category)
                    print_add(f"The voice channel {Fore.YELLOW}{channel_voice.name}{Fore.BLUE} has been created")
            except Exception as e:
                print_error(f"Error creating voice channel: {channel_voice.name}. Details: {e}")

    @staticmethod
    async def emojis_create(guild_to: discord.Guild, guild_from: discord.Guild):
        emojis = guild_from.emojis
        if not emojis:
            print_warning("No emojis found.")
            return
        for emoji in emojis:
            try:
                existing_emoji = discord.utils.get(guild_to.emojis, name=emoji.name)
                if existing_emoji:
                    print_add(f"Emoji with the name {Fore.YELLOW}{emoji.name}{Fore.BLUE} already exists.")
                else:
                    response = requests.get(str(emoji.url))
                    emoji_image = response.content
                    await guild_to.create_custom_emoji(name=emoji.name, image=emoji_image)
                    print_add(f"The emoji {Fore.YELLOW}{emoji.name}{Fore.BLUE} has been created.")
                    await asyncio.sleep(1)
            except discord.Forbidden:
                print_error(f"Error creating emoji: {Fore.YELLOW}{emoji.name}{Fore.RED} Insufficient permissions.{Fore.RESET}")
                await asyncio.sleep(random.uniform(2, 3))
            except discord.HTTPException as e:
                if e.status == 429:
                    print_warning(f"Many requests were made. Waiting 10 seconds. Details: {e}")
                    await asyncio.sleep(10)
                    await guild_to.create_custom_emoji(name=emoji.name, image=emoji_image)
            except Exception as e:
                print_warning(f"An error occurred with {emoji.name}. Details: {e}")
            except asyncio.TimeoutError:
                print_error(f"An error occurred with {emoji.name} due to timeout.")

    @staticmethod
    async def guild_edit(guild_to: discord.Guild, guild_from: discord.Guild):
        try:
            icon_content = None
            try:
                icon_content = requests.get(guild_from.icon_url).content
            except requests.exceptions.RequestException:
                print_error(f"Unable to download icon for {guild_from.name}")
            await guild_to.edit(name=guild_from.name)
            if icon_content:
                try:
                    await guild_to.edit(icon=icon_content)
                    print_add(f"Changed group icon: {guild_to.name}")
                except Exception as e:
                    print_error(f"Error changing group icon: {guild_to.name}. Details: {e}")
        except discord.LoginFailure:
            print("Unable to authenticate to account. Verify that the token is correct.")
        except discord.Forbidden:
            print_error(f"Error changing group icon: {guild_to.name}")

# Helper Functions
def print_add(message):
    print(f'{Style.BRIGHT}{Fore.CYAN} {message}{Fore.RESET}')

def print_delete(message):
    print(f'{Style.BRIGHT}{Fore.CYAN} {message}{Fore.RESET}')

def print_warning(message):
    print(f'{Style.BRIGHT}{Fore.YELLOW} {message}{Fore.RESET}')

def print_error(message):
    print(f'{Style.BRIGHT}{Fore.RED} {message}{Fore.RESET}')
