from config import PAGE_ACCESS_TOKEN, VERIFY_TOKEN

from flask import Flask, request
import json
import requests
import pokebase as pb
import random

app = Flask(__name__)

display_pokemon = None
quick_replies_list = None


@app.route('/', methods=['GET'])
def handle_verification():
    """ If the endpoint is registered correctly as a webhook,
        it must echo back the `hub.challenge` value it receives
        in the query arguments.
    """
    print("Handling verification")
    if request.args.get('hub.verify_token') == VERIFY_TOKEN:
        print("Verification successful!")
        return request.args['hub.challenge']
    else:
        print("Verification failed")
        return 'Error, wrong validation token'


@app.route('/', methods=['POST'])
def webhook():
    """ Endpoint for processing incoming messaging events. """
    print("Handling messages")
    payload = request.get_data()
    for sender, message in messaging_events(payload):
        print("Incoming from {}: {}".format(sender, message))
        send_message(sender, message)
    return "Ok"


def messaging_events(payload):
    """ Generate tuples of (sender_id, message_text) from the
        provided payload.
    """
    data = json.loads(payload)
    messaging_events = data["entry"][0]["messaging"]
    for event in messaging_events:
        if "message" in event and "text" in event["message"]:
            yield event["sender"]["id"], event["message"]["text"]
        else:
            yield event["sender"]["id"], "I can't echo this"


def generate_questions():
    with open('pokemon.txt') as f:
        pokemons = [p.strip('\n') for p in f.readlines()]

    randomized_pokemons = random.sample(pokemons, 4)

    quick_replies_list = [
        {
            "content_type": "text",
            "title": pokemon,
            "payload": pokemon
        } for pokemon in randomized_pokemons
    ]

    display_pokemon = random.choice(randomized_pokemons)
    return display_pokemon, quick_replies_list


def send_message(recipient, text):
    """Send the message text to recipient with id recipient."""
    global display_pokemon, quick_replies_list
    params = {"access_token": PAGE_ACCESS_TOKEN}
    headers = {"Content-Type": "application/json"}

    if display_pokemon is not None:
        print("Inside here")
        print("Display pokemon: {}".format(display_pokemon))
        if display_pokemon != text:
            data = json.dumps({
                "recipient": {"id": recipient},
                "message": {"text": "That's wrong. Please try again",
                            "quick_replies": quick_replies_list}
                })
            r = requests.post("https://graph.facebook.com/v2.6/me/messages",
                              params=params, headers=headers, data=data)
            return
        data = json.dumps({
                "recipient": {"id": recipient},
                "message": {"text": "That's right! Onto the next question!"},
                })
        r = requests.post("https://graph.facebook.com/v2.6/me/messages",
                          params=params, headers=headers, data=data)

    display_pokemon, quick_replies_list = generate_questions()
    pokemon = pb.pokemon(display_pokemon)

    data = json.dumps({
    "recipient": {"id": recipient},
    "message": {"attachment": {
        "type": "image",
        "payload": {
            "url": pokemon.sprites.front_default
        }},
        "quick_replies": quick_replies_list}
    })

    r = requests.post("https://graph.facebook.com/v2.6/me/messages",
                      params=params, headers=headers, data=data)

    if r.status_code != requests.codes.ok:
        print(r.text)


if __name__ == '__main__':
    app.run()
