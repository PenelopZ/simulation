
# coding: utf-8

# In[1]:

import pandas as pd
import random
import tweepy
import json,csv
import re, string
from sklearn.utils import shuffle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import SGDClassifier
from textblob import TextBlob
import urllib,urllib.parse,urllib.request



# In[2]:

wmuseum = ['museum', 'museums', 'history', 'learning', 'exhibit', 'exhibits', 'gallery', 'galleries', 'archive',
           'art', 'science', 'collection', 'visit', 'curator', 'painting', 'curio', 'statuary', 'artwork',
           'dinosaur', 'showcase','fresco']
wpark = ['park', 'parks', 'garden', 'outdoor', 'parkland', 'ballpark', 'commons', 'mall', 'campground',
         'green', 'playground', 'yosemite', 'yellowstone', 'fair', 'lawn', 'beach', 'marina', 'lake', 'lakeside',
         'grove', 'coast', 'bay', 'river', 'boat', 'boating', 'yatch', 'ski', 'resort', 'slide',
         'disney', 'disneyworld', 'ranger', 'reserve', 'sanctuary', 'hike', 'trek', 'trail', 'wildlife', 'refuge',
         'cloud','sunrise','sunset','dolomites','flowers','mount','florets','fields','waterpark','sanctuary','zoo',
         'clouds', 'skies', 'bridge', 'walk', 'skydiving','sea','cruise','caves']
wsports = ['sport', 'sports', 'baseball', 'stadium', 'hockey', 'football', 'soccer', 'nfl', 'afl', 'basketball',
           'score', 'scores', 'player', 'players', 'bat', 'batting', 'pitch', 'pitches', 'pitched', 'touchdown',
           'catch', 'catching', 'caught', 'field', 'golf', 'league', 'homerun', 'sporting', 'team',
           'athletic', 'athletics', 'boxing', 'clubs', 'club', 'game', 'games', 'pros', 'arena', 'coach',
           'referee', 'coliseum', 'mvp', 'fan', 'track', 'sportsman', 'captain', 'win', 'won', 'winning',
           'loss', 'lost', 'losing', 'losses', 'loses', 'scoring', 'scored', 'playing', 'rink', 'dome',
           'putt', 'tie', 'homerun','canal']
wfood = ['restaurant', 'coffee shop', 'diner', 'canteen', 'eatery', 'fastfood', 'grill', 'cafe', 'tasty',
         'delicious', 'pizzeria', 'grill', 'spicy', 'sweet', 'bland', 'crispy', 'delectable', 'flavored',
         'greasy', 'grilled', 'healthy', 'hot', 'juicy', 'mouth-watering', 'organic', 'palatable',
         'succulent', 'tart', 'tender', 'steakhouse', 'seafood', 'breakfast', 'lunch', 'brunch','winetime',
         'dinner', 'supper', 'food', 'meat', 'fish', 'eat', 'eating', 'burger', 'continental', 'deli','doughnuts',
         'sushi','sashimi','pairing', 'restaurants'
         'chinese', 'asian', 'indian', 'soulfood', 'pastry', 'dessert', 'beet', 'wine','dish','dishes']
wbuildings = ['basilica', 'cathedral', 'mosque', 'temple', 'statehouse', 'courthouse', 'capitol',
              'library', 'university', 'shrine', 'historical', 'monument', 'synagogue', 'mill', 'skyway',
              'building', 'convent', 'monastery','chateau']


# In[3]:

def strip_links(text):
    link_regex    = re.compile('((https?):((//)|(\\\\))+([\w\d:#@%/;$()~_?\+-=\\\.&](#!)?)*)', re.DOTALL)
    links         = re.findall(link_regex, text)
    for link in links:
        text = text.replace(link[0], ', ')
    t = text.lower()
    t = re.sub('\d+','',t)
    t = ' '.join(t.split())
    return t

def strip_all_entities(text):
    entity_prefixes = ['@']
    for separator in  string.punctuation:
        if separator not in entity_prefixes :
            text = text.replace(separator,' ')
    words = []
    for word in text.split():
        word = word.strip()
        if word:
            if word[0] not in entity_prefixes:
                words.append(word)
    return ' '.join(words)

def cfactor(n):
    if n <= 0:
        return 0
    elif n<=10:
        return 0.2
    elif n<=30:
        return 0.5
    elif n<=100:
        return 0.8
    else:
        return 1

