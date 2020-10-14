import time, threading, requests, os
from flask import Flask, jsonify, request
from bs4 import BeautifulSoup
from rcp import RichPressence
from dotenv import load_dotenv

# GET ENV VARS
load_dotenv()
CLIENT_ID = os.getenv('CLIENT_ID')
L_IMG = os.getenv('L_IMG')


curr_time = time.time()

app = Flask(__name__)
prev_url = ""

# RCP
rcp = RichPressence(CLIENT_ID)


# strips the url and returns a list of [url, params]
def url_strip(url):
    try:
        url = url.split("/")[2:]
        return url[0], url[1:]
    except Exception as e:
        print(e)
        return None, None


def set_netflix_presence(url):
    # extracct the url content 
    soup = BeautifulSoup(requests.get(url).content, "html.parser")
    title = soup.find('title').string.split("|")[0] # get the title 

    rcp.set_presence(state=title, large_image=L_IMG, detail="Streaming ", limit=30) # set presence


@app.route('/send_url', methods=['POST'])
def send_url():
    global prev_url

    response = request.get_data().decode()
    url = response.replace("url=", "")
    site, params = url_strip(url)

    print("CURRENT TAB: " + site)
    if prev_url: print("PREV TAB: ", prev_url)
    prev_url = site

    # check if the visited site is netflix, if yes then set presence
    if "netflix.com" in site and "watch" == params[0]:
        set_netflix_presence(url)

    return jsonify({'message': 'success!'}), 200


@app.route('/quit_url', methods=['POST'])
def quit_url():
    response = request.get_data().decode()
    url = response.replace("url=", "")
    site, _ = url_strip(url)
    if site:
        if "netflix.com" in site:
            rcp.quit()

    return jsonify({'message': 'quit success!'}), 200


app.run(host='0.0.0.0', port=5000)
