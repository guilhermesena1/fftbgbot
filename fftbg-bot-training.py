# -*- coding: utf-8 -*-
"""
Created on Fri Dec 27 22:27:32 2024

@author: Alexa
"""

#from keras import *
import json
import pandas as pd
import numpy as np
import os

def get_index(tips, prefix, key):
  if key == "":
    return 0
  v = prefix + "_" + key.replace(" ", "_")
  v = tips[v]
  return int(v)

def fix_job(job):
  return job.replace(" ", "")


def unit_to_array(unit, tips):
  gender = unit["Gender"]
  job = fix_job(unit["Class"])

  # hack
  job = (job if job != "Time Mage" else "TimeMage")

  ans = [0]*len(tips)
  ans[0] = 1
  ans[tips["Brave"]] = unit["Brave"]/100.0
  ans[tips["Faith"]] = unit["Faith"]/100.0
  job = "Class_" + job + ("" if gender == "Monster" else  "_" + unit["Gender"])
  ans[tips[job]] = 1

  ans[get_index(tips, "Zodiac", unit["Sign"])] = 1

  # abilities
  ans[get_index(tips, "Ability", unit["ReactionSkill"])] = 1
  ans[get_index(tips, "Ability", unit["SupportSkill"])] = 1
  ans[get_index(tips, "Ability", unit["MoveSkill"])] = 1

  skills = unit['ClassSkills']
  for i in range(len(skills)):
    ans[get_index(tips, "Ability", skills[i])] = 1
  skills = unit['ExtraSkills']
  for i in range(len(skills)):
    ans[get_index(tips, "Ability", skills[i])] = 1

  ans[get_index(tips, "Item", unit["Mainhand"])] = 1
  ans[get_index(tips, "Item", unit["Offhand"])] = 1
  ans[get_index(tips, "Item", unit["Head"])] = 1
  ans[get_index(tips, "Item", unit["Armor"])] = 1
  ans[get_index(tips, "Item", unit["Accessory"])] = 1

  return ans


team_to_index = {
  "red": 0,
  "blue": 1,
  "green": 2,
  "yellow": 3,
  "white": 4,
  "black": 5,
  "purple": 6,
  "brown": 7,
  "champion": 8
}


def make_feature_dictionary(tips):
  BRAVE_INDEX = 1
  FAITH_INDEX = BRAVE_INDEX + 1
  ans = {}

  ans[""] = 0
  ans["Brave"] = BRAVE_INDEX
  ans["Faith"] = FAITH_INDEX

  ind = FAITH_INDEX + 1
  classes = tips["Class"]
  items = tips["Item"]
  ability = tips["Ability"]
  zodiac = tips["Zodiac"]

  for zd in zodiac:
    ans["Zodiac_" + zd.replace(" ", "_")] = ind
    ind += 1
  for cl in classes:
    ans["Class_" + cl.replace(" ", "_")] = ind
    ind += 1
  for it in items:
    ans["Item_" + it.replace(" ", "_")] = ind
    ind += 1
  for ab in ability:
    ans["Ability_" + ab.replace(" ", "_")] = ind
    ind += 1

  return ans

with open("tips.json", "r") as f:
  tips = make_feature_dictionary(json.load(f))

with open("tournaments/1735334091607.json", "r") as f:
  tournament = json.load(f)

team_matrices = np.zeros((9, 4, len(tips)))
teams = tournament["Teams"]
for team in teams:
  the_team = teams[team]["Units"]
  team_matrices[team_to_index[team]] = np.array([unit_to_array(the_team[i], tips) for i in range((len(the_team)))])

print(team_matrices)
