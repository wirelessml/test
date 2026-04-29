#!/usr/bin/env python3
"""Generic Gmail SMTP sender for monitoring scripts.

Reads credentials from ~/.config/masu-p-watch/email.json:
{
  "from_addr": "wirelessml@gmail.com",
  "to_addr": "wirelessml@gmail.com",
  "app_password": "xxxx xxxx xxxx xxxx"
}

Usage:
  send-email.py --subject "..." --body-file /path/to/body.txt
  echo "body" | send-email.py --subject "..."
"""
import argparse
import json
import os
import smtplib
import ssl
import sys
from email.message import EmailMessage
from pathlib import Path


CONFIG_PATH = Path.home() / ".config" / "masu-p-watch" / "email.json"


def load_config():
    if not CONFIG_PATH.exists():
        sys.stderr.write(
            f"[send-email] config not found: {CONFIG_PATH}\n"
            "  Create it with the following structure:\n"
            "  {\n"
            '    "from_addr": "wirelessml@gmail.com",\n'
            '    "to_addr": "wirelessml@gmail.com",\n'
            '    "app_password": "Gmail App Password (16 chars)"\n'
            "  }\n"
        )
        sys.exit(2)
    with open(CONFIG_PATH) as f:
        return json.load(f)


def send(subject: str, body: str, config: dict) -> None:
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = config["from_addr"]
    msg["To"] = config["to_addr"]
    msg.set_content(body)

    ctx = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=ctx) as smtp:
        smtp.login(config["from_addr"], config["app_password"].replace(" ", ""))
        smtp.send_message(msg)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--subject", required=True)
    parser.add_argument("--body-file", help="Path to body text file. If omitted, reads stdin.")
    args = parser.parse_args()

    if args.body_file:
        with open(args.body_file) as f:
            body = f.read()
    else:
        body = sys.stdin.read()

    config = load_config()
    try:
        send(args.subject, body, config)
        print(f"[send-email] sent: {args.subject}")
    except Exception as e:
        sys.stderr.write(f"[send-email] FAIL: {e}\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
