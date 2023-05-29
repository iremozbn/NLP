import pandas as pd
import re 
import snowballstemmer 
from sklearn.feature_extraction.text import CountVectorizer #bow için kullanılan kütüphane
from sklearn.feature_extraction.text import TfidfVectorizer #bowdan daha yaygın
from gensim.models import Word2Vec #nlp kütüphanesi

#sayısal değerlerin kaldırılması
def remove_numeric(value):
    bfr= [item for item in value if not item.isdigit()]
    bfr="".join(bfr)
    return bfr

def remove_emoji(value):
    bfr = re.compile("[\U00010000-\U0010ffff]", flags=re.UNICODE)
    bfr = bfr.sub(r'', value)
    return bfr

#tek karakterli ifadeleri kaldırma
def remove_sing_char(value):
    return re.sub(r'(?:^| )\w(?:$| )','',value)

#noktalama işaretlerini kaldırma
def remove_noktalama(value):
    return re.sub(r'[^\w\s]','',value)

#linkleri kaldırma
def remove_link(value):
    return re.sub('((www\.[^\s]+)|(https?://[^\s]+))','',value)

#hashtag kaldırma
def remove_hashtag(value):
    return re.sub(r'#\S+', '', value)

def remove_username(value):
    return re.sub('@[^\s]+','',value)

def stem_word(value):
    stemmer=snowballstemmer.stemmer("turkish")
    value=value.lower()
    value =stemmer.stemWords(value.split())
    stopwords = [
    'acaba', 'altı', 'altmış', 'ama', 'ancak', 'arada', 'aslında', 'ayrıca', 'az', 'bana',
    'bazen', 'bazı', 'bazıları', 'belki', 'ben', 'beni', 'benim', 'beş', 'bile', 'bin', 'bir',
    'birçok', 'biri', 'birkaç', 'birkez', 'birşey', 'birşeyi', 'biz', 'bize', 'bizden', 'bizi',
    'bizim', 'böyle', 'böylece', 'bu', 'buna', 'bunda', 'bundan', 'bunu', 'bunun', 'burada',
    'bütün', 'çok', 'da', 'daha', 'dahi', 'de', 'defa', 'diğer', 'diye', 'doksan', 'dokuz', 'dolayı',
    'dört', 'elbette', 'en', 'fakat', 'falan', 'felan', 'filan', 'gene', 'gibi', 'hem', 'henüz',
    'hep', 'hepsi', 'her', 'her biri', 'herkes', 'herkese', 'herkesi', 'hiç', 'hiç kimse', 'hiçbiri',
    'iki', 'ile', 'ilgili', 'itibaren', 'itibariyle', 'kaç', 'kadar', 'kendi', 'kendilerine', 'kendini',
    'kendisi', 'kendisine', 'kendisini', 'kez', 'ki', 'kim', 'kime', 'kimi', 'kimse', 'madem', 'mı',
    'mi', 'mu', 'mü', 'nasıl', 'ne', 'neden', 'nedenle', 'nerde', 'nerede', 'nereden', 'nereye',
    'nesi', 'neyse', 'niçin', 'niye', 'o', 'olan', 'olarak', 'oldu', 'olduğu', 'olduğunu', 'olduklarını',
    'olmadı', 'olmadığı', 'olmak', 'olması', 'olmayan', 'olmaz', 'olsa', 'olsun', 'olup', 'olur', 'olursa',
    'oluyor', 'on', 'ona', 'ondan', 'onlar', 'onlara', 'onlardan', 'onları', 'onların', 'onu', 'onun',
    'orada', 'oysa', 'oysaki', 'öbürü', 'ön', 'önce', 'ötürü', 'öyle', 'pek', 'rağmen', 'sadece', 'sanki',
    'şayet', 'siz', 'sizden', 'size', 'sizi','tabii', 'tamam', 'tamamen', 'tarafından', 'trilyon', 'tüm', 
    've', 'veya', 'ya', 'yani', 'yapacak', 'yapılan', 'yapılması', 'yapıyor', 'yapmak', 'yaptı', 
    'yaptığı', 'yaptığını', 'yaptıkları', 'yedi', 'yerine', 'yetmiş', 'yine', 'yoksa', 'zaten', 'zira']
    value=[item for item in value if not item in stopwords]
    value = ' '.join(value)
    return value


def pre_processing(value):
    return [remove_numeric(
              remove_emoji(
                remove_sing_char(
                 remove_noktalama(
                  remove_link(
                  remove_hashtag(
                   remove_username(
                   stem_word(word)))))))) for word in value.split()]

#Boşlukların silinmesi
def remove_space(value):
    return[item for item in value if item.strip()] #strip kaldırma

#bag of words

def bag_of_words(value):
    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(value)
    return X.toarray().tolist()

#TF-IDF

def tfidf(value):
    vectorizer = TfidfVectorizer()
    X =vectorizer.fit_transform(value)
    return X.toarray().tolist()

#word2vec model

def word2vec(value):
    model = Word2Vec.load("word2vec.model")
    bfr_list = []
    bfr_len = len(value)
    
    for k in value:
        bfr = model.wv.key_to_index[k]
        bfr = model.wv[bfr]
        bfr_list.append(bfr)
        
    bfr_list=sum(bfr_list)
    bfr_list=bfr_list/bfr_len
    return bfr_list.tolist()