def tfactor(n):
    return n/140.0

def get_user_preferences(usertweets,tscore):
    tcount = 0
    pcats = ['Buildings', 'Restaurants', 'Museums', 'Parks', 'Stadiums', 'Others']
    pplaces = [0, 0, 0, 0, 0, 0]
    nplaces = [0, 0, 0, 0, 0, 0]
    uplaces = [0, 0, 0, 0, 0, 0]
    cnt = 0
    for tweet in usertweets:
        cat = [0, 0, 0, 0, 0]
        tcount += 1
        tx = (TextBlob(tweet)).sentiment.polarity
        for word in tweet.split(" "):
            if word in wbuildings:
                cat[0] += 1
            if word in wfood:
                cat[1] += 1
            if word in wmuseum:
                cat[2] += 1
            if word in wpark:
                cat[3] += 1
            if word in wsports:
                cat[4] += 1
        m = max(cat)
        if m == 0:
            if tx < 0:
                nplaces[5] += 1
            elif tx == 0:
                uplaces[5] += 1
            else:
                pplaces[5] += 1
        else:
            for c in range(0, 5):
                if m == cat[c]:
                    if tx < 0:
                        nplaces[c] += tscore[cnt]
                    elif tx == 0:
                        uplaces[c] += tscore[cnt]
                    else:
                        pplaces[c] += tscore[cnt]
        cnt += 1
    nnplaces = []
    npplaces = []
    nuplaces = []
    tmax = max(nplaces[0:5])
    for x in nplaces:
        nnplaces.append(x/tmax) if tmax>0 else nnplaces.append(x)
    tmax = max(uplaces[0:5])
    for x in uplaces:
        nuplaces.append(x/tmax) if tmax>0 else nuplaces.append(x)
    tmax = max(pplaces[0:5])
    for x in pplaces:
        npplaces.append(x/tmax) if tmax>0 else npplaces.append(x)        
    return tcount,pcats,npplaces,nuplaces,nnplaces


# In[4]:
filepath = "C:/Users/Shengya/Documents/#Twitter#Project/TC/"
filepathTB = "C:/Users/Shengya/Documents/#Twitter#Project/TC2/"
tweets_file = filepath+"A__tweets.csv"


alltweets = pd.read_csv(tweets_file,names=["tweet","tag"])
alltweets = alltweets.sample(frac=1).reset_index(drop=True)
tv = TfidfVectorizer()
x_train = tv.fit_transform(alltweets['tweet'].values)
y_train = alltweets['tag'].values
SGDClass = SGDClassifier()
SGDClass.fit(x_train,y_train)


# In[5]:

def get_user_tweets(user,src):
    user_tweets = []
    usr = []
    tscore = []
    tnscore = []
    maxscore = 0

    collect_all = []
    collect_tra = []

    try:
        for page in tweepy.Cursor(client.user_timeline, screen_name=user, count=200).pages(16):
            for status in page:
                try:
                    if status.lang in ['en']:
                        if status.retweeted:
                            stat = status.retweeted_status
                            usr.append(stat.user.screen_name)
                        else:
                            stat = status
                        
                        #to get more tweets for ML
                        tt = stat.text.split()
                        twt = []
                        for word in tt:
                            if (word[0:4] != 'http'):
                                twt.append(word)
                        try:
                            collect_all.append([src," ".join(twt)])
                            #writer.writerow([" ".join(twt)])
                        except:
                            continue
                        
                        tweet = strip_all_entities(strip_links(stat.text))
                        tag = SGDClass.predict(tv.transform([tweet]))
                        if tag in ['y']:
                            ts = 0.0
                            ts += cfactor(stat.favorite_count)
                            ts += cfactor(stat.retweet_count)
                            ts += len(stat.entities['hashtags']) * 0.3
                            ts += len(stat.entities['urls']) * 0.4
                            ts += len(stat.entities['user_mentions']) * 0.3
                            ts += len(stat.entities['media']) * 0.6
                            ts += tfactor(len(tweet))
                            if ts > maxscore:
                                maxscore = ts
                            tscore.append(ts)
                            user_tweets.append(tweet)
                            #print(tweet)
                            collect_tra.append([src,tweet,ts,"y"])
                            #twriter.writerow([tweet,"y"])
                except:
                    continue
    except:
        pass
    if len(user_tweets) >= REQUIREDTWEETS or src=='U':
        try:
            for [ufl,zn] in collect_all:
                writer.writerow([ufl,zn])
        except:
            pass
        try:
            for [ufl,zn,sc,t] in collect_tra:
                twriter.writerow([ufl,zn,sc,t])
        except:
            pass

    fptr.flush()
    tfile.flush()
    for s in tscore:
        tnscore.append(s/maxscore)
    return user_tweets,tnscore,usr

