#!/bin/bash
java -mx1000m -cp /app/stanford-ner-2018-02-27/stanford-ner.jar edu.stanford.nlp.ie.NERServer -loadClassifier /app/stanford-ner-2018-02-27/classifiers/english.all.3class.distsim.crf.ser.gz -port 8888 -outputFormat inlineXML &
sleep 5
gunicorn --bind :$PORT --workers 1 --threads 3 main:app --timeout 90
