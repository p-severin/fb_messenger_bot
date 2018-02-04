import json
import requests
from pprint import pprint

ACCESS_TOKEN = 'EAALEpv2h7VsBACmGcnLGmg2mu5ZBy5PnA7434uYgzfBc6coYS62YYv3PVyhuVvA2WP9H1C4KEiccXrnywvnZCQqVq3ojRH5cexi49JY8ZCQdUykKfd5UdV4rUZArRvnZBwf6GLKqZCietkUs1rnb2g8BhKfIDcjTRNOvbbzMWju57mVjmpSNVZC'


def post_facebook_message(fbid, received_message):
    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=' + ACCESS_TOKEN
    response_msg = json.dumps({"recipient": {"id": fbid}, "message": {"text": received_message}})
    status = requests.post(post_message_url, headers={'Content-Type': 'application/json'}, data=response_msg)
    pprint(status.json())


