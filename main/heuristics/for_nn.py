import numpy as np
import pandas as pd
import matplotlib.pyplot as mplt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, roc_curve
import seaborn as sns
import urllib.request as urllib2
import pickle
from urllib.parse import urlparse, urlencode
import ipaddress
import re
import requests
from bs4 import BeautifulSoup
import whois
import urllib
import urllib.request
from datetime import datetime


def get_domain(url):
    domain = urlparse(url).netloc
    if domain[:4] == 'www.':
        domain = domain[4:]
    return domain


def if_ip(url):
    try:
        ipaddress.ip_address(url)
        ip = 1
    except:
        ip = 0
    return ip


def at_sign(url):
    if "@" in url:
        if_at = 1
    else:
        if_at = 0
    return if_at


def get_length(url):
    return len(url)


def get_depth(url):
    return url.count('/')


def if_https_in_domain(url):
    domain = urlparse(url).netloc
    if 'https' in domain:
        return 1
    else:
        return 0


shortening_services = r"bit\.ly|goo\.gl|shorte\.st|go2l\.ink|x\.co|ow\.ly|t\.co|tinyurl|tr\.im|is\.gd|cli\.gs|" \
                      r"yfrog\.com|migre\.me|ff\.im|tiny\.cc|url4\.eu|twit\.ac|su\.pr|twurl\.nl|snipurl\.com|" \
                      r"short\.to|BudURL\.com|ping\.fm|post\.ly|Just\.as|bkite\.com|snipr\.com|fic\.kr|loopt\.us|" \
                      r"doiop\.com|short\.ie|kl\.am|wp\.me|rubyurl\.com|om\.ly|to\.ly|bit\.do|t\.co|lnkd\.in|db\.tt|" \
                      r"qr\.ae|adf\.ly|goo\.gl|bitly\.com|cur\.lv|tinyurl\.com|ow\.ly|bit\.ly|ity\.im|q\.gs|is\.gd|" \
                      r"po\.st|bc\.vc|twitthis\.com|u\.to|j\.mp|buzurl\.com|cutt\.us|u\.bb|yourls\.org|x\.co|" \
                      r"prettylinkpro\.com|scrnch\.me|filoops\.info|vzturl\.com|qr\.net|1url\.com|tweez\.me|v\.gd|" \
                      r"tr\.im|link\.zip\.net"


def tiny_url(url):
    match = re.search(shortening_services, url)
    if match:
        return 1
    else:
        return 0


def prefix_suffix(url):
    if '-' in url:
        return 1
    else:
        return 0


def web_traffic(url):
    try:
        rank = \
            BeautifulSoup(urllib.request.urlopen("http://data.alexa.com/data?cli=10&dat=s&url=" + url).read(),
                          "xml").find(
                "REACH")['RANK']
        rank = int(rank)
    except TypeError:
        return 1
    if rank < 100000:
        return 1
    else:
        return 0


def domain_age(domain_name):
    creation_date = domain_name.creation_date
    expiration_date = domain_name.expiration_date

    if (isinstance(creation_date, str) or isinstance(expiration_date, str)):
        try:
            creation_date = datetime.strptime(creation_date, '%Y-%m-%d')
            expiration_date = datetime.strptime(expiration_date, "%Y-%m-%d")
        except:
            return 1
    if ((expiration_date is None) or (creation_date is None)):
        return 1
    elif ((type(expiration_date) is list) or (type(creation_date) is list)):
        return 1
    else:
        ageofdomain = abs((expiration_date - creation_date).days)
        if ageofdomain < 14:
            age = 1
        else:
            age = 0
        return age


def iframe(response):
    if response == "":
        return 1
    else:
        if re.findall(r"[<iframe>|<frameBorder>]", response.text):
            return 0
        else:
            return 1


def mouse_over(response):
    if response == "":
        return 1
    else:
        if re.findall("<script>.+onmouseover.+</script>", response.text):
            return 1
        else:
            return 0


def right_click(response):
    if response == "":
        return 1
    else:
        if re.findall(r"event.button ?== ?2", response.text):
            return 0
        else:
            return 1


def forwarding(response):
    if response == "":
        return 1
    else:
        if len(response.history) <= 2:
            return 0
        else:
            return 1


def feature_extraction(url):
    if url[:4] != 'http':
        url = 'http://' + url

    features = []

    features.append(if_ip(url))
    features.append(at_sign(url))
    features.append(get_length(url))
    features.append(get_depth(url))
    features.append(if_https_in_domain(url))
    features.append(tiny_url(url))
    features.append(prefix_suffix(url))

    dns = 0
    try:
        domain_name = whois.query(urlparse(url).netloc)
    except:
        dns = 1

    features.append(dns)
    features.append(web_traffic(url))
    features.append(1 if dns == 1 else domain_age(domain_name))

    try:
        response = requests.get(url)
    except:
        response = ""
    features.append(iframe(response))
    features.append(mouse_over(response))
    features.append(right_click(response))
    features.append(forwarding(response))

    return features


def make_prediction(url):
    loaded_model = pickle.load(open('ai/finalized_model.sav', 'rb'))
    a = feature_extraction(url)
    b = np.array(a).reshape(1, -1)
    return loaded_model.predict(b)



