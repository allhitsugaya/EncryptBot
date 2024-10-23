# Encryption and Decryption Telegram Bot

This is a Telegram bot that provides encryption and decryption of messages using the `pynacl` library. It allows users to encrypt their text messages and decrypt them back in a secure and straightforward way, using symmetric key cryptography. The bot is built with the `aiogram` framework for handling interactions with Telegram API.

## Features

- **Encrypt messages**: Securely encrypts a text message using the `SecretBox` from `pynacl`.
- **Decrypt messages**: Decrypts the encrypted message back to plain text.
- **User-friendly interface**: Interactive buttons for quick access to commands like support and command list.
- **Command-based interactions**: Simple commands for starting, encrypting, decrypting, and retrieving information about the bot.

## Libraries Used

- **aiogram** (`v2.25`) — Python asynchronous framework for building Telegram bots.
- **pynacl** (`v1.5.0`) — Python binding to the Networking and Cryptography library (NaCl) for secure encryption and decryption of messages.
- **pycparser** (`v2.21`) — Required for `pynacl` installation.

## Installation and Setup

To run this bot, you need to install the required dependencies and set up your Telegram bot token.

### Prerequisites

- Python 3.7 or higher
- Telegram bot token (you can get it by creating a bot through [BotFather](https://core.telegram.org/bots#botfather))

### Step-by-Step Guide

1. Clone the repository or download the project files:
   ```bash
   git clone https://github.com/yourusername/telegram-encryption-bot.git
   cd telegram-encryption-bot
