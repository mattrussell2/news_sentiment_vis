#!/bin/bash

#setup flask
xterm -e python webpage.py &

#setup ngrok
xterm -e ./ngrok http 5000 &

#sleep so the ngrok ip can be nabbed
sleep 2

#nab the ngrok ip
python grab_ngrok_ip.py

#update the ngrok ip on the server
rsync -av js/env.js mrussell@homework.cs.tufts.edu:~/public_html/vis/js/
rsync -av vis.html mrussell@homework.cs.tufts.edu:~/public_html/vis/
