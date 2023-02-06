#!/bin/bash
sudo systemctl daemon-reload
sudo systemctl restart discord-bot-eft-v2.service
sudo systemctl status discord-bot-eft-v2.service