# In[51]:

access_token = "781560941758517248-lBqivXjuB0Sizby1rhV0oQ7Z9ayuL65"
access_token_secret = "UnpFJgnTTETCThJyPZVitaZduSQWP28H5IdNWbTkP98TP"
consumer_key = "ZpqEpC08CZp64Yywimm0Qde5c"
consumer_secret = "g42J7044S2JMPWtBWNKNQcc9nfl6lTSw6wLX2idxLRhTsQbJp9"

#https://github.com/truthy/botornot-python
#BotOrNot: A System to Evaluate Social Bots https://arxiv.org/abs/1602.00975v1
import botornot
twitter_app_auth = {
    'consumer_key': consumer_key,
    'consumer_secret': consumer_secret,
    'access_token': access_token,
    'access_token_secret': access_token_secret,
  }
bon = botornot.BotOrNot(**twitter_app_auth)


def build_URL(search_text='', types_text=''):
    base_url = 'https://maps.googleapis.com/maps/api/place/textsearch/json'  # Can change json to xml to change output type
    key_string = '?key=' + 'AIzaSyC5XkmbFeERH4REnnpVVHqHMHMCRE1lDh8'  # First think after the base_url starts with ? instead of &
    query_string = '&query=' + urllib.parse.quote(search_text)
    sensor_string = '&sensor=false'  # Presumably you are not getting location from device GPS
    type_string = ''
    if types_text != '':
        type_string = '&types=' + urllib.parse.quote(
            types_text)  # More on types: https://developers.google.com/places/documentation/supported_types
    url = base_url + key_string + query_string + sensor_string + type_string
    return url


userlist = ['sollyde']
#'adolfo112','truman_ross','PetersonBecca','_wiscago','austinb0hn','erinjuliah','susyzuciy','neeraliii',
#            'ConnorWRoseYork','MikeNick_','pennnay','JaniePetit',
#            'ohmygoy','cynxhernandez','Nakia_Amya', 'JohnMcClellanXO',
#            'joebencoelho','m_cragin','oliverddsouza','alexduochn','sollyde','adolfo112']



REQUIREDTWEETS = 15
BOT_THRESHHOLD = 0.40



