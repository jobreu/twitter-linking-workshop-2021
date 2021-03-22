#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import datetime
import math
import csv
import json
import traceback
import time

user_dict = {}
included_tweets_dict = {}
places_dict = {}
queried_at = int(datetime.datetime.now().timestamp())

def parse_tweet(raw_tweet):
    parsed_tweet = {
        "status_id":"",
        "created_at":"",
        "text":"",
        "conversation_id":"",
        "hashtags":"",
        "mentions":"",
        "url_location":"",
        "url_unwound":"",
        "url_title":"",
        "url_description":"",
        "url_sensitive":"",
        "geo":"",
        "lang":"",
        "reply_settings":"",
        "retweet_count":"",
        "reply_count":"",
        "like_count":"",
        "quote_count":"",
        "is_retweet":"",
        "is_reply":"",
        "is_quote":"",
        
        "retweeted_user_id":"",
        "retweeted_user_screen_name":"",
        "retweeted_user_name":"",
        "retweeted_user_followers_count":"",
        "retweeted_user_following_count":"",
        "retweeted_user_tweet_count":"",
        "retweeted_user_listed_count":"",
        "retweeted_user_protected":"",
        "retweeted_user_verified":"",
        "retweeted_user_description":"",
        "retweeted_tweet_status_id":"",
        "retweeted_tweet_conversation_id":"",
        "retweeted_tweet_created_at":"",
        "retweeted_tweet_lang":"",
        "retweeted_tweet_source":"",
        "retweeted_tweet_text":"",
        "retweeted_tweet_retweet_count": "",
        "retweeted_tweet_reply_count": "",
        "retweeted_tweet_like_count": "",
        "retweeted_tweet_quote_count": "",

        "replied_user_id":"",
        "replied_user_screen_name":"",
        "replied_user_name":"",
        "replied_user_followers_count":"",
        "replied_user_following_count":"",
        "replied_user_tweet_count":"",
        "replied_user_listed_count":"",
        "replied_user_protected":"",
        "replied_user_verified":"",
        "replied_user_description":"",
        "replied_tweet_status_id":"",
        "replied_tweet_conversation_id":"",
        "replied_tweet_created_at":"",
        "replied_tweet_lang":"",
        "replied_tweet_source":"",
        "replied_tweet_text":"",
        "replied_tweet_retweet_count": "",
        "replied_tweet_reply_count": "",
        "replied_tweet_like_count": "",
        "replied_tweet_quote_count": "",

        "quoted_user_id":"",
        "quoted_user_screen_name":"",
        "quoted_user_name":"",
        "quoted_user_followers_count":"",
        "quoted_user_following_count":"",
        "quoted_user_tweet_count":"",
        "quoted_user_listed_count":"",
        "quoted_user_protected":"",
        "quoted_user_verified":"",
        "quoted_user_description":"",
        "quoted_tweet_status_id":"",
        "quoted_tweet_conversation_id":"",
        "quoted_tweet_created_at":"",
        "quoted_tweet_lang":"",
        "quoted_tweet_source":"",
        "quoted_tweet_text":"",
        "quoted_tweet_retweet_count": "",
        "quoted_tweet_reply_count": "",
        "quoted_tweet_like_count": "",
        "quoted_tweet_quote_count": "",

        "geo_id":"",
        "geo_full_name":"",
        "geo_name":"",
        "geo_country":"",
        "geo_country_code":"",
        "geo_place_type":"",
        "geo_json":"",

        "user_id":"",
        "screen_name":"",
        "name":"",
        "account_created_at":"",
        "description":"",
        "url":"",
        "location":"",
        "followers_count":"",
        "following_count":"",
        "tweet_count":"",
        "listed_count":"",
        "protected":"",
        "verified":"",
        "queried_at":""
    }

    parsed_tweet["status_id"] = raw_tweet["id"]
    parsed_tweet["created_at"] = raw_tweet["created_at"]
    parsed_tweet["text"] = raw_tweet["text"]
    parsed_tweet["conversation_id"] = raw_tweet["conversation_id"]

    # entities
    if "entities" in raw_tweet.keys():
        if "hashtags" in raw_tweet["entities"].keys():
            parsed_tweet["hashtags"] = json.dumps([i["tag"] for i in raw_tweet["entities"]["hashtags"]])
        
        if "mentions" in raw_tweet["entities"].keys():
            parsed_tweet["mentions"] = json.dumps([i["username"] for i in raw_tweet["entities"]["mentions"]])

        if "urls" in raw_tweet["entities"].keys():
            try:
                parsed_tweet["url_location"] = json.dumps([i["expanded_url"] for i in raw_tweet["entities"]["urls"]])
            except:
                pass
            
            # experimental
            try:
                parsed_tweet["url_unwound"] = json.dumps([i["unwound_url"] for i in raw_tweet["entities"]["urls"]])
            except:
                pass

            try:
                parsed_tweet["url_title"] = json.dumps([i["title"] for i in raw_tweet["entities"]["urls"]])
            except:
                pass
            
            try:
                parsed_tweet["url_description"] = json.dumps([i["description"] for i in raw_tweet["entities"]["urls"]])
            except:
                pass

            try:
                parsed_tweet["url_sensitive"] = raw_tweet["possiby_sensitive"]
            except:
                pass

    
    # geo, needs testing
    # Check: https://developer.twitter.com/en/docs/twitter-api/data-dictionary/object-model/place
    try:
        parsed_tweet["geo_id"] = raw_tweet["geo"]["place_id"]
        parsed_tweet["geo_full_name"] = places_dict[raw_tweet["geo"]["place_id"]]["full_name"]
        parsed_tweet["geo_name"] = places_dict[raw_tweet["geo"]["place_id"]]["name"]
        parsed_tweet["geo_country"] = places_dict[raw_tweet["geo"]["place_id"]]["country"]
        parsed_tweet["geo_country_code"] = places_dict[raw_tweet["geo"]["place_id"]]["country_code"]
        parsed_tweet["place_type"] = places_dict[raw_tweet["geo"]["place_id"]]["geo_place_type"]
        parsed_tweet["geo_json"] = places_dict[raw_tweet["geo"]["place_id"]]["geo_json"]
    except:
        pass
    
    # BCP47 language tag
    try:
        parsed_tweet["lang"] = raw_tweet["lang"]
    except:
        pass
    
    parsed_tweet["reply_settings"] = raw_tweet["reply_settings"]
    parsed_tweet["source"] = raw_tweet["source"]

    parsed_tweet["retweet_count"] = raw_tweet["public_metrics"]["retweet_count"]
    parsed_tweet["reply_count"] = raw_tweet["public_metrics"]["reply_count"]
    parsed_tweet["like_count"] = raw_tweet["public_metrics"]["like_count"]
    parsed_tweet["quote_count"] = raw_tweet["public_metrics"]["quote_count"]

    if "referenced_tweets" in raw_tweet.keys():
        for referenced_tweet in raw_tweet["referenced_tweets"]:
            if referenced_tweet["type"] == "quoted":
                parsed_tweet["quoted_user_id"] = included_tweets_dict[referenced_tweet["id"]]["user_id"]
                parsed_tweet["quoted_user_screen_name"] = included_tweets_dict[referenced_tweet["id"]]["screen_name"]
                parsed_tweet["quoted_user_name"] = included_tweets_dict[referenced_tweet["id"]]["name"]
                parsed_tweet["quoted_user_followers_count"] = included_tweets_dict[referenced_tweet["id"]]["followers_count"]
                parsed_tweet["quoted_user_following_count"] = included_tweets_dict[referenced_tweet["id"]]["following_count"]
                parsed_tweet["quoted_user_tweet_count"] = included_tweets_dict[referenced_tweet["id"]]["tweet_count"]
                parsed_tweet["quoted_user_listed_count"] = included_tweets_dict[referenced_tweet["id"]]["listed_count"]
                parsed_tweet["quoted_user_protected"] = included_tweets_dict[referenced_tweet["id"]]["protected"]
                parsed_tweet["quoted_user_verified"] = included_tweets_dict[referenced_tweet["id"]]["verified"]
                parsed_tweet["quoted_user_description"] = included_tweets_dict[referenced_tweet["id"]]["description"]
                parsed_tweet["quoted_tweet_status_id"] = referenced_tweet["id"]
                parsed_tweet["quoted_tweet_conversation_id"] = included_tweets_dict[referenced_tweet["id"]]["conversation_id"]
                parsed_tweet["quoted_tweet_created_at"] = included_tweets_dict[referenced_tweet["id"]]["created_at"]
                parsed_tweet["quoted_tweet_lang"] = included_tweets_dict[referenced_tweet["id"]]["lang"]
                parsed_tweet["quoted_tweet_source"] = included_tweets_dict[referenced_tweet["id"]]["source"]
                parsed_tweet["quoted_tweet_text"] = included_tweets_dict[referenced_tweet["id"]]["text"]
                parsed_tweet["quoted_tweet_retweet_count"] = included_tweets_dict[referenced_tweet["id"]]["retweet_count"]
                parsed_tweet["quoted_tweet_reply_count"] = included_tweets_dict[referenced_tweet["id"]]["reply_count"]
                parsed_tweet["quoted_tweet_like_count"] = included_tweets_dict[referenced_tweet["id"]]["like_count"]
                parsed_tweet["quoted_tweet_quote_count"] = included_tweets_dict[referenced_tweet["id"]]["quote_count"]
            elif referenced_tweet["type"] == "retweeted":
                parsed_tweet["retweeted_user_id"] = included_tweets_dict[referenced_tweet["id"]]["user_id"]
                parsed_tweet["retweeted_user_screen_name"] = included_tweets_dict[referenced_tweet["id"]]["screen_name"]
                parsed_tweet["retweeted_user_name"] = included_tweets_dict[referenced_tweet["id"]]["name"]
                parsed_tweet["retweeted_user_followers_count"] = included_tweets_dict[referenced_tweet["id"]]["followers_count"]
                parsed_tweet["retweeted_user_following_count"] = included_tweets_dict[referenced_tweet["id"]]["following_count"]
                parsed_tweet["retweeted_user_tweet_count"] = included_tweets_dict[referenced_tweet["id"]]["tweet_count"]
                parsed_tweet["retweeted_user_listed_count"] = included_tweets_dict[referenced_tweet["id"]]["listed_count"]
                parsed_tweet["retweeted_user_protected"] = included_tweets_dict[referenced_tweet["id"]]["protected"]
                parsed_tweet["retweeted_user_verified"] = included_tweets_dict[referenced_tweet["id"]]["verified"]
                parsed_tweet["retweeted_user_description"] = included_tweets_dict[referenced_tweet["id"]]["description"]
                parsed_tweet["retweeted_tweet_status_id"] = referenced_tweet["id"]
                parsed_tweet["retweeted_tweet_conversation_id"] = included_tweets_dict[referenced_tweet["id"]]["conversation_id"]
                parsed_tweet["retweeted_tweet_created_at"] = included_tweets_dict[referenced_tweet["id"]]["created_at"]
                parsed_tweet["retweeted_tweet_lang"] = included_tweets_dict[referenced_tweet["id"]]["lang"]
                parsed_tweet["retweeted_tweet_source"] = included_tweets_dict[referenced_tweet["id"]]["source"]
                parsed_tweet["retweeted_tweet_text"] = included_tweets_dict[referenced_tweet["id"]]["text"]
                parsed_tweet["retweeted_tweet_retweet_count"] = included_tweets_dict[referenced_tweet["id"]]["retweet_count"]
                parsed_tweet["retweeted_tweet_reply_count"] = included_tweets_dict[referenced_tweet["id"]]["reply_count"]
                parsed_tweet["retweeted_tweet_like_count"] = included_tweets_dict[referenced_tweet["id"]]["like_count"]
                parsed_tweet["retweeted_tweet_quote_count"] = included_tweets_dict[referenced_tweet["id"]]["quote_count"]
                
            elif referenced_tweet["type"] == "replied_to":
                try:
                    parsed_tweet["replied_user_id"] = included_tweets_dict[referenced_tweet["id"]]["user_id"]
                    parsed_tweet["replied_user_screen_name"] = included_tweets_dict[referenced_tweet["id"]]["screen_name"]
                    parsed_tweet["replied_user_name"] = included_tweets_dict[referenced_tweet["id"]]["name"]
                    parsed_tweet["replied_user_followers_count"] = included_tweets_dict[referenced_tweet["id"]]["followers_count"]
                    parsed_tweet["replied_user_following_count"] = included_tweets_dict[referenced_tweet["id"]]["following_count"]
                    parsed_tweet["replied_user_tweet_count"] = included_tweets_dict[referenced_tweet["id"]]["tweet_count"]
                    parsed_tweet["replied_user_listed_count"] = included_tweets_dict[referenced_tweet["id"]]["listed_count"]
                    parsed_tweet["replied_user_protected"] = included_tweets_dict[referenced_tweet["id"]]["protected"]
                    parsed_tweet["replied_user_verified"] = included_tweets_dict[referenced_tweet["id"]]["verified"]
                    parsed_tweet["replied_user_description"] = included_tweets_dict[referenced_tweet["id"]]["description"]
                    parsed_tweet["replied_tweet_status_id"] = referenced_tweet["id"]
                    parsed_tweet["replied_tweet_conversation_id"] = included_tweets_dict[referenced_tweet["id"]]["conversation_id"]
                    parsed_tweet["replied_tweet_created_at"] = included_tweets_dict[referenced_tweet["id"]]["created_at"]
                    parsed_tweet["replied_tweet_lang"] = included_tweets_dict[referenced_tweet["id"]]["lang"]
                    parsed_tweet["replied_tweet_source"] = included_tweets_dict[referenced_tweet["id"]]["source"]
                    parsed_tweet["replied_tweet_text"] = included_tweets_dict[referenced_tweet["id"]]["text"]
                    parsed_tweet["replied_tweet_retweet_count"] = included_tweets_dict[referenced_tweet["id"]]["retweet_count"]
                    parsed_tweet["replied_tweet_reply_count"] = included_tweets_dict[referenced_tweet["id"]]["reply_count"]
                    parsed_tweet["replied_tweet_like_count"] = included_tweets_dict[referenced_tweet["id"]]["like_count"]
                    parsed_tweet["replied_tweet_quote_count"] = included_tweets_dict[referenced_tweet["id"]]["quote_count"]
                except:
                    parsed_tweet["replied_user_id"] = raw_tweet["in_reply_to_user_id"]
                
    # user fields
    parsed_tweet["user_id"] = raw_tweet["author_id"]
    parsed_tweet["screen_name"] = user_dict[raw_tweet["author_id"]]["username"]
    parsed_tweet["name"] = user_dict[raw_tweet["author_id"]]["name"]
    parsed_tweet["account_created_at"] = user_dict[raw_tweet["author_id"]]["created_at"]
    parsed_tweet["description"] = user_dict[raw_tweet["author_id"]]["description"]
    parsed_tweet["url"] = user_dict[raw_tweet["author_id"]]["url"]
    parsed_tweet["location"] = user_dict[raw_tweet["author_id"]]["location"]
    parsed_tweet["followers_count"] = user_dict[raw_tweet["author_id"]]["followers_count"]
    parsed_tweet["following_count"] = user_dict[raw_tweet["author_id"]]["following_count"]
    parsed_tweet["tweet_count"] = user_dict[raw_tweet["author_id"]]["tweet_count"]
    parsed_tweet["listed_count"] = user_dict[raw_tweet["author_id"]]["listed_count"]
    parsed_tweet["protected"] = user_dict[raw_tweet["author_id"]]["protected"]
    parsed_tweet["verified"] = user_dict[raw_tweet["author_id"]]["verified"]

    parsed_tweet["is_retweet"] = "False" if parsed_tweet["retweeted_tweet_status_id"] == "" else "True"
    parsed_tweet["is_reply"] = "False" if parsed_tweet["replied_tweet_status_id"] == "" else "True"
    parsed_tweet["is_quote"] = "False" if parsed_tweet["quoted_tweet_status_id"] == "" else "True"

    parsed_tweet["queried_at"] = queried_at

    return(parsed_tweet)

