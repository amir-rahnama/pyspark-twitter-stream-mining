import re
from nltk.corpus import stopwords


class Util:

    @staticmethod
    def normalize(tweet):
        """
        :param tweet: tweet text
        :return: normalized text according to: Alec Go (2009)'s Twitter Sentiment Classification using Distant Supervision
        """
        # http://stackoverflow.com/questions/2304632/regex-for-twitter-username
        tweet = unicode(tweet)
        result = tweet.decode('unicode_escape').encode('ascii', 'ignore')
        result = re.sub('(?<=^|(?<=[^a-zA-Z0-9-_\.]))@([A-Za-z]+[A-Za-z0-9]+)', 'USER', result)
        result = result.replace('\\', '')
        result = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', 'URL', result)
        # result = re.sub('[^a-zA-Z]', ' ', result)
        result = result.lower().split()
        stops = set(stopwords.words("english"))
        tokens = [t for t in result if (not t in stops)]
        tokens = [t for t in tokens if "#" in t or t.isalnum()]

        return " ".join(tokens)
