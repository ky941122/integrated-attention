# -*- coding: utf-8 -*-
import sys
import os
import torch
import re
from unique_token import Constants
import jieba

# load base path
basePath = os.path.dirname(os.path.realpath(__file__))
workplace = basePath

def seg_sentence(sentence):
    sentence_seged = list(jieba.cut(sentence.strip()))
    return sentence_seged

# load stopwords list
def stopwordslist(filepath):
    stopwords = [line.strip() for line in open(filepath, 'r', encoding='utf-8').readlines()]  
    return stopwords

stopwords = stopwordslist(os.path.join(workplace,"bin","stopwords.txt"))

def text_clean(sentence,keep_list):
    '''
    for this, assume base on a sentence
    '''
    qs_list = []
    for word in seg_sentence(sentence):
        word = re.sub(r':','比',word)
        word = re.sub(r" ","",word)
        word = re.sub("[A-Za-z\[\`\~\!\@\#\$\^\&\*\(\)\=\|\{\}\'\:\;\'\,\[\]\.\<\>\/\?\~\！\@\#\\\&\*\%]", "", word)
        if word == '':
            continue
        if bool(re.search(r'\d',word) and re.search(r'\.',word)) and word not in keep_list:
            keep_list.append(word)
        if word not in keep_list:
            try:
                if not bool(re.search(r'\d',word)):
                    qs_list.append(word.strip())
                elif len(word)>=5:
                    for zimu in word:
                        qs_list.append(alabo2han(zimu).strip())
                else:
                    qs_list += alabo2han(word).split()
            except:
                continue
    return qs_list

num_alabo={'0':'零','1':'一','2':'二','3':'三','4':'四','5':'五','6':'六','7':'七','8':'八','9':'九'}
weishu = {'0':'','1':'十','2':'百','3':'千','4':'万','5':'十万','6':'百万','7':'千万','8':'亿'}

def alabo2han(number):
    if len(number) == 1:
        return num_alabo[number]
    han = ''
    num_len = len(number)
    count = 1
    for digit in number:
        if digit == '0':
            count +=1
            continue
        han += num_alabo[digit]
        han = han + weishu[str(num_len-count)]+' '
        count+=1
    han = re.sub(r"一十万","十万",han)
    return han

class sentence():
    def __init__(self, max_sent_len=30):
        self.max_sentence_len = max_sent_len

    def tokenized(self,text):
        return seg_sentence(text)

    def tokenize_sentence(self,text):
        words_1 = text_clean(text, keep_list=['\n',''])
        if len(words_1) > self.max_sentence_len:
            words_1 = words_1[:self.max_sentence_len]
            #print('trimming sentence 1')
        else:
            words_1 += [Constants.PAD_WORD]*(self.max_sentence_len-len(words_1))
        
        if words_1:
            return words_1
        else:
            return None