def parse_tweets(r):
    if "includes" in r.json().keys():
        if "users" in r.json()["includes"].keys():
            for user in r.json()["includes"]["users"]:
                if not user["id"] in user_dict.keys():
                    user_dict[user["id"]] = {}
                    try:
                        user_dict[user["id"]]["name"] = user["name"]
                    except:
                        user_dict[user["id"]]["name"] = ""

                    try:
                        user_dict[user["id"]]["username"] = user["username"]
                    except:
                        user_dict[user["id"]]["username"] = ""

                    try:
                        user_dict[user["id"]]["created_at"] = user["created_at"]
                    except:
                        user_dict[user["id"]]["created_at"] = ""

                    try:
                        user_dict[user["id"]]["description"] = user["description"]
                    except:
                        user_dict[user["id"]]["description"] = ""

                    try:
                        user_dict[user["id"]]["url"] = user["entities"]["url"]["urls"][0]["expanded_url"]
                    except:
                        try:
                            user_dict[user["id"]]["url"] = user["url"]
                        except:
                            user_dict[user["id"]]["url"] = ""

                    try:
                        user_dict[user["id"]]["location"] = user["location"]
                    except:
                        user_dict[user["id"]]["location"] = ""

                    try:
                        user_dict[user["id"]]["followers_count"] = user["public_metrics"]["followers_count"]
                    except:
                        user_dict[user["id"]]["followers_count"] = ""

                    try:
                        user_dict[user["id"]]["following_count"] = user["public_metrics"]["following_count"]
                    except:
                        user_dict[user["id"]]["following_count"] = ""

                    try:
                        user_dict[user["id"]]["tweet_count"] = user["public_metrics"]["tweet_count"]
                    except:
                        user_dict[user["id"]]["tweet_count"] = ""

                    try:
                        user_dict[user["id"]]["listed_count"] = user["public_metrics"]["listed_count"]
                    except:
                        user_dict[user["id"]]["listed_count"] = ""

                    try:
                        user_dict[user["id"]]["protected"] = user["protected"]
                    except:
                        user_dict[user["id"]]["protected"] = ""

                    try:
                        user_dict[user["id"]]["verified"] = user["verified"]
                    except:
                        user_dict[user["id"]]["verified"] = ""

        if "tweets" in r.json()["includes"].keys():
            for tweet in r.json()["includes"]["tweets"]:
                if not tweet["id"] in included_tweets_dict.keys():
                    included_tweets_dict[tweet["id"]] = {}
                    
                    included_tweets_dict[tweet["id"]]["conversation_id"] = tweet["conversation_id"]
                    included_tweets_dict[tweet["id"]]["created_at"] = tweet["created_at"]
                    included_tweets_dict[tweet["id"]]["lang"] = tweet["lang"]
                    included_tweets_dict[tweet["id"]]["source"] = tweet["source"]
                    included_tweets_dict[tweet["id"]]["text"] = tweet["text"]

                    included_tweets_dict[tweet["id"]]["retweet_count"] = tweet["public_metrics"]["retweet_count"]
                    included_tweets_dict[tweet["id"]]["reply_count"] = tweet["public_metrics"]["reply_count"]
                    included_tweets_dict[tweet["id"]]["like_count"] = tweet["public_metrics"]["like_count"]
                    included_tweets_dict[tweet["id"]]["quote_count"] = tweet["public_metrics"]["quote_count"]

                    included_tweets_dict[tweet["id"]]["user_id"] = tweet["author_id"]
                    included_tweets_dict[tweet["id"]]["screen_name"] = user_dict[tweet["author_id"]]["username"]
                    included_tweets_dict[tweet["id"]]["name"] = user_dict[tweet["author_id"]]["name"]
                    included_tweets_dict[tweet["id"]]["followers_count"] = user_dict[tweet["author_id"]]["followers_count"]
                    included_tweets_dict[tweet["id"]]["following_count"] = user_dict[tweet["author_id"]]["following_count"]
                    included_tweets_dict[tweet["id"]]["tweet_count"] = user_dict[tweet["author_id"]]["tweet_count"]
                    included_tweets_dict[tweet["id"]]["listed_count"] = user_dict[tweet["author_id"]]["listed_count"]
                    included_tweets_dict[tweet["id"]]["protected"] = user_dict[tweet["author_id"]]["protected"]
                    included_tweets_dict[tweet["id"]]["verified"] = user_dict[tweet["author_id"]]["verified"]
                    included_tweets_dict[tweet["id"]]["description"] = user_dict[tweet["author_id"]]["description"]

        if "places" in r.json()["includes"].keys():
            for place in r.json()["includes"]["places"]:
                if not place["id"] in places_dict.keys():
                    places_dict[place["id"]] = {}
                    try:
                        places_dict[place["id"]]["full_name"] = place["full_name"]
                    except:
                        places_dict[place["id"]]["full_name"] = ""
                    
                    try:
                        places_dict[place["id"]]["name"] = place["name"]
                    except:
                        places_dict[place["id"]]["name"] = ""
                    
                    try:
                        places_dict[place["id"]]["country"] = place["country_code"]
                    except:
                        places_dict[place["id"]]["country"] = ""
                    
                    try:
                        places_dict[place["id"]]["place_type"] = place["place_type"]
                    except:
                        places_dict[place["id"]]["place_type"] = ""
                    
                    try:
                        places_dict[place["id"]]["geo_json"] = json.dumps(place["geo"])
                    except:
                        places_dict[place["id"]]["geo_json"] = ""

    parsed_tweets = []
    for tweet in r.json()["data"]:
        parsed_tweets.append(parse_tweet(tweet))

    return(parsed_tweets)

