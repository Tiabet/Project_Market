#!/usr/bin/env python
# coding: utf-8

# <a href="https://colab.research.google.com/github/Tiabet/Project_Market/blob/master/text_preprocessing_pipeline.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>

# In[ ]:


import unicodedata
import pandas as pd
from hanspell import spell_checker
import re
import os
import sys
from sklearn.pipeline import Pipeline
from sklearn.base import BaseEstimator, TransformerMixin

def normalize_unicode(text):
    return unicodedata.normalize('NFKC', text)

def correct_spelling(text):
    spelled_sent = spell_checker.check(text)
    return spelled_sent.checked

#def apply_regex(text):
#    only_BMP_pattern = re.compile("["
#        u"\U00010000-\U0010FFFF"  #BMP characters 이외
#                           "]+", flags=re.UNICODE)
#    text = only_BMP_pattern.sub(r'', text)
#    text = re.sub(r'[ㄱ-ㅎㅏ-ㅣ0-9]+', '', text)
#    text = re.sub('ᄒ+', '', text)
#    text = re.sub('[ෆ⃛❤❤❤♥♡】૮₍˶•⑅₎ა]', '', text)
#    text = re.sub('[-=+,#/\?^.@*\";※~ㆍ!』‘|\<\>\[\]\_`\'…》\”\“\’·]', ' ', text)
#    text = re.sub(r':[)D]|:[(]','', text)
#    text = re.sub(r':','', text)
#    text = re.sub(r'[a-zA-Z]{1,2}', '', text)
#    text = re.sub(r'\s{2,}|\t', ' ', text)
#    return text

def apply_regex(text): 
    text = re.sub(r'[^ 가-힣a-zA-Z\(\):]','',text)
    text = re.sub(r'[a-zA-Z]{1,2}', '', text)
    text = re.sub(r':\s?[)D]|:\s?\[', '', text)
    return text

class NormalizeUnicodeTransformer(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self

    def transform(self, X):
        return X.apply(normalize_unicode)

class CorrectSpellingTransformer(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self

    def transform(self, X):
        return X.apply(correct_spelling)

class ApplyRegexTransformer(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self

    def transform(self, X):
        return X.apply(apply_regex)

def preprocess_file(input_filename, output_filename):
    df = pd.read_csv(input_filename, sep='\t')
    

    preprocessing_pipeline = Pipeline([
        ('normalize_unicode', NormalizeUnicodeTransformer()),
        ('correct_spelling', CorrectSpellingTransformer()),
        ('apply_regex', ApplyRegexTransformer()),
        ('correct_spelling_2', CorrectSpellingTransformer())
    ])

    df_preprocessed = preprocessing_pipeline.fit_transform(df['review'])
    df['review'] = df_preprocessed
    df.to_csv(output_filename, sep='\t', index=False)  

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python preprocessing_script.py input.tsv")
    else:
        input_filename = sys.argv[1]
        base_filename, extension = os.path.splitext(input_filename)
        output_filename = base_filename + '_preprocessed' + extension
        preprocess_file(input_filename, output_filename)
