from requests_oauthlib import OAuth1Session
import os
import json
import markovify
import re
from janome.tokenizer import Tokenizer

api = OAuth1Session(os.environ["CONSUMER_KEY"],
                    os.environ["CONSUMER_SECRET"],
                    os.environ["ACCESS_TOKEN"],
                    os.environ["ACCESS_TOKEN_SECRET"])


def get_tweets(word, min_retweets=0, min_faves=0, retweets=False) -> (int, []):
    url = 'https://api.twitter.com/1.1/search/tweets.json'
    query = word + ' min_retweets:' + str(min_retweets) + ' min_faves:' + str(min_faves)
    if retweets == False:
        query += ' exclude:retweets'
    params = {
        'q': query,
        'count': 100  # max:100
    }
    res = api.get(url, params=params)
    if res.status_code == 200:
        tweets = json.loads(res.text)
        responses = tweets['statuses']
    else:
        print("ERROR: %d" % res.status_code)
        return res.status_code, None

    tweet_texts = []
    for r in responses:
        for k, v in r.items():
            if k == 'text':
                tweet_texts.append(v)
    return res.status_code, tweet_texts


def make_model(texts):
    if texts is None:
        print("ERROR: texts is none")
        exit()
    poko_modified = ''
    for p in texts:
        modified = re.sub('@[a-z|A-Z|0-9|_]*', '', p)
        modified = re.sub('[#|\n]*', '', modified)
        modified = re.sub('http[a-z|A-Z|0-9|_|/|.|:]*', '', modified)
        modified = re.sub('。', '.', modified)
        poko_modified += modified + '.'

    t = Tokenizer(wakati=True)
    poko_data = t.tokenize(poko_modified)
    sentence = ''
    for s in poko_data:
        if s == '.':
            sentence = sentence + '\n'
        else:
            sentence = sentence + ' ' + s
    model_poko = markovify.NewlineText(sentence, state_size=2)
    return model_poko


def create_sentence():
    # 前振りを作る
    c, t = get_tweets("かっこ")
    if c == 200:
        s1 = make_model(t).make_sentence_with_start("かっこ", max_words=50).replace(' ', '')
    else:
        exit(0)

    # 落ちを作る
    c, t = get_tweets("黙っ")
    if c == 200:
        s2 = make_model(t).make_sentence_with_start("黙っ", max_words=50).replace(' ', '')
    else:
        exit(0)
    return [s1, s2]


if __name__ == '__main__':
    print(create_sentence())