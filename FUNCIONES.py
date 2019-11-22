from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
import nltk
from nltk.corpus import stopwords
from nltk import SnowballStemmer
from collections import Counter
from nltk import SnowballStemmer
import numpy as np
from playsound import playsound
from gtts import gTTS
from playsound import playsound
import speech_recognition as sr
import os
from scipy import spatial
recognize = sr.Recognizer()
#Funciones
from nltk.tokenize import RegexpTokenizer
from stop_words import get_stop_words
from nltk.stem.porter import PorterStemmer
from gensim import corpora, models
import random
import gensim
from nltk import WordNetLemmatizer
import LETRAS as lts
#===========================R EN PYTHON=======================================
from rpy2.robjects import r
from rpy2.robjects.packages import importr
#=============================================================================


def DCoseno(v1,v2):
    result = 1-spatial.distance.cosine(v1, v2)
    if np.isnan(result):
        result = 1
    return result

def Rmusic(music):
    importr('tuneR')
    r('r <- readMP3("C:/Users/Usuario/Desktop/ProyectoML/canciones/'+music+'")')
    r('writeWave(r,"C:/Users/Usuario/Desktop/ProyectoML/canciones/tmp.wav",extensible=FALSE)')


def vozToText(path):
    t=[]
    b=""
    ext = path[len(path)-3:len(path)]
    if ext == 'mp3':
        Rmusic(path)
        audioFile = 'canciones/tmp.wav'
    if ext == 'wav':
        audioFile = 'canciones/'+path
    if ext == 'txt':
        archivo = open('canciones/'+path)     
        for a in archivo:
            b = b + a
        return b
    if ext != 'mp3':
        if ext != 'wav':
            print('Audio no valido')
            return None
    with sr.AudioFile(audioFile) as source:
        print("Empezando a escuchar")
        audio = recognize.record(source)
        print("Procesando...")
    try:
        text = recognize.recognize_google(audio)
        t = text
        print(t)
        return t
    except Exception as e:
        print("No se pudo entender la cancion")
        print (e)
    

def clear(documento):
    texto = ''
    texto = texto + re.sub('[\'-.,"!@#$]', '', str(documento).lower())
    return texto

def npl2(documentos):
    corpus=[]
    salida=[]
    aux=[]
    salida2=[]
    for text in range(len(documentos)):
        corpus.append(re.sub('[.,"!@#$]', '', documentos[text].lower()))
    n4 = stopwords.words('english')
    for word in corpus:
        if word in n4:
            corpus.remove(word)
    stemmer=SnowballStemmer('english')
    n6 = []
    for w in corpus:
        n5 = stemmer.stem(w)
        n6.append(n5)
    dic = dict(Counter(n6))
    for d in dic.items():
        aux.append(d[1])
    for s in dic.keys():
        salida.append(s)
    salida2 = [salida,aux]
    return salida2

def npl(documentos):
    corpus=[]
    salida=[]
    for text in range(len(documentos)):
        corpus.append(re.sub('[.,"!@#$]', '', documentos[text].lower()))
    n4 = stopwords.words('english')
    for word in corpus:
        if word in n4:
            corpus.remove(word)
    stemmer=SnowballStemmer('english')
    n6 = []
    for w in corpus:
        n5 = stemmer.stem(w)
        n6.append(n5)
    dic = dict(Counter(n6))
    for s in dic.keys():
        salida.append(s)
    return salida

def sendCrawlers(url):
    dat = []
    tit_cancion = 'Not found'
    file = urlopen(url)
    html=file.read()
    file.close()
    tit=[]
    soup = BeautifulSoup(html,"html.parser")
    busca = soup.find_all('h1')
    tit = str(busca)
    a0 = tit.replace(tit[0:47],'')
    b0 = a0.replace(tit[-6:-1],'')
    tit_cancion = b0.replace(tit[-1],'')

    lyc =[]
    for links in soup.find_all('pre'):
        lyc.append(links)
    corp=[]
    for l in lyc:
        for k in l:
            k = str(k)
            if k[0] != '<':    
                k = k.replace('\r\n',' ')
                corp.append(k)
    aux=[]
    doc = []
    for c in corp:
        aux = aux + c.split()
        doc = npl2(aux)
    dat = [tit_cancion,doc[0],url,doc[1]]
    return dat

def sendCrawlers2(url):
    file = urlopen(url)
    html=file.read()
    file.close()
    soup = BeautifulSoup(html,"html.parser")
    lyc =[]
    for links in soup.find_all('pre'):
        lyc.append(links)
    corp=[]
    for l in lyc:
        for k in l:
            k = str(k)
            if k[0] != '<':    
                k = k.replace('\r\n',' ')
                corp.append(k)
    return corp
    
def recommend(songName):
    try:
        os.remove("canciones/rec.mp3")
        os.remove("canciones/rec2.mp3")
    except:
        print() 
    tts = gTTS(songName, lang='en-US')
    tts.save("canciones/rec.mp3")
    tts = gTTS('La canción es:', lang='es-us')
    tts.save("canciones/rec2.mp3")
    playsound('canciones/rec2.mp3')
    playsound('canciones/rec.mp3')



def frecuencia(terms,doc):
    v=[]
    i=0
    for t in terms:
        for d in doc:
            if t.__eq__(d):
                i = i + 1
        v.append(i)
        i=0
    return v
                
def Suma(v):
    a=0
    for i in v:
        a = a + i
    return a

