# -*- coding: utf-8 -*-
"""
Created on Fri Dec 27 22:27:32 2024

@author: Alexa
"""

#from keras import *
import json
import numpy as np
import os
from apiparse import *
from model import *
from tqdm import tqdm

# less verbose tensorflow
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

team_to_index = {"red": 0, "blue": 1, "green": 2, "yellow": 3, "white": 4, "black": 5, "purple": 6, "brown": 7, "champion": 8}

# parse JSON files
with open("tips.json", "r") as f:
  tips = api_make_feature_dictionary(json.load(f))
NUM_FEATURES = len(tips)
X, y = [], []

tournaments = os.listdir("tournaments")

# flatten that puts similar features next to each other
def prepare_input(x):
    return x.transpose().flatten()

model = get_fftbg_model()
print(model.summary())
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

for i in tqdm(range(len(tournaments))):
  with open("tournaments/" + tournaments[i], "r") as f:
    tournament = json.load(f)

  if len(tournament["Winners"]) != 8:
    continue
  team_matrices = np.zeros((9, 4*NUM_FEATURES))
  teams = tournament["Teams"]
  for team in teams:
    the_team = teams[team]["Units"]
    team_matrices[team_to_index[team]] = prepare_input(np.array([api_unit_to_array(the_team[i], tips) for i in range((len(the_team)))]))
  
  team_pairs, team_y = api_parse_winners(tournament)

  for i in range(8):
    X.append(
      np.vstack((team_matrices[team_pairs[i][0]], team_matrices[team_pairs[i][1]])).
      transpose().
      astype('float32')
    )
    y.append(team_y[i])


X = np.array(X).astype('float32')
y = np.array(y)
shuf = np.random.permutation(X.shape[0])
X = X[shuf]
y = y[shuf]
print(X.shape)
print(y.shape)
print(y.sum())

# train model
model.fit(X, y, batch_size = 128, validation_split=0.1, epochs = 20)
pr = model.predict(X)