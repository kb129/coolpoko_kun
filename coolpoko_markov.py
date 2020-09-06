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
def get_tweet_texts(word):
    url = 'https://api.twitter.com/1.1/search/tweets.json'
    query = word+' min_retweets:100 min_faves:100 exclude:retweets'
    params = {
        'q': query,
        'count': 100 # max:100
    }
    res = api.get(url, params=params)
    if res.status_code == 200:
        tweets = json.loads(res.text)
        responses = tweets['statuses']
    else:
        print("ERROR: %d" % res.status_code)
        return None

    tweet_texts = []
    for r in responses:
        for k, v in r.items():
            if k == 'text':
                tweet_texts.append(v)
    return tweet_texts

def make_markov_model(word):
    poko = get_tweet_texts(word)
    if poko is None:
        print("ERROR: poko is none")
        exit()
    poko_modified = ''
    for p in poko:
        r_uname = re.sub('@[a-z|A-Z|0-9|_]*', '', p)
        r_kigou = re.sub('[#|\n]*', '', r_uname)
        r_http = re.sub('http[a-z|A-Z|0-9|_|/|.|:]*', '', r_kigou)
        poko_modified = poko_modified + r_http + '.'

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

if __name__ == '__main__':
    m_female = make_markov_model("女")
    m_talk = make_markov_model("話")
    m_male = make_markov_model("男")
    m_quiet = make_markov_model("黙")

    m1 = markovify.combine([m_female, m_talk], [2,1])
    m2 = markovify.combine([m_male, m_quiet], [2,1])
    for _ in range(10):
        print(m1.make_short_sentence(200).replace(' ', ''))
        print("って言ってたやつがいたんですよ～")
        print("な～にぃ～！？")
        print("男は黙って")
        print(m2.make_short_sentence(40).replace(' ', ''))
        print()