# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"
from typing import Any, Text, Dict, List
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

#
client = MongoClient("mongodb+srv://laro-31:laro-31@courselist.i0n97yv.mongodb.net/?retryWrites=true&w=majority")
db = client["courselist"]
collection = db["courselist"]


class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "action_hello_world"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        institute = tracker.get_slot('institute')
        dispatcher.utter_message(text='The features you entered: ' + str(institute))
        dispatcher.utter_message(text="Hello World!")

        return []


class ActionZScore(Action):

    def name(self) -> Text:
        return "action_zscore"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text="Zscore is 1.567")

        return []


class ActionCourse(Action):

    def name(self):
        return "action_course"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Retrieve data from MongoDB
        course = tracker.get_slot("course")
        dispatcher.utter_message(course)
        print("Identified slot is" + course)
        # course = tracker.latest_message.get("text")
        data = collection.find_one({"course": course})
        # Do something with the data
        if data:
            # Send a response message to the user
            dispatcher.utter_message(text="Here is some data from MongoDB: {}".format(data))
        else:
            # Send an error message if no data is found
            dispatcher.utter_message(text="Sorry, no data found in MongoDB.")
        return []


class QueryZscoreAction(Action):
    def name(self) -> Text:
        return "action_query_zscore_form"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Get the values of the slots
        institute = tracker.get_slot("institute")
        district = tracker.get_slot("district")
        course = tracker.get_slot("course")
        year = tracker.get_slot("year")

        # Connect to the MongoDB database
        try:
            # client = MongoClient("mongodb://localhost:27017/")
            # db = client["courselist"]
            zscore_collection = db["zscore_list"]
        except ConnectionFailure:
            dispatcher.utter_message(text="Could not connect to the database.")
            return []

        # Query the z-score from the database
        query = {"institute": institute, "district": district, "course": course, "year": year}
        result = zscore_collection.find_one(query)
        if result is None:
            dispatcher.utter_message(text="No z-score found for the given criteria.")
        else:
            zscore = result["zscore"]
            dispatcher.utter_message(text=f"The z-score is {zscore}.")

        return []


class ActionDefaultFallback(Action):
    def name(self) -> Text:
        return "action_default_fallback"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message("I'm sorry, but I didn't understand. Can you please rephrase your request?")

        return []
