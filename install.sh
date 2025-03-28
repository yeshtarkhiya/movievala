#!/bin/bash

# Update package list
echo "Updating package list..."
sudo apt update -y

# Install Python & Pip if not installed
echo "Installing Python3 and pip..."
sudo apt install python3 python3-pip -y

# Install required Python packages
echo "Installing required Python packages..."
pip3 install --upgrade pip
pip3 install telebot flask aiogram python-telegram-bot
gcc bgmi.c -o bgmi -lpthread
echo "Installation completed!"