def lookup_tweets(tweet_ids, bearer_token, verbose=True):
    headers = {
        "Authorization": "Bearer {}".format(bearer_token),
    }
    query_ids = tweet_ids
    if len(query_ids) > 100:
        raise Exception("Query too long, halting")
    params = (
        ("ids", ",".join(query_ids)),
        ("tweet.fields", "author_id,created_at,conversation_id,text,lang,geo,entities,reply_settings,public_metrics,source,referenced_tweets"),
        ("user.fields", "id,name,username,created_at,description,url,location,protected,verified,public_metrics,entities"),
        ("expansions", "referenced_tweets.id,referenced_tweets.id.author_id,in_reply_to_user_id,author_id,attachments.media_keys,entities.mentions.username,geo.place_id")
    )
    if verbose:
        print("Searching for tweets with the following parameters:")
        print("\tids:", ",".join(query_ids))

    try:
        r = requests.get("https://api.twitter.com/2/tweets", headers=headers, params=params)
    except:
        print("Error getting tweets (Error: {})".format(traceback.format_exc()))
        
    if (r.status_code == 429):
        sleep_time = math.ceil((datetime.datetime.fromtimestamp(int(r.headers["x-rate-limit-reset"])) - datetime.datetime.today()).total_seconds()) + 15
        if sleep_time < 15:
            sleep_time = 900
        if verbose:
            print("\t"*5, "Rate limit exceeded, resuming in {} seconds".format(str(sleep_time)))
        time.sleep(sleep_time)
        r = requests.get("https://api.twitter.com/2/tweets", headers=headers, params=params)

    if (r.status_code != 200):
        print("Error getting tweets (status code: {}), halting".format(r.status_code))
        print(r.text)
        exit()

    if "errors" in r.json().keys():
        print("No tweets found")
        return(None)

    queried_tweets = parse_tweets(r)
    print("Retrieved {} tweets".format(len(queried_tweets)))
    if verbose:
        print("\t{} of {} calls remaining.\n".format(r.headers["x-rate-limit-remaining"], r.headers["x-rate-limit-limit"]))
    return(queried_tweets)