for user in userlist:
    #user = input("Enter username :")
    print("User: ",user)
    tfilename = filepath + "TW_"+user+".txt"
    tfile = open(tfilename, 'w', newline="")
    twriter = csv.writer(tfile)

    try:
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        client = tweepy.API(auth,wait_on_rate_limit=True)
        uclient = client.get_user(user,wait_on_rate_limit=True)
    except:
        print('Unable to authenticate Twitter connection....')
        client = -1



    fptr = open(filepath+'T_%s_tweets.csv' % user, 'w', newline="")
    writer = csv.writer(fptr)


    # In[52]:

    if (client != -1):
        usertweets,utscore,usr = get_user_tweets(user,'U')
    tcount,pcats,upplaces,uuplaces,unplaces = get_user_preferences(usertweets,utscore)


    # In[53]:

    #for a in range(0, 6):
    #    print('{:15}'.format(pcats[a]), '{:8.3f}'.format(upplaces[a]), '{:8.3f}'.format(uuplaces[a]), '{:8.3f}'.format(unplaces[a]))


    # In[54]:

    frlist = []
    friendlist = []
    friends_all =[f.screen_name for f in uclient.friends(count=100)]
    print("No. of Friends : ",len(friends_all))
    for friend in friends_all:
        if friend in usr:
            frlist.append(friend)
    for friend in friends_all:
        if friend not in frlist:
            frlist.append(friend)

    for f in frlist:
        try:
            score = bon.check_account(f)['score']
            if score<BOT_THRESHHOLD:
                friendlist.append(f)
        except:
            continue


    # In[55]:

    fpplaces = [0,0,0,0,0,0]
    fuplaces = [0,0,0,0,0,0]
    fnplaces = [0,0,0,0,0,0]
    fcount = 0
    for fuser in friendlist:
        usertweets,ftscore,fusr = get_user_tweets(fuser,'F')
        print('             ',fuser,len(usertweets))
        if len(usertweets)>=REQUIREDTWEETS:
            print("Friend : ",fuser)
            tcount,pcats,pplaces,uplaces,nplaces = get_user_preferences(usertweets,ftscore)
            for a in range(0, 6):
                fpplaces[a] += pplaces[a]
                fuplaces[a] += uplaces[a]
                fnplaces[a] += nplaces[a]
            fcount += 1
        if fcount == 10:
            break
    fnnplaces = []
    fnpplaces = []
    fnuplaces = []
    tmax = max(fnplaces[0:5])
    for x in fnplaces:
        fnnplaces.append(x/tmax) if tmax>0 else fnnplaces.append(x)
    tmax = max(fuplaces[0:5])
    for x in fuplaces:
        fnuplaces.append(x/tmax) if tmax>0 else fnuplaces.append(x)
    tmax = max(fpplaces[0:5])
    for x in fpplaces:
        fnpplaces.append(x/tmax) if tmax>0 else fnpplaces.append(x)


    # In[ ]:

    #for a in range(0, 6):
    #    print('{:15}'.format(pcats[a]), '{:8.3f}'.format(fnpplaces[a]), '{:8.3f}'.format(fnuplaces[a]), '{:8.3f}'.format(fnnplaces[a]))


    # In[ ]:

    lpplaces = [0,0,0,0,0,0]
    luplaces = [0,0,0,0,0,0]
    lnplaces = [0,0,0,0,0,0]
    followlist = []

    fllist =[f.screen_name for f in uclient.followers(count=100)]
    print("No. of Followers : ", len(fllist))

    for follower in fllist:
        print('              ',follower,'   ',end="")
        if (len(followlist) >= 10):
            break
        if follower not in friendlist:
            #if (follower in usr) or ([i for i in usr if i in friendlist]):
            try:
                score = bon.check_account(follower)['score']
                print(':: ', score, end="")
                if score < BOT_THRESHHOLD:
                    usertweets,ltscore,lusr = get_user_tweets(follower,'L')
                    print('             ', follower, len(usertweets))
                    if (len(usertweets))>=REQUIREDTWEETS:
                        print("Follower : ", follower)
                        followlist.append(follower)
                        tcount, pcats, pplaces, uplaces, nplaces = get_user_preferences(usertweets, ltscore)
                        print('  ::  ', len(usertweets))
                        for a in range(0, 6):
                            lpplaces[a] += pplaces[a]
                            luplaces[a] += uplaces[a]
                            lnplaces[a] += nplaces[a]
            except:
                continue

    for follower in fllist:
        if (len(followlist) >= 10):
            break
        print('              ', follower, '   ', end="")
        if (follower not in followlist) and (follower not in friendlist):
            try:
                score = bon.check_account(follower)['score']
                print(':: ',score,end="")
                if score < BOT_THRESHHOLD:
                    usertweets, ltscore, lusr = get_user_tweets(follower,'L')
                    print('  ::  ',len(usertweets))
                    if (len(usertweets)) >= REQUIREDTWEETS:
                        print("Follower : ", follower)
                        followlist.append(follower)
                        tcount, pcats, pplaces, uplaces, nplaces = get_user_preferences(usertweets, ltscore)
                        for a in range(0, 6):
                            lpplaces[a] += pplaces[a]
                            luplaces[a] += uplaces[a]
                            lnplaces[a] += nplaces[a]
            except:
                continue


    lnnplaces = []
    lnpplaces = []
    lnuplaces = []
    tmax = max(lnplaces[0:5])
    for x in lnplaces:
        lnnplaces.append(x/tmax) if tmax>0 else lnnplaces.append(x)
    tmax = max(luplaces[0:5])
    for x in luplaces:
        lnuplaces.append(x/tmax) if tmax>0 else lnuplaces.append(x)
    tmax = max(lpplaces[0:5])
    for x in lpplaces:
        lnpplaces.append(x/tmax) if tmax>0 else lnpplaces.append(x)


    # In[ ]:

    #for a in range(0, 6):
    #    print('{:15}'.format(pcats[a]), '{:8.3f}'.format(lnpplaces[a]), '{:8.3f}'.format(lnuplaces[a]), '{:8.3f}'.format(lnnplaces[a]))


    # In[ ]:

    fptr.close()

    fscore = [0, 0, 0, 0, 0, 0]
    fscr_u = [0, 0, 0, 0, 0, 0]
    fscr_f = [0, 0, 0, 0, 0, 0]
    fscr_l = [0, 0, 0, 0, 0, 0]
    frec = [['', 0], ['', 0], ['', 0], ['', 0], ['', 0], ['', 0]]
    for a in range(0, 6):
        fscr_u[a] = upplaces[a] + uuplaces[a] * 0.7 + unplaces[a] * 0.3
        fscr_f[a] = fpplaces[a] + fuplaces[a] * 0.7 + fnplaces[a] * 0.3
        fscr_l[a] = lpplaces[a] + luplaces[a] * 0.7 + lnplaces[a] * 0.3
        fscore[a] = (upplaces[a] + fpplaces[a] * 0.65 + lpplaces[a] * 0.35) * 1.0 + (uuplaces[a] + fuplaces[a] * 0.65 +
                                                                                     luplaces[a] * 0.35) * 0.7 + (
                                                                                                                 unplaces[
                                                                                                                     a] +
                                                                                                                 fnplaces[
                                                                                                                     a] * 0.65 +
                                                                                                                 lnplaces[
                                                                                                                     a] * 0.35) * 0.30
    tmax = sum(fscore[0:5])
    utmax = sum(fscr_u[0:5])
    ftmax = sum(fscr_f[0:5])
    ltmax = sum(fscr_l[0:5])
    for a in range(0, 6):
        frec[a][0] = pcats[a]
        frec[a][1] = (fscore[a] / tmax if tmax > 0 else fscore[a])
        fscr_u[a] = (fscr_u[a] / utmax if utmax > 0 else fscr_u[a])
        fscr_f[a] = (fscr_f[a] / ftmax if ftmax > 0 else fscr_f[a])
        fscr_l[a] = (fscr_l[a] / ltmax if ltmax > 0 else fscr_l[a])

    dbrow = [user]
    #for a in range(0, 6):
    #    dbrow = dbrow + [float('{:8.2f}'.format(fscr_u[a]))]
    #for a in range(0, 6):
    #    dbrow = dbrow + [float('{:8.2f}'.format(fscr_f[a]))]
    #for a in range(0, 6):
    #    dbrow = dbrow + [float('{:8.2f}'.format(fscr_l[a]))]
    for a in range(0, 6):
        dbrow = dbrow + [float('{:8.2f}'.format(frec[a][1]))]

    fpdb = open(filepath+'RSdatabase.csv', 'a', newline="")
    fpdbw = csv.writer(fpdb)
    fpdbw.writerow(dbrow)
    fpdb.close()
    tfile.close()
    fptr.close()

    frec = sorted(frec, key=lambda x: x[1], reverse=True)
    print("===>", user)
    for a in range(0, 6):
        print('{:15}'.format(frec[a][0]),'{:8.2f}'.format(frec[a][1]))
        #print('{:15}'.format(frec[a][0]), '{:8.2f}'.format(fscr_u[a]), '{:8.2f}'.format(fscr_f[a]),
        #      '{:8.2f}'.format(fscr_l[a]), '{:8.2f}'.format(frec[a][1]))

'''
    placetovisit = random.choice(['New York','Washington DC','San Francisco','Los Angeles','Chicago','Orlando','Seattle'])

    #frec = sorted(frec, key=lambda x: x[1], reverse=True)
    for l in range(1, 6):
        if (frec[l][1]>0 and round(frec[l][1]*15)<1):
            n = 1
        else:
            n = round(frec[l][1]*15)
        print(frec[l][0],n)
        print('------------------------')
        lookurl = build_URL(search_text=frec[l][0] + ' in ' + placetovisit)
        response = urllib.request.urlopen(lookurl)

        jsonRaw = response.read().decode('utf-8')
        jsonData = json.loads(jsonRaw)
        for cnt in range(0, n):
            try:
                print(jsonData['results'][cnt]['name'], jsonData['results'][cnt]['formatted_address'])
            except:
                continue

'''
