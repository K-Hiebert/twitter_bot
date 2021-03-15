import tweepy
from connect_four import Game

__all__ = ['get_replies_to_tweet', 'get_reply', 'tweet', 'start_new_game', 'get_start_board']

def get_replies_to_tweet(api, tweet):
    reply_list = []
    tweet_id = tweet.id
    user_name = tweet.user.screen_name
    max_id = None
    replies = tweepy.Cursor(api.search, q='to:{}'.format(user_name),
                                since_id=tweet_id, max_id=max_id, tweet_mode='extended').items()
    print('w')
    for reply in replies:
        print('q')
        # make sure to not hit query limits...
        if(reply.in_reply_to_status_id == tweet_id):
            reply_dict = {"user_name" : reply.user.name,
                          "user_id": reply.user.id,
                          "tweet_text": reply.full_text,
                          "tweet_id": reply.id}
            reply_list.append(reply_dict)
    return reply_list

def get_reply(tweet):
    text = tweet.get("tweet_text")
    text = text.replace("@SUpsets", "")
    text = text.replace(" ", "")
    try:
        move = int(text)
        if 1 <= move <= 7:
            return move
    except ValueError:
        return -1

def start_new_game(tweet):
    text = tweet.get("tweet_text")
    text = text.replace("@SUpsets", "")
    text = text.replace(" ", "")
    return text == 'new' or text == 'New'


# most difficult bug of detecting string duplicates.
def tweet(api, tweet):
    try:
        api.update_status(tweet)
    except tweepy.TweepError as e:
        # for past_tweet in api.user_timeline(tweet_mode = 'extended'):
        #     if (set(past_tweet.full_text.split(' ')) == set(tweet.split(' '))):
        #         api.destroy_status(past_tweet.id)
        for status in tweepy.Cursor(api.user_timeline).items():
            try:
                api.destroy_status(status.id)
            except:
                pass
        api.update_status(tweet)


# def tweet_reply(api, tweet):
#     try:
#         api.update_status(tweet)
#     except tweepy.TweepError as e:
#         for past_tweet in api.user_timeline(tweet_mode = 'extended'):
#             if (set(past_tweet.full_text.split(' ')) == set(tweet.split(' '))):
#                 api.destroy_status(past_tweet.id)
#         api.update_status(tweet)


def get_start_board():
    g = Game()
    return g.to_string()
