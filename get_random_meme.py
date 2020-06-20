import praw
from prawcore import NotFound
import random
# 0 error code - no memes found
# Sorry error code - subreddit doesn't exist


def get_meme(subs=['memes', 'dankmemes']):
    def sub_exists(sub):
        exists = True
        try:
            reddit.subreddits.search_by_name(sub, exact=True)
        except NotFound:
            exists = False
        return exists

    reddit = praw.Reddit(client_id="CLIENT_ID",
                         client_secret="CLIENT_SECRET",
                         password="PASSWORD",
                         user_agent="USER_AGENT",
                         username="USERNAME")
    meme_captions_urls = []
    for sub in subs:
        if not sub_exists(sub):
            return "Sorry "+sub+" subreddit doesn't exist."
        for post in reddit.subreddit(sub).hot(limit=(50//len(subs))+10):
            if (post.url).endswith(('.jpg', '.png', '.jpeg')):
                meme_captions_urls.append([post.url, post.title])
    return random.choice(meme_captions_urls) if len(meme_captions_urls) > 0 else 0


if __name__ == "__main__":
    print(get_meme())
