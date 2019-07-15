import os
import re
import sys
import csv

import glob
import nltk

import ntpath
import gensim
import context
import logging

from esgtopic import ESGTopic
from esgtopic import ESGTokenKey
from esgtopickey import ESGTopicKey

import numpy as np
import pandas as pd

from gensim.utils import simple_preprocess
from gensim.parsing.preprocessing import STOPWORDS

from nltk.stem import WordNetLemmatizer, SnowballStemmer
from nltk.stem.porter import *

'''configures file logging for error and debug info'''
def initLogger():
    logging.basicConfig(filename='logfile.log', level=logging.WARNING, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
    logging.basicConfig(filename='errorfile.log', level=logging.ERROR, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')


'''remotely downloads nltk.wordnet -- requires network connection'''
def loadPackages():
    nltk.download('wordnet')


''':returns list of file paths of raw .txt's '''
def loadPaths():
    workingDir = os.path.dirname(os.path.realpath(__file__))
    print(f'Working directory: {workingDir}')

    rawFilesDir = os.path.join(workingDir,'extern')
    print(f'External data directory: {rawFilesDir}')
    
    dirFiles = [os.path.join(rawFilesDir, x) for x in os.listdir(rawFilesDir)]
    print(f'Data files found: {dirFiles}')

    return dirFiles

def writeTokensToFile(company, year, tokens, filePath):
    for token in tokens:
        row = [company, year, token.token, str(token.count)]
        with open('tokenCounts.csv', encoding='utf-8', mode='a') as outputCsv:
            print(f'Output row: {row}')
            writer = csv.writer(outputCsv)
            writer.writerows(row) 

''':returns tokens in first person and present tense only'''
def lemmatize_stemming(text):
    stemmer = SnowballStemmer('english')
    lemmatizer = stemmer.stem(WordNetLemmatizer().lemmatize(text, pos='v'))
    return lemmatizer

''' :returns list of invariant, lowercase tokens of at least 3 characters and lemmatized '''
def preprocess(text):
    result = []
    for token in gensim.utils.simple_preprocess(text):
        if token not in gensim.parsing.preprocessing.STOPWORDS and len(token) > 2:
            result.append(lemmatize_stemming(token))
    return result

''' :returns each topic in a company's report along with their frequency as a list of ESGTopic'''
def countTopics(topicKey, topics):
    wordMap = dict()
    
    for topic in topics:
        key = ESGTokenKey(topicKey.company, topicKey.year, topic.token)
        if key in wordMap:
            logging.debug(f'Found {topic} in word bag. Incrementing count...')
            wordMap[key].inc()
            logging.debug(f'New count: {wordMap[key].count}')
        else:
            logging.debug(f'New word bag entry: {topic}')
            topic.inc()
            wordMap[key] = topic

    logging.debug(f'{topicKey.company} {topicKey.year} unique topics: {len(wordMap)}')
    return list(wordMap.values())


if __name__ == '__main__':

    context.create(dbName="reports")

    allWords = []
    topicMap = dict()
    paths = loadPaths()

    for filePath in paths:

        print (f'\r\nPre-Processing {filePath}\r\n')

        with open(filePath, encoding='utf-8', mode='r') as file:
            rawText = file.read()
            tokens = preprocess(rawText)
            print(f'\r\nTokenized. Prepare DB record.\r\n')

            fileName = ntpath.basename(filePath)
            print(f'Base file name: {fileName}')

            try:
                fileKeys = fileName.split(' ')
                year = fileKeys[0]
                company = fileKeys[1].split('.')[0]
            except Exception as ex:
                logging.exception(f"Error parsing file name to key {fileName}\r\n{ex}")

            key = ESGTopicKey(company, int(year))
            
            topics = countTopics(key, [ESGTopic(company, year, t) for t in tokens])
            topicMap[key] = topics
            
            logging.debug(f"{company} {year} entry created with {len(topicMap[key])} entries")
            logging.debug(f'Company: {company} Year: {year}\r\n\r\nInserting records to db')

            #context.insertTokens(company, year, topics)
            writeTokensToFile(company, year, topics, 'tokenCount.csv')

    print("Done")