#!/bin/bash 
#> ./Responses/test.md

if [ -z $1 ]; then
/usr/local/bin/python3 /workspaces/python-openai-demos/chat_stream.py 
else 
/usr/local/bin/python3 /workspaces/python-openai-demos/chat.py 
fi