def search_tweets(query, bearer_token, since_id=None, until_id=None, start_time=None, end_time=None, mode="recent", verbose=False):
    headers = {
        "Authorization": "Bearer {}".format(bearer_token),
    }
    if len(query) > 1024:
        raise Exception("Query too long, halting")
    params = (
        ("query", query),
        ("max_results", 100),
        ("tweet.fields", "author_id,created_at,conversation_id,text,lang,geo,entities,reply_settings,public_metrics,source,referenced_tweets"),
        ("user.fields", "id,name,username,created_at,description,url,location,protected,verified,public_metrics,entities"),
        ("expansions", "referenced_tweets.id,referenced_tweets.id.author_id,in_reply_to_user_id,author_id,attachments.media_keys,entities.mentions.username,geo.place_id")
    )

    if verbose:
        print("Searching for tweets with the following parameters:")
        print("\tquery:", query)

    if since_id:
        params = params + (("since_id", since_id),)
        if verbose:
            print("\tsince_id:", query)

    if until_id:
        params = params + (("until_id", until_id),)
        if verbose:
            print("\tuntil_id:", until_id)

    if start_time:
        params = params + (("start_time", start_time),)
        if verbose:
            print("\tstart_time:", start_time)

    if end_time:
        params = params + (("end_time", end_time),)
        if verbose:
            print("\tend_time:", end_time)


    try:
        r = requests.get("https://api.twitter.com/2/tweets/search/{}".format(mode), headers=headers, params=params)
    except:
        print("Error getting tweets (Error: {})".format(traceback.format_exc()))
    
    if (r.status_code == 429):
        sleep_time = math.ceil((datetime.datetime.fromtimestamp(int(r.headers["x-rate-limit-reset"])) - datetime.datetime.today()).total_seconds()) + 15
        if sleep_time < 15:
            sleep_time = 900
        if verbose:
            print("\t"*5, "Rate limit exceeded, resuming in {} seconds".format(str(sleep_time)), end="\r")
        time.sleep(sleep_time)
        r = requests.get("https://api.twitter.com/2/tweets/search/{}".format(mode), headers=headers, params=params)

    if (r.status_code != 200):
        print("Error getting tweets (status code: {}), halting".format(r.status_code))
        print(r.text)
        exit()

    if r.json()["meta"]["result_count"] == 0:
        print("No tweets found")
        return(None)

    searched_tweets = parse_tweets(r)

    if "next_token" in r.json()["meta"]:
        try:
            while "next_token" in r.json()["meta"]:
                if verbose:
                    print("Retrieved {} tweets".format(len(searched_tweets)), end="\r")
                next_token = r.json()["meta"]["next_token"]
                time.sleep(1.2)
                r = requests.get("https://api.twitter.com/2/tweets/search/{}".format(mode), headers=headers, params=params + (("next_token", next_token),))
                if (r.status_code == 429):
                    sleep_time = math.ceil((datetime.datetime.fromtimestamp(int(r.headers["x-rate-limit-reset"])) - datetime.datetime.today()).total_seconds()) + 15
                    if sleep_time < 15:
                        sleep_time = 900
                    if verbose:
                        print("\t"*5, "Rate limit exceeded, resuming in {} seconds".format(str(sleep_time)), end="\r")
                    time.sleep(sleep_time)
                    r = requests.get("https://api.twitter.com/2/tweets/search/{}".format(mode), headers=headers, params=params + (("next_token", next_token),))
                
                if r.json()["meta"]["result_count"] > 0:
                    searched_tweets.extend(parse_tweets(r))
        except:
            print("Error in while loop results, continuing (Traceback: {})".format(traceback.format_exc()))

    print("Retrieved {} tweets".format(len(searched_tweets)))
    if verbose:
        print("\t{} of {} calls remaining.\n".format(r.headers["x-rate-limit-remaining"], r.headers["x-rate-limit-limit"]))
    return(searched_tweets)

