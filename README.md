# Discord Server Cloner

Discord Server Cloner is a powerful script designed to help you clone an entire Discord server, including roles, channels, categories, and more. It uses the Discord.py library to interact with the Discord API and perform the cloning operations.

## Features

- **Clone Server Details**: Edit server name and icon.
- **Clone Roles**: Copy all roles from the source server to the destination server.
- **Clone Channels**: Copy all channels and their settings.
- **Clone Categories**: Copy all categories and their settings.
- **Clone Emojis**: Copy all custom emojis.
- **Delete Channels**: Optionally delete channels in the destination server before cloning.

## Requirements

- Python 3.9+

## Usage

1. **Clone the Repository**

   ```bash
   git clone https://github.com/juniarikiwm6lo/discord-server-cloner.git
   cd discord-server-cloner
   ```

2. **Run the `start.bat`**

3. **Follow the Prompts**

   - Insert your Discord bot token.
   - Provide the ID of the server you want to replicate.
   - Provide the ID of the destination server where you want to paste the copied server.

4. **Configure Cloning Preferences**

   You will be prompted to confirm or reconfigure default settings such as:
   - Changing server name and icon
   - Deleting destination server channels
   - Cloning roles
   - Cloning categories
   - Cloning channels
   - Cloning emojis

## Error Handling

The script includes error handling for common issues such as:

- Invalid token or insufficient permissions.
- Element not found (channels, categories, etc.).
- Communication errors with the Discord API.
- Timeouts and other unexpected errors.

If an error occurs, the script will provide possible causes and solutions, and automatically attempt to restart the cloning process.

## Disclaimer

This tool is intended for educational purposes. Please ensure you comply with Discord's Terms of Service and community guidelines while using this tool.
