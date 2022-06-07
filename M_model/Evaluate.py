!pip install -qq transformers
import transformers
import pandas as pd
import numpy as np
import torch
from transformers import BertTokenizer
from transformers import BertModel
from transformers import BertTokenizer, TFBertForSequenceClassification
from transformers import InputExample, InputFeatures
import tensorflow as tf
import xlrd
from os import listdiir

model = TFBertForSequenceClassification.from_pretrained("bert-base-uncased")
tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
model.load_weights('/content/gdrive/MyDrive/Test/for_nlp/my_model_weights.h5')

record_data = pd.DataFrame(columns = ['F_name','result'])
from os import listdir
for year in range(2005,2022):
  for Q in ['Q1','Q2','Q3','Q4']:
    f_list = listdir(f'/content/gdrive/MyDrive/Test/for_nlp/{year}/{Q}')
    for d_f in f_list:
      append_list = {}
      if (d_f.split('.')[1]=='csv'):
        try:
          total_score = 0
          data = pd.read_csv(f'/content/gdrive/MyDrive/Test/for_nlp/{year}/{Q}/{d_f}')
          pred_sentences = list(data['Content'])
          tf_batch = tokenizer(pred_sentences, max_length=128, padding=True, truncation=True, return_tensors='tf')
          tf_outputs = model(tf_batch)
          tf_predictions = tf.nn.softmax(tf_outputs[0], axis=-1)
          labels = ['Negative','Positive']
          label = tf.argmax(tf_predictions, axis=1)
          label = label.numpy()
          append_list['F_name'] = f'{year}/{Q}/{d_f}'
          append_list['result'] = (label.sum()-len(label))/len(label)
          record_data = record_data.append(append_list,ignore_index=True)
          record_data.to_csv('/content/gdrive/MyDrive/Test/for_nlp/record_data.csv',index=False)
        except:
          pass
    print(f'{year} {Q} complete!')