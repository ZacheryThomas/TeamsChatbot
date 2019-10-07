import json
import random
import logging
import os

from requests import post, get
import html2markdown

from chatterbotapi import ChatterBotFactory, ChatterBotType

BEARER = os.getenv('BEARER')
MYID = os.getenv('MYID')
HEADERS = {"Authorization": "Bearer {}".format(BEARER)}

logger = logging.getLogger('botlogger')

def call_bot(message):
    """
    Calls bot given message

    Returns response of the bot as a string
    """
    factory = ChatterBotFactory()

    bot = factory.create(ChatterBotType.PANDORABOTS, 'b0dafd24ee35a477')
    botSession = bot.create_session()

    return botSession.think(message)


def bot_event(event, context):
    """
    Main funciton for bot
    """
    logger.info(event)
    logger.info(context)

    data = json.loads(event['body'])['data']

    roomId = data['roomId']
    personId = data['personId']
    messageId = data['id']

    logger.info('roomId: {}'.format(roomId))
    logger.info('personId: {}'.format(personId))

    # don't respond to yourself
    #   else it will just be an infinate loop
    if not personId == MYID:
        # Get text from message given message id
        res = get(url = "https://api.ciscospark.com/v1/messages/{}".format(messageId),
                    headers = HEADERS)

        text = res.json()['text']
        text = text.replace('Joey "The Machine" Ly', '')
        text = text.strip()

        # call bot and format response
        botResponse = call_bot(text)
        botResponse = botResponse.replace('target="_blank"', '')
        botResponse = html2markdown.convert(botResponse)

        logger.info('message: {}'.format(text))
        logger.info('bot response: {}'.format(botResponse))

        # post resposne to room as joeybot
        res = post(url = "https://api.ciscospark.com/v1/messages",
                    headers = HEADERS,
                    data = {
                                "markdown": botResponse,
                                "roomId": roomId
                            })

        logger.info('response from bot post: {}'.format(res))

    response = {
        "statusCode": 200,
    }

    return response
