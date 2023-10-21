# Linux-AI-Assistant-scripts
These are my custom scripts used to interact with Whisper / OpenAI through keyboard shortcuts and voice input.

I am using ArchLinux and the xfce Keyboard settings for key bindings.

## Listen to me
`voice.sh` bound to `F2` - activates voice recording. Once stopped by the other script, it sends a `wav` file to `whisper.cpp`.

`stop_voice.py` bound to `F4` - stops voice recording (uses Linux pipe).

`voice_tr.sh` bound to `F3` - same voice recording, but with a more capable model. Used for translations.

This is how it works for me: 
![voice](https://github.com/samoylenkodmitry/Linux-AI-Assistant-scripts/assets/2128250/92d269e3-fd73-4c28-9370-0097bc0a9673)

## Answer to me

`process_clipboard.sh` bound to `F1` - sends the currently selected text to the ChatGPT [aichat project](https://github.com/sigoden/aichat).

This is how it works:
![selected_text](https://github.com/samoylenkodmitry/Linux-AI-Assistant-scripts/assets/2128250/620b34ff-3439-4348-90d4-422c9d237523)

`notify_history.sh` is used to read the notification history. It is bound to a shortcut in the system tray.

## You will need to install

`aichat` - as mentioned previously

`dunst`, `zenity` - for notifications 

[whisper.cpp](https://github.com/ggerganov/whisper.cpp) - for voice transcribing
