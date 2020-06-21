from telegram.ext import(CommandHandler, MessageHandler, Filters, Updater)
import logging
import random
import os
from get_random_meme import get_meme
from get_gangsta_text import text
from get_movie_series import (get_recommendation, get_similar)
from get_text_insult import get_insult
from get_xkcd import get_comic
PORT = int(os.environ.get('PORT', 5000))
NEWLINE = '\n'
WHITESPACE = ' '


def meme(update, context):
    text = update.message.text.replace('/meme', ' ').strip()
    if text == '':
        response = get_meme()
        context.bot.send_photo(
            chat_id=update.effective_chat.id, photo=response[0], caption=response[1])
    else:
        response = get_meme(text.split(' '))
        if response == 0:
            context.bot.send_message(
                chat_id=update.effective_chat.id, text="This subreddit doesn't contain memes. Type /meme for random memes.")
        elif "Sorry" in response:
            context.bot.send_message(
                chat_id=update.effective_chat.id, text=response+" Type /meme for random memes")
        else:
            context.bot.send_photo(
                chat_id=update.effective_chat.id, photo=response[0], caption=response[1])


def start(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id, text="A little birdy told me you're bored.\nWhat's up?")


def is_bad_word(text):
    with open("bad_words.txt") as file:
        bad_words = set(file.read().split(NEWLINE))
        return len(text & bad_words) > 0


def xkcd(update, context):
    context.bot.send_photo(
        chat_id=update.effective_chat.id, photo=get_comic())


def insult(update, context):
    message = update.message.text.replace('/insult', ' ').strip()
    response = get_insult()
    if message == '':
        context.bot.send_message(
            chat_id=update.effective_chat.id, text=response)
    else:
        context.bot.send_message(
            chat_id=update.effective_chat.id, text=message+" "+response.lower())


def gangsta(update, context):
    message = update.message.text.replace('/gangsta', ' ').strip()
    if message == '':
        context.bot.send_message(
            chat_id=update.effective_chat.id, text="Type suttin' afta /gangsta dawg.")
    else:
        context.bot.send_message(
            chat_id=update.effective_chat.id, text="Itz pronounced like '"+text(message)+"' up in tha streets.")


def recommend(update, context):
    response = get_recommendation()
    context.bot.send_message(
        chat_id=update.effective_chat.id, text="Title : {}\n\nOverview : {}\n\nAverage vote : {}".format(response["title"], response["overview"], response["vote"]))
    context.bot.send_photo(
        chat_id=update.effective_chat.id, photo=response["poster"], caption="Here's the poster.")


def similar(update, context):
    message = update.message.text.replace('/similar', ' ').strip()
    if message == '':
        context.bot.send_message(
            chat_id=update.effective_chat.id, text="Type a movie name after /similar.")
    else:
        response = get_similar(message)
        if response == 0:
            context.bot.send_message(
                chat_id=update.effective_chat.id, text="Couldn't find movie. Try again.")
        elif response == 1:
            context.bot.send_message(
                chat_id=update.effective_chat.id, text="Couldn't find similar movie. Try again.")
        else:
            context.bot.send_message(chat_id=update.effective_chat.id, text="Title : {}\n\nOverview : {}\n\nAverage vote : {}".format(
                response["title"], response["overview"], response["vote"]))
            context.bot.send_photo(chat_id=update.effective_chat.id,
                                   photo=response["poster"], caption="Here's the poster.")


def bad_word(update, context):
    text = set(word.strip('.')
               for word in set(update.message.text.lower().split(WHITESPACE)))
    if is_bad_word(text):
        with open('insults_image_urls.txt', 'r') as file:
            urls = file.read().split('\n')
        context.bot.send_photo(chat_id=update.effective_chat.id,
                               photo=random.choice(urls), caption='@' + update.message.from_user.username)


if __name__ == "__main__":
    updater = Updater(
        token='BOT_TOKEN', use_context=True)
    dispatcher = updater.dispatcher
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)

    bad_words_handler = MessageHandler(
        Filters.text & (~Filters.command), bad_word)
    dispatcher.add_handler(bad_words_handler)

    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    meme_handler = CommandHandler('meme', meme)
    dispatcher.add_handler(meme_handler)

    gangsta_handler = CommandHandler('gangsta', gangsta)
    dispatcher.add_handler(gangsta_handler)

    recommend_handler = CommandHandler('recommend', recommend)
    dispatcher.add_handler(recommend_handler)

    similar_handler = CommandHandler('similar', similar)
    dispatcher.add_handler(similar_handler)

    insult_handler = CommandHandler('insult', insult)
    dispatcher.add_handler(insult_handler)

    xkcd_handler = CommandHandler('xkcd', xkcd)
    dispatcher.add_handler(xkcd_handler)

    updater.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path='BOT_TOKEN')
    updater.bot.setWebhook('APP_URL' +
                           'BOT_TOKEN')
    updater.idle()
