# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"
import logging
from random import random
from typing import Any, Text, Dict, List
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import os
import requests
import openai

#
client = MongoClient("secret_key")
db = client["courselist"]
collection = db["courselist"]

logger = logging.getLogger(__name__)


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


path = os.getcwd()

url = "https://api.openai.com/v1/completions"

key = "secret_key"

headers = {"Authorization": f"Bearer {key}"}


class ActionApiClass(Action):
    def name(self):
        return "action_call_openai"

    def run(self, dispatcher, tracker, domain):
        # dispatcher.utter_message(text= "message you want to display" )
        context = tracker.latest_message['text']
        model = 'text-davinci-003'
        prompt = "assume you are sri lankan ugc based inquiry chatbot that gives answers only in sri lankan higher " \
                 "education domain considering this answer the question follows : " + context
        data = {'model': model, 'prompt': prompt, 'temperature': 0, 'max_tokens': 256, 'stop': [" Human:", " AI:"]}
        if context:
            response = requests.post(url, headers=headers, json=data, verify=False)
            logger.info(response)
            msg = response.json()['choices'][0]['text']
        else:
            dispatcher.utter_message('pls retry asking question')
        dispatcher.utter_message(text=str(msg))
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


class ActionSuggestCourse(Action):
    def name(self) -> Text:
        return "action_suggest_course"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # In this example, we'll provide a static list of course suggestions.
        course_suggestions = [
            "Introduction to Data Science",
            "Web Development Fundamentals",
            "Machine Learning Basics",
            "Digital Marketing Essentials",
            "Business Analytics for Beginners",
            "Graphic Design for Beginners",
            "Android App Development 101",
            "Artificial Intelligence Fundamentals",
            "Cybersecurity Fundamentals",
            "Project Management Essentials"
        ]

        # Randomly select a course from the suggestions
        suggested_course = random.choice(course_suggestions)

        # Provide the course suggestion as a response
        dispatcher.utter_message(f"I recommend taking the course '{suggested_course}'. It's a great choice!")

        return []
