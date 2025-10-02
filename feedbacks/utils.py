from textblob import TextBlob

def analisar_sentimento(texto):
    polaridade = TextBlob(texto).sentiment.polarity
    if polaridade > 0.1:
        return 'positivo'
    elif polaridade < -0.1:
        return 'negativo'
    else:
        return 'neutro'
