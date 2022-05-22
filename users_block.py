import tweepy
import json
import sys
import re
import time

pattern_strings = re.compile(r'♡|💛|♥|💓|💖|❤|💔|💕|💙|💚|💜|💘|💝')


try:
    json_file= open("\\token.json","r")
    json_obj = json.load(json_file)
    AP = json_obj['twitter_token']['api_key']
    APS = json_obj['twitter_token']['secret_key']
    AT = json_obj['twitter_token']['access_token']
    AS = json_obj['twitter_token']['access_token_secret']
except Exception:
    print("jsonが読み込めませんでした")
    sys.exit()

def OAuth():
    try:
        auth = tweepy.OAuthHandler(AP,APS)
        auth.set_access_token(AT,AS)
        api = tweepy.API(auth,wait_on_rate_limit=True)
        return api
    except Exception:
        print("認証に失敗しました")
        sys.exit()

def get_follower(api,user):
    try:
        followers = api.followers_ids(user)
        return followers
    except tweepy.TweepError as e:
        print(e.reason)

def get_follow(api,user):
    try:
        follow = api.friends_ids(user)
        return follow
    except tweepy.TweepError as e:
        print(e.reason)

def  get_not_mutual(list1,list2):
    list3 = []
    length = len(list2)
    for f in range(length):
        if not list2[f] in list1:
            list3.append(list2[f])
    return list3
        

def get_bio(api,list3):
    block_list = []
    for i in list3:
        user = api.get_user(i)
        name = user.name
        bio = user.description
        if re.search(pattern_strings,bio):
            block_list.append(i)
    return block_list

def user_block(api,list4):
    for i in list4:
        api.create_block(i)
        user = api.get_user(i)
        name = user.name
        print(f"{name}をブロックしました")

if __name__=='__main__':
    print("ユーザー名を入力してください")
    user = input()
    api = OAuth()
    followers = get_follower(api,user)
    follow = get_follow(api,user)
    mutual = get_not_mutual(follow,followers)

    bio = get_bio(api,list(mutual))
    user_block(api,bio)
