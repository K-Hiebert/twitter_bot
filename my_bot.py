import tweepy
from my_bot_functions import *
from connect_four import Game, RED, BLACK
from ai import Ai
import time

CONSUMER_KEY = "TrMvCk3uT4lZPqUZmOFy5cjxE"
CONSUMER_SECRET = "UVDTaf6wWkKxM0aQCeeinAZkDRTlyBrqwv54x28uukXBSVTOjm"
ACCESS_TOKEN = "1345971965048176640-Gfu4L7dC15locdBKtANFvz6kzKuFGP"
ACCESS_TOKEN_SECRET = "FTRuSrZEltqF6aPlYGVNqE4klsvGBQauZ6VQ1W1lQuWiC"

# Authentication
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET )

# Create API object
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
games = []
num_replies = 0

tweet(api, "To play Connect Four against an AI Bot, simply reply to this tweet by typing 'new'.\n")

initial_tweet = api.user_timeline()[0]

while True:
    time.sleep(3)
    replies = get_replies_to_tweet(api, initial_tweet)
    print(len(replies))
    # if we have a new game
    if (len(replies)) > num_replies:
        num_replies += 1
        print("got a reply")
        if (start_new_game(replies[0])):
            print("got a new game")
            tweet(api, "Hey " + replies[0].get('user_name') + ", you have started a new game. You are Red, and you move first. Reply to this tweet by typing "
                                                              "the column you would like to place your chip (1 - 7)\n")
            games.append([Game(), Ai(), api.user_timeline()[0], replies[0].get('user_name')])
            games[-1][1].set_game(games[-1][0])
    # make moves for all current games
    for i in range(len(games)):
        reply = get_replies_to_tweet(api, games[i][2])
        if len(reply) == 0:
            continue
        move = get_reply(reply[0])
        if move == -1:
            continue
        games[i][0].make_move(move - 1)
        api.update_status(status = "After your move " + games[i][3] + ":\n" + games[i][0].to_string(),
                          in_reply_to_status_id = reply[0].get('tweet_id') , auto_populate_reply_metadata=True)
        # if player won the game
        if (games[i][0].check_winning_move(RED)):
            api.update_status(status="Congrats " + games[i][3] + "! You Won! Please play again.",
                              in_reply_to_status_id=reply[0].get('tweet_id'), auto_populate_reply_metadata=True)
            del games[i]
            continue

        games[i][1].make_best_move()
        api.update_status(status = "After bot's move. Make move by replying[1-7], " + games[i][3] + ".\n" + games[i][0].to_string(),
                          in_reply_to_status_id = reply[0].get('tweet_id') , auto_populate_reply_metadata=True)
        if (games[i][0].check_winning_move(BLACK)):
            api.update_status(status= games[i][3] + ", Unfortunately you lost. Please play again.",
                              in_reply_to_status_id=reply[0].get('tweet_id'), auto_populate_reply_metadata=True)
            del games[i]
            continue
        if (games[i][0].is_over()):
            api.update_status(status= games[i][3] + ",It's a draw," + games[i][3] +". Nobody was able to win. Please play again.",
                              in_reply_to_status_id=reply[0].get('tweet_id'), auto_populate_reply_metadata=True)
            del games[i]
            continue
        games[i][2] = api.user_timeline()[0] #update the tweet to reply to.




