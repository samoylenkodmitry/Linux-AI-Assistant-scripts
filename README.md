# Linux-AI-Assistant-scripts
This is my custom scripts to use Whisper / OpenAI by keyboard shortcuts and voice input.

I am using ArchLinux, xfce Keyboard setting to do the binding.

## Listen to me
`voice.sh` to `F2` - activates the voice recording. After it is stopped by the other script, it sends a `wav` file to the `whisper.cpp`

`stop_voice.py` to `F4` - stops the voice recording (by using Linux pipe)

`voice_tr.sh` to `F3` - same voice recording, but with more capabale model. I use it for translations.

This is how it works for me: 
![voice](https://github.com/samoylenkodmitry/Linux-AI-Assistant-scripts/assets/2128250/92d269e3-fd73-4c28-9370-0097bc0a9673)

## Answer to me

`process_clipboard.sh` to `F1` - sends the current selected text to ChatGPT [aichat project](https://github.com/sigoden/aichat)

This is how it works:
![selected_text](https://github.com/samoylenkodmitry/Linux-AI-Assistant-scripts/assets/2128250/620b34ff-3439-4348-90d4-422c9d237523)

`notify_history.sh` this is just for reading the notification history, because all the output got here. I bind it to shortcut in a tray.

## You will need to install

`aichat` - as said before

`dunst`, `zenity` - for notifications 

[whisper.cpp](https://github.com/ggerganov/whisper.cpp) - for voice transcribing
