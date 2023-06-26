import os
import time

def team_url(org, team_name):
    return f'https://linear.app/{org}/team/{team_name}'

def open_linear_url(url):
    print("Opening " + url)
    time.sleep(1)
    os.system(f'open "{url}" -a Linear.app')
