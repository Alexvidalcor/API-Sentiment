
import nltk
nltk.download('punkt')
nltk.download('vader_lexicon')


from nltk.corpus import stopwords
nltk.corpus.stopwords.words("spanish")

from nltk.tokenize import RegexpTokenizer
from nltk.tokenize import sent_tokenize

from nltk.sentiment.vader import SentimentIntensityAnalyzer
sia = SentimentIntensityAnalyzer()

from textblob import TextBlob

import goslate
gs = goslate.Goslate()



def transText(textList):

    try:
        for element in textList:
            languageDetection = gs.detect(f"{element}")
            if languageDetection == "es":
                break
            elif languageDetection =="en":
                return textList    
    except:
        return False
        
    if languageDetection == "es":
        try:
            translated = [gs.translate(f"{element}", 'en') for element in textList]
            return translated
        except:
            return False


def tokenize(text):
    result = []
    for element in text:
        words = nltk.word_tokenize(f"{element}")

        tokenizer = RegexpTokenizer(r'\w+')
        tokens = tokenizer.tokenize(element)

        stop_words = set(stopwords.words('spanish'))
        tokens_clean = [e for e in tokens if e not in stop_words]
        result.append(tokens_clean)
    
    joinedResult =[value for element in result for value in element]

    return joinedResult


def sentimentAnalysis(text):
    
    analysis = [sia.polarity_scores(element) for element in text]

    negative = sum([element["neg"] for element in analysis])
    positive = sum([element["pos"] for element in analysis])
    neutral = sum([element["neu"] for element in analysis])

    return {"Positivo":positive, "Negativo":negative, "Neutral":neutral}

def objectiveAnalysis(text):
    pos_count = 0
    pos_correct = 0

    neg_count = 0
    neg_correct = 0
    for element in text:
        analysis = TextBlob(f"{element}")
        eng=analysis.translate(to='en')
        
        if eng.sentiment.polarity > 0:
            pos_correct += 1
        pos_count +=1
            
        if eng.sentiment.polarity <= 0:
            neg_correct += 1
        neg_count +=1

    calcPos = pos_correct/pos_count*100.0
    calcNeg = neg_correct/neg_count*100.0

    Positividad = f"Impacto positivo = {calcPos}% con {pos_count} ejemplos"
    Negatividad = f"Impacto negativo = {calcNeg}% con {neg_count} ejemplos"

    return (Positividad, Negatividad)