#!/usr/bin/env python
# coding: utf-8

# In[1]:


import nltk
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
import json
import pickle
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation, Dropout
from tensorflow.keras.optimizers import SGD
import random
import json
import sys
import os


# In[10]:

botName = sys.argv[1]
BOTCONFIG_PATH = 'bots/'+botName+'/config/'+botName+'.json'
if not os.path.exists('bots/'+botName+'/models/intents'):
    os.makedirs('bots/'+botName+'/models/intents')


# In[11]:


words=[]
classes = []
documents = []
ignore_words = ['?', '!']
data_file = open(BOTCONFIG_PATH).read()
botdata = json.loads(data_file)
intent = botdata['intents']


# In[12]:


intent


# In[13]:


for pattern in intent:
    for sentence in pattern['patterns']:
        w = nltk.word_tokenize(sentence)
        words.extend(w)
        documents.append((w, pattern['journeyName']))
        if pattern['journeyName'] not in classes:
            classes.append(pattern['journeyName'])
print("words >> ", words, "documents >> ", documents, "classes >> ", classes)


# In[14]:


# lemmaztize and lower each word and remove duplicates
words = [lemmatizer.lemmatize(w.lower()) for w in words if w not in ignore_words]
words = sorted(list(set(words)))
print("words >> ", words)


# In[15]:


# sort classes
classes = sorted(list(set(classes)))
# documents = combination between patterns and intents
print (len(documents), "documents")
# classes = intents
print (len(classes), "classes", classes)
# words = all words, vocabulary
print (len(words), "unique lemmatized words", words)


# In[16]:


pickle.dump(words,open('bots/'+botName+'/models/intents/words.pkl','wb'))
pickle.dump(classes,open('bots/'+botName+'/models/intents/classes.pkl','wb'))


# In[17]:


# create our training data
training = []
# create an empty array for our output
output_empty = [0] * len(classes)


# In[18]:


# training set, bag of words for each sentence
for doc in documents:
    # initialize our bag of words
    bag = []
    # list of tokenized words for the pattern
    pattern_words = doc[0]
    # lemmatize each word - create base word, in attempt to represent related words
    pattern_words = [lemmatizer.lemmatize(word.lower()) for word in pattern_words]
    # create our bag of words array with 1, if word match found in current pattern
    for w in words:
        bag.append(1) if w in pattern_words else bag.append(0)
    
    # output is a '0' for each tag and '1' for current tag (for each pattern)
    output_row = list(output_empty)
    output_row[classes.index(doc[1])] = 1
    
    training.append([bag, output_row])
print ("training >> ", training)


# In[19]:


# shuffle our features and turn into np.array
random.shuffle(training)
training = np.array(training)
# create train and test lists. X - patterns, Y - intents
train_x = list(training[:,0])
train_y = list(training[:,1])
print("Training data created")


# In[20]:


# Create model - 3 layers. First layer 128 neurons, second layer 64 neurons and 3rd output layer contains number of neurons
# equal to number of intents to predict output intent with softmax
model = Sequential()
model.add(Dense(128, input_shape=(len(train_x[0]),), activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(len(train_y[0]), activation='softmax'))


# In[21]:


# Compile model. Stochastic gradient descent with Nesterov accelerated gradient gives good results for this model
sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])


# In[22]:


#fitting and saving the model 
hist = model.fit(np.array(train_x), np.array(train_y), epochs=200, batch_size=5, verbose=1)
model.save('bots/'+botName+'/models/intents/primaryintent_model.h5', hist)


# In[ ]:




