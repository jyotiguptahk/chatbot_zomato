from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
import requests
import json


class ActionSearchRestaurants(Action):
    def name(self):
        return "action_search_restaurants"

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message(text="looking for restaurants")
        url = "https://developers.zomato.com/api/v2.1/search"
        api_key =  "bc4ef22aea16adde028738b5e2462087"
        params = {"entity_id": "61", "entity_type": "city", "q": tracker.get_slot("cuisine"), "count": "1", "sort": "rating", "order": "desc"}
        res = requests.post(url, params=params, headers={"user-key": api_key})
        zomato = json.loads(res.text)
        resto_name = zomato["restaurants"][0]["restaurant"]["name"]
        resto_lat = zomato["restaurants"][0]["restaurant"]["location"]["latitude"]
        resto_lon = zomato["restaurants"][0]["restaurant"]["location"]["longitude"]
        return [SlotSet("matches", resto_name),SlotSet("latitude", resto_lat),SlotSet("longitude", resto_lon)]


class ActionSuggest(Action):
    def name(self):
        return "action_suggest"

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message(text="here's what I found:")
        dispatcher.utter_message(text=tracker.get_slot("matches"))
        dispatcher.utter_message(text="https://maps.google.com/?q=" + str(tracker.get_slot("latitude")) + "," + str(tracker.get_slot("longitude")))
        return []
