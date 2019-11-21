[samples, fs] = audioread('c3.wav');
speechObject = speechClient('Google','languageCode','en-US'); 
outInfo = speech2text(speechObject, samples, fs);
outInfo.TRANSCRIPT