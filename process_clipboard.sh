#!/bin/bash
# Get the ID of the window that currently has focus
focused_window_id=$(xdotool getwindowfocus)

# Get the window name of the focused window
window_name=$(xprop -id $focused_window_id | grep -E 'WM_NAME\(' | cut -d '=' -f 2- | tr -d ' "')

echo "--------------------------------------------"
echo "Window name: $window_name"

clipboard_content=$(xclip -o -selection 2>/dev/null)
notify-send -u low -t 20000 "asking aichat... $clipboard_content"
aichat_output=$(aichat "You are ArchLinux OS assistant. Window in focus (maybe not relevant to the task): $window_name. Help me with this: $clipboard_content")
echo "result:"
echo "$aichat_output"

# concat input and output and copy to clipboard:
# echo "$clipboard_content" > /tmp/clipboard_content
# echo "$aichat_output" > /tmp/aichat_output
# cat /tmp/clipboard_content /tmp/aichat_output | xclip -selection clipboard


# Show a notification with the aichat output
notify-send -u low -t 20000 "aichat output" "$aichat_output"