def Metodotf(term,v,v2,v3,N):
    i=0
    z=0
    salida=[]
    res=[]
    
    #print('\t\t\t\tConsulta\t\t\t Documento')
    #print('TERM \t','tfi,q\t','pesado(tfi,q)\t','dfi\tidfi\tWi,q\tfi,d\tpesado(tfi,d)\tWi,d')
    for n in v:
        tf1 = tf(n)
        idf1=idf(N,v2[i])
        tf2 = tf(v3[i])
        tfidf=round(tf2*idf1,2)
        wi = tf1*idf1
        salida.append(wi)
        if tf1 != 0:
            if tf2 != 0:
                z = z + tfidf
        #print(term[i],'\t',v[i],'\t',tf1,'\t\t', v2[i],'\t', idf1,'\t',wi,'\t',v3[i],'\t',tf2,'\t\t',tfidf)
        i=i+1
        res=[salida,round(z,2)]
    return res
   #----- 

def tf(num):
    if num != 0:
        ans = (1+np.log10(num))
    else:
        ans = 0
    return round(ans,2)

def idf(N,num):
    if num != 0:
        ans = np.log10(N/num)
    else:
        ans = 0
    if ans==float('inf'):
        return 0
    return round(ans,2)

def inDocument(bow):
    cnt=0
    ndoc=[]
    for b in range(len(bow[0])):
        for b2 in bow:
            if b2[b] != 0:
                cnt=cnt+1
        ndoc.append(cnt)
        cnt=0    
    return ndoc
            
#*********   

##Topic model         
def lemmatize_stemming(text):
    stemmer=SnowballStemmer('english')
    return stemmer.stem(WordNetLemmatizer().lemmatize(text, pos='v'))
def preprocess(text):
    result = []
    for token in gensim.utils.simple_preprocess(text):
        if token not in gensim.parsing.preprocessing.STOPWORDS and len(token) > 3:
            result.append(lemmatize_stemming(token))
    return result

def Comparacion(url,query):
    try:
        q = query[0][0]
        ur = sendCrawlers(url[0])
        if len(q)<len(ur[3]):
            dif = len(ur[1]) - len(query[0][0])
            for i in range(dif):
                q.append(0)
        similitud = DCoseno(q,ur[3])
        similitud = round(similitud,2)
        print(similitud)
        if similitud > 0.9:
            return query
        if similitud < 0.9:
            return url
    except:
        return url

def topicM(url):
    #Paso 1: Tokenizar y se eliminan palabras vacias
    #Paso 2: Se eliminan palabras que tienen menos de 3 caracteres
    #Paso 3: Todas las palabras vacias se eliminan
    #Paso 4: Se lematiza 
    #Paso 5: Se deriva la palabra a su raiz(Snowball)
    doc2=[]
    doc = sendCrawlers2(url)
    line=""
    for d in doc:
        line = line +d
    doc2.append(line)
    texto = preprocess(doc2[0])
    texto = [texto]
    dictionary = corpora.Dictionary(texto)
    corpus = [dictionary.doc2bow(text) for text in texto]
    ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=3, id2word = dictionary, passes=20)
    ld = ldamodel.print_topics(num_topics=3, num_words=3)
    return ld


def topicM2(text):
    #Paso 1: Tokenizar
    #Paso 2: Se eliminan palabras que tienen menos de 3 caracteres
    #Paso 3: Todas las palabras vacias se eliminan
    #Paso 4: Se lematiza 
    #Paso 5: Se deriva la palabra a su raiz(Snowball)
    doc2=[]
    doc = text
    line=""
    for d in doc:
        line = line +d
    doc2.append(line)
    texto = preprocess(doc2[0])
    texto = [texto]
    dictionary = corpora.Dictionary(texto)
    corpus = [dictionary.doc2bow(text) for text in texto]
    ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=3, id2word = dictionary, passes=20)
    ld = ldamodel.print_topics(num_topics=3, num_words=3)
    return ld





def gettopic(topic):
    import re
    import numpy as np
    tx=[]
    for t in topic:
        tx.append(re.sub(r'\d','',t[1]))
    tx2=[]
    for t in tx:
        c = re.sub('[.,"*!@#$ ]', '', t)                  
        c=c+"+"
        tx2.append(c)
    aux=""
    sa=[]
    for c in tx2:
        for r in c:
            aux = aux + r
            if r == "+":
                sa.append(aux)
                aux=""
    palabras = []
    md2=[]
    for s in sa:
        palabras.append(s.replace("+",""))
    
    div = np.sqrt(len(palabras))
    div = int(div)
    
    for i in range(div):
        md2.append(palabras[(i*div):(i*div+div)])  
    return md2




def PosibleTitulo(b):
    posibles=[]
    ver = lts.getVerbos()
    pro = lts.getPronombres()
    art = lts.getArticulos()
    verbo=[]
    complemento=b
    comp=[]
    
    
    for p in b:
        for p2 in p:
            for v in ver:
                if p2 == v:
                    verbo.append(p2)
    for p in complemento:
        for v in verbo:
            try:
                p.remove(v)
            except:
                print("",end="")
    print()
    for c in complemento:
        for c2 in c:
            comp.append(c2)
           
    for i in range(3):
        posible = pro[random.randrange(len(pro))]+" "+verbo[random.randrange(len(verbo))]+" "+art[random.randrange(len(art))]+" "+comp[random.randrange(len(complemento))]
        posibles.append(posible)
    return posibles
    