def tweets_to_csv(queried_tweets, file_name, append=False, verbose=False):
    file_mode = "a+" if append else "w"
    if verbose:
        print("Appending" if append else "Writing", "to file", file_name)
    if queried_tweets:
        with open(file_name, file_mode) as f:
            writer = csv.writer(f)
            if not append:
                writer.writerow([
                    "status_id",
                    "created_at",
                    "text",
                    "conversation_id",
                    "hashtags",
                    "mentions",
                    "url_location",
                    "url_unwound",
                    "url_title",
                    "url_description",
                    "url_sensitive",
                    "geo",
                    "lang",
                    "reply_settings",
                    "retweet_count",
                    "reply_count",
                    "like_count",
                    "quote_count",
                    "is_retweet",
                    "is_reply",
                    "is_quote",
                    "retweeted_user_id",
                    "retweeted_user_screen_name",
                    "retweeted_user_name",
                    "retweeted_user_followers_count",
                    "retweeted_user_following_count",
                    "retweeted_user_tweet_count",
                    "retweeted_user_listed_count",
                    "retweeted_user_protected",
                    "retweeted_user_verified",
                    "retweeted_user_description",
                    "retweeted_tweet_status_id",
                    "retweeted_tweet_conversation_id",
                    "retweeted_tweet_created_at",
                    "retweeted_tweet_lang",
                    "retweeted_tweet_source",
                    "retweeted_tweet_text",
                    "retweeted_tweet_retweet_count",
                    "retweeted_tweet_reply_count",
                    "retweeted_tweet_like_count",
                    "retweeted_tweet_quote_count",
                    "replied_user_id",
                    "replied_user_screen_name",
                    "replied_user_name",
                    "replied_user_followers_count",
                    "replied_user_following_count",
                    "replied_user_tweet_count",
                    "replied_user_listed_count",
                    "replied_user_protected",
                    "replied_user_verified",
                    "replied_user_description",
                    "replied_tweet_status_id",
                    "replied_tweet_conversation_id",
                    "replied_tweet_created_at",
                    "replied_tweet_lang",
                    "replied_tweet_source",
                    "replied_tweet_text",
                    "replied_tweet_retweet_count",
                    "replied_tweet_reply_count",
                    "replied_tweet_like_count",
                    "replied_tweet_quote_count",
                    "quoted_user_id",
                    "quoted_user_screen_name",
                    "quoted_user_name",
                    "quoted_user_followers_count",
                    "quoted_user_following_count",
                    "quoted_user_tweet_count",
                    "quoted_user_listed_count",
                    "quoted_user_protected",
                    "quoted_user_verified",
                    "quoted_user_description",
                    "quoted_tweet_status_id",
                    "quoted_tweet_conversation_id",
                    "quoted_tweet_created_at",
                    "quoted_tweet_lang",
                    "quoted_tweet_source",
                    "quoted_tweet_text",
                    "quoted_tweet_retweet_count",
                    "quoted_tweet_reply_count",
                    "quoted_tweet_like_count",
                    "quoted_tweet_quote_count",
                    "geo_id",
                    "geo_full_name",
                    "geo_name",
                    "geo_country",
                    "geo_country_code",
                    "geo_place_type",
                    "geo_json",
                    "user_id",
                    "screen_name",
                    "name",
                    "account_created_at",
                    "description",
                    "url",
                    "location",
                    "followers_count",
                    "following_count",
                    "tweet_count",
                    "listed_count",
                    "protected",
                    "verified",
                    "queried_at"
                    ])
            for parsed_tweet in queried_tweets:
                writer.writerow([
                    parsed_tweet["status_id"],
                    parsed_tweet["created_at"],
                    parsed_tweet["text"],
                    parsed_tweet["conversation_id"],
                    parsed_tweet["hashtags"],
                    parsed_tweet["mentions"],
                    parsed_tweet["url_location"],
                    parsed_tweet["url_unwound"],
                    parsed_tweet["url_title"],
                    parsed_tweet["url_description"],
                    parsed_tweet["url_sensitive"],
                    parsed_tweet["geo"],
                    parsed_tweet["lang"],
                    parsed_tweet["reply_settings"],
                    parsed_tweet["retweet_count"],
                    parsed_tweet["reply_count"],
                    parsed_tweet["like_count"],
                    parsed_tweet["quote_count"],
                    parsed_tweet["is_retweet"],
                    parsed_tweet["is_reply"],
                    parsed_tweet["is_quote"],
                    parsed_tweet["retweeted_user_id"],
                    parsed_tweet["retweeted_user_screen_name"],
                    parsed_tweet["retweeted_user_name"],
                    parsed_tweet["retweeted_user_followers_count"],
                    parsed_tweet["retweeted_user_following_count"],
                    parsed_tweet["retweeted_user_tweet_count"],
                    parsed_tweet["retweeted_user_listed_count"],
                    parsed_tweet["retweeted_user_protected"],
                    parsed_tweet["retweeted_user_verified"],
                    parsed_tweet["retweeted_user_description"],
                    parsed_tweet["retweeted_tweet_status_id"],
                    parsed_tweet["retweeted_tweet_conversation_id"],
                    parsed_tweet["retweeted_tweet_created_at"],
                    parsed_tweet["retweeted_tweet_lang"],
                    parsed_tweet["retweeted_tweet_source"],
                    parsed_tweet["retweeted_tweet_text"],
                    parsed_tweet["retweeted_tweet_retweet_count"],
                    parsed_tweet["retweeted_tweet_reply_count"],
                    parsed_tweet["retweeted_tweet_like_count"],
                    parsed_tweet["retweeted_tweet_quote_count"],
                    parsed_tweet["replied_user_id"],
                    parsed_tweet["replied_user_screen_name"],
                    parsed_tweet["replied_user_name"],
                    parsed_tweet["replied_user_followers_count"],
                    parsed_tweet["replied_user_following_count"],
                    parsed_tweet["replied_user_tweet_count"],
                    parsed_tweet["replied_user_listed_count"],
                    parsed_tweet["replied_user_protected"],
                    parsed_tweet["replied_user_verified"],
                    parsed_tweet["replied_user_description"],
                    parsed_tweet["replied_tweet_status_id"],
                    parsed_tweet["replied_tweet_conversation_id"],
                    parsed_tweet["replied_tweet_created_at"],
                    parsed_tweet["replied_tweet_lang"],
                    parsed_tweet["replied_tweet_source"],
                    parsed_tweet["replied_tweet_text"],
                    parsed_tweet["replied_tweet_retweet_count"],
                    parsed_tweet["replied_tweet_reply_count"],
                    parsed_tweet["replied_tweet_like_count"],
                    parsed_tweet["replied_tweet_quote_count"],
                    parsed_tweet["quoted_user_id"],
                    parsed_tweet["quoted_user_screen_name"],
                    parsed_tweet["quoted_user_name"],
                    parsed_tweet["quoted_user_followers_count"],
                    parsed_tweet["quoted_user_following_count"],
                    parsed_tweet["quoted_user_tweet_count"],
                    parsed_tweet["quoted_user_listed_count"],
                    parsed_tweet["quoted_user_protected"],
                    parsed_tweet["quoted_user_verified"],
                    parsed_tweet["quoted_user_description"],
                    parsed_tweet["quoted_tweet_status_id"],
                    parsed_tweet["quoted_tweet_conversation_id"],
                    parsed_tweet["quoted_tweet_created_at"],
                    parsed_tweet["quoted_tweet_lang"],
                    parsed_tweet["quoted_tweet_source"],
                    parsed_tweet["quoted_tweet_text"],
                    parsed_tweet["quoted_tweet_retweet_count"],
                    parsed_tweet["quoted_tweet_reply_count"],
                    parsed_tweet["quoted_tweet_like_count"],
                    parsed_tweet["quoted_tweet_quote_count"],
                    parsed_tweet["geo_id"],
                    parsed_tweet["geo_full_name"],
                    parsed_tweet["geo_name"],
                    parsed_tweet["geo_country"],
                    parsed_tweet["geo_country_code"],
                    parsed_tweet["geo_place_type"],
                    parsed_tweet["geo_json"],
                    parsed_tweet["user_id"],
                    parsed_tweet["screen_name"],
                    parsed_tweet["name"],
                    parsed_tweet["account_created_at"],
                    parsed_tweet["description"],
                    parsed_tweet["url"],
                    parsed_tweet["location"],
                    parsed_tweet["followers_count"],
                    parsed_tweet["following_count"],
                    parsed_tweet["tweet_count"],
                    parsed_tweet["listed_count"],
                    parsed_tweet["protected"],
                    parsed_tweet["verified"],
                    parsed_tweet["queried_at"]
                    ])
    else:
        if verbose:
            print("No tweets to write to file")