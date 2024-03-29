import numpy as np
import operator
from collections import Counter
import FUNCIONES as pj
import LETRAS as lts
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.metrics import euclidean_distances
from scipy.spatial import distance_matrix
from sklearn import manifold
#-----------------------------------------------------------------------------
from gensim import corpora, models
from gensim.utils import simple_preprocess
from gensim.parsing.preprocessing import STOPWORDS
from nltk.stem import WordNetLemmatizer, SnowballStemmer
from nltk.stem.porter import *
import numpy as np
np.random.seed(2018)
import nltk
#-----------------------------------------------------------------------------                               
#pj.ModAudioR('hooa')
from time import time #importamos la función time para capturar tiempos  
#entrada = pj.vozToText("r1.mp3")
def BuscarCancion(path):
    tiempo_inicial = time() 
    audio=[]
    entrada = pj.vozToText(path)
    entrada2 = list(entrada.split())
    query = pj.npl2(entrada2)
    freqT = query[1]
    query = query[0]
    audio.append(freqT)
    audio.append(query)
    top=[]
    urls = lts.Load()
    ide=0
    bow=[]
    for u in urls:
            cw = pj.sendCrawlers(u)
            name = cw[0]
            doc = cw[1]
            doc = pj.clear(doc)
            doc = doc.split()
            ide=ide+1
            fc = pj.frecuencia(query,doc)
            bow.append(fc) #BOLAS DE PALABRAS <----

    for b in range(len(bow)):
            t = query #Terminos de la consulta   
            v = freqT#frecuencia del termino en la consulta
            v2 = pj.inDocument(bow) #numero de documentos en los que se repite
            v3 = bow[b]#fecuencia del termino en el documento
            tif = pj.Metodotf(t,v,v2,v3,len(bow))
            t1 = tif[1]
            top.append(t1)
    dicio={}
    for t in range(len(top)):
            dicio[t]=top[t]
    resultado = sorted(dicio.items(), key=operator.itemgetter(1),reverse=True)
    rankin=[]
    topurls=[]
    resu=[]
    for ans in range(len(resultado)):
        posi = resultado[ans][0] 
        resu.append(resultado[ans][1])
        cw2 = pj.sendCrawlers(urls[posi])
        name = cw2[0]
        ur = cw2[2]
        rankin.append(name)
        topurls.append(ur)
    a = ""
    recomendadas = []
    nf = pj.Suma(resu)
    if nf != 0:
        lim=len(rankin)
        for rak in range(lim):    
            if resultado[rak][1] != 0:
                a = str(rak+1)+') '+rankin[rak]
                b = str(resultado[rak][1])+"%"
                aux0 = [[a],[b],[topurls[0]],[audio]]
                recomendadas.append(aux0)
        pj.recommend(rankin[0])        
        tiempo_final = time() 
        tiempo_ejecucion = tiempo_final - tiempo_inicial
        print ('\n\nEl tiempo de ejecucion fue:',tiempo_ejecucion," segundos") #En segundos
    return recomendadas






