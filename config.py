#!/usr/bin/env python3

import configparser
import os
from typing import Dict

def load_config(config_path='config.ini') -> Dict[str, str]:
    
    if not os.path.exists(config_path):
        raise FileNotFoundError(
            f"Config file not found: {config_path}\n"
            f"Please copy config.ini.example to config.ini and add your Reddit API credentials"
        )
    
    config = configparser.ConfigParser()
    config.read(config_path)
    
    required_fields = ['client_id', 'client_secret', 'user_agent']
    
    if 'reddit' not in config:
        raise ValueError("Missing [reddit] section in config file")
    
    reddit_config = config['reddit']
    
    for field in required_fields:
        if field not in reddit_config or not reddit_config[field].strip():
            raise ValueError(f"Missing or empty required field: {field}")
        
        if reddit_config[field].strip() in ['YOUR_CLIENT_ID', 'YOUR_CLIENT_SECRET', 'YOUR_USER_AGENT']:
            raise ValueError(
                f"Please replace placeholder value for {field} in config.ini\n"
                f"See API_SETUP.md for instructions on obtaining Reddit API credentials"
            )
    
    return {
        'client_id': reddit_config['client_id'].strip(),
        'client_secret': reddit_config['client_secret'].strip(),
        'user_agent': reddit_config['user_agent'].strip()
    }
