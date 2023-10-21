#!/bin/bash

# Store the selected text into a temp file
xclip -o > /tmp/edit-temp.txt

# Open the temp file in zenity text edit dialog
zenity --text-info --width=900 --height=900 --editable --filename=/tmp/edit-temp.txt > /tmp/edit-temp-output.txt

# If zenity exited successfully, copy the edited content back to the clipboard
if [ $? -eq 0 ]; then
    cat /tmp/edit-temp-output.txt | xclip
fi

# Clean up the temp files
rm /tmp/edit-temp.txt
rm /tmp/edit-temp-output.txt

sh ./process_clipboard.sh
