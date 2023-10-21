#!/bin/bash
dunstctl history | jq -r '.data[][] | "\(.message.data)\n"' | zenity --text-info --editable --title="Dunst Notification History" --width=900 --height=900
