"""
java -mx1000m -cp stanford-ner.jar edu.stanford.nlp.ie.NERServer -loadClassifier classifiers/english.all.3class.distsim.crf.ser.gz -port 8888 -outputFormat inlineXML
"""
import subprocess
import ner
import sys
import os
import time
       
from nltk.tag import StanfordNERTagger


tagger = None
p = None

def start_classifier():
    global tagger
    global p
    tagger = ner.SocketNER(host='localhost', port=8888)
    try:
        tagger.get_entities("just a test")
        return
    except:
        pass
    DETACHED_PROCESS = 0x00000008
    #if stanford-ner.jar is already running, it's ok, this will just exit nicely
    p = subprocess.Popen(["java", "-mx1000m", "-cp",
                                "stanford-ner.jar",
                                "edu.stanford.nlp.ie.NERServer",
                                "-loadClassifier", "classifiers/english.all.3class.distsim.crf.ser.gz",
                                "-port", "8888",
                                "-outputFormat", "inlineXML"], 
                                cwd=os.path.join(os.getcwd(),"stanford-ner-2018-02-27"),
                                creationflags=DETACHED_PROCESS,shell=True)
    time.sleep(3)


def stop_classifier():
    global p
    try:
        #this will fail if p wasn't set (above) because stanford-ner.jar was already running
        p.stop
    except:
        pass


def tag(text, org_filter=None):
    global tagger
    
    tagged = []

    if not text:
        return tagged

    if type(text) is list:
        text = " ".join(text)
    
    if not tagger:
        start_classifier()

    classified_text = tagger.get_entities(text)

    return classified_text
