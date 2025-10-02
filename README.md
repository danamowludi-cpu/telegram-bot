# Telegram Bot Deployment Guide

## Deploy to Railway (Free - Recommended)

1. **Create Railway Account**: Go to [railway.app](https://railway.app) and sign up
2. **Deploy from GitHub**:
   - Push your code to GitHub
   - Connect Railway to your GitHub repo
   - Railway will auto-deploy

3. **Set Environment Variables**:
   - In Railway dashboard, go to Variables
   - Add: `TELEGRAM_BOT_TOKEN` = your bot token
   - Save and redeploy

## Deploy to Render (Free Alternative)

1. **Create Render Account**: Go to [render.com](https://render.com)
2. **Create Web Service**:
   - Connect your GitHub repo
   - Choose "Background Worker" (not Web Service)
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python "bott (2).py"`

3. **Set Environment Variables**:
   - Add `TELEGRAM_BOT_TOKEN` in Environment section

## Deploy to VPS (Paid but Full Control)

1. **Get a VPS** (DigitalOcean, Vultr, etc.)
2. **Install Python and dependencies**:
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip
   pip3 install -r requirements.txt
   ```

3. **Run with systemd** (keeps running after reboot):
   ```bash
   sudo nano /etc/systemd/system/telegram-bot.service
   ```
   
   Add:
   ```ini
   [Unit]
   Description=Telegram Bot
   After=network.target

   [Service]
   Type=simple
   User=ubuntu
   WorkingDirectory=/home/ubuntu/bot
   Environment=TELEGRAM_BOT_TOKEN=your_token_here
   ExecStart=/usr/bin/python3 "bott (2).py"
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```

   Enable and start:
   ```bash
   sudo systemctl enable telegram-bot
   sudo systemctl start telegram-bot
   ```

## Files Needed for Deployment

- `bott (2).py` - Your bot code
- `requirements.txt` - Python dependencies
- `Procfile` - For Railway/Heroku
- `bot_data.xlsx` - Will be created automatically
- `imghdr.py` - Python 3.13 compatibility

## Environment Variables

- `TELEGRAM_BOT_TOKEN` - Your bot's API token (keep secret!)

## Notes

- Railway gives 500 hours/month free (enough for 24/7 if you verify with GitHub Student or credit card)
- Render has some limitations on free tier
- VPS gives full control but requires more setup
- Your Excel file will be created automatically on first run
