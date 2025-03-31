"""
Return a random response from a predefined pool
"""
import random

def failure_response():
    """
    Randomly returns a failure response.
    """
    responses = [
        "I'm sorry, but I cannot assist with that.",
        "Unfortunately, I don't have the information you're looking for.",
        "That's outside my area of expertise.",
        "I can't help you with that right now.",
        "I'm not able to provide assistance on that topic."
    ]
    return random.choice(responses)

def no_input():
    """
    Randomly returns a response if the user did not submit any input
    """
    responses = [
        "Hey! How can I help?",
        "Is there something you'd like to ask?",
        "I'm here to assist you. What do you need?",
        "Feel free to type your question or request.",
        "What can I do for you today?"
    ]
    return random.choice(responses)

def data_failure():
    """
    For when the json data fails to load, and the bot is unable to generate a response.
    """
    responses = [
        "Oops! Something went wrong while processing your request.",
        "I'm having trouble accessing the data right now.",
        "It seems there's an issue with the data.",
        "Sorry, I couldn't retrieve the information you need.",
        "There was an error loading the data. Can you try again?"
    ]
    return random.choice(responses)

def no_app_found():
    """
    For when the bot is unable to find an application.
    """
    responses = [
        "I couldn't find the application you're looking for.",
        "Sorry, but that application doesn't exist in my database.",
        "Unfortunately, I don't have information on that application.",
        "I can't seem to locate the application you mentioned.",
        "That application isn't available in my records."
    ]
    return random.choice(responses)

def no_defined_apps():
    """
    For when the user requests the bot to list applications, but they have no apps defined.
    """
    responses = [
        "You don't have any applications defined yet.",
        "It looks like you haven't set up any applications.",
        "I can't list any applications because none are defined.",
        "You need to define some applications first."
    ]
    return random.choice(responses)
