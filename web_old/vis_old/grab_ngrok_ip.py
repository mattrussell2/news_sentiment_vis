#thanks!! https://stackoverflow.com/questions/34322988/view-random-ngrok-url-when-run-in-background

import json
import requests
import sys
url = "http://localhost:4040/api/tunnels"
res = requests.get(url)
res_unicode = res.content.decode("utf-8")
res_json = json.loads(res_unicode)
ip = res_json["tunnels"][0]["public_url"]

if ip[4] != 's':
    ip = 'https://' + ip.split('://')[1]
    
f = open('js/env.js','w')
f.write("env = {\n ngrok_ip: '" + ip + "'\n}")
f.close()
