
# Convert a FFTBG API unit to a binary array
def standardize_name(s):
  return s.replace(" ", "").replace("-", "").lower()

def api_unit_to_array(unit, tips):
  def get_index(tips, prefix, key):
    if key == "":
      return 0
    v = prefix + "_" + standardize_name(key)
    v = tips[v]
    return int(v)
  
  gender = unit["Gender"]
  job = standardize_name(unit["Class"])

  # hack
  job = (job if job != "Time Mage" else "TimeMage")

  ans = [0]*len(tips)
  ans[0] = 1
  ans[tips["Brave"]] = unit["Brave"]/100.0
  ans[tips["Faith"]] = unit["Faith"]/100.0
  job = "Class_" + standardize_name(job + ("" if gender == "Monster" else unit["Gender"]))
  ans[tips[job]] = 1

  ans[get_index(tips, "Zodiac", unit["Sign"])] += 1

  # abilities
  ans[get_index(tips, "Ability", unit["ReactionSkill"])] += 1
  ans[get_index(tips, "Ability", unit["SupportSkill"])] += 1
  ans[get_index(tips, "Ability", unit["MoveSkill"])] += 1

  skills = unit['ClassSkills']
  for i in range(len(skills)):
    ans[get_index(tips, "Ability", skills[i])] += 1
  skills = unit['ExtraSkills']
  for i in range(len(skills)):
    ans[get_index(tips, "Ability", skills[i])] += 1

  ans[get_index(tips, "Item", unit["Mainhand"])] += 1
  ans[get_index(tips, "Item", unit["Offhand"])] += 1
  ans[get_index(tips, "Item", unit["Head"])] += 1
  ans[get_index(tips, "Item", unit["Armor"])] += 1
  ans[get_index(tips, "Item", unit["Accessory"])] += 1

  return ans

def api_make_feature_dictionary(tips):
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
    ans["Zodiac_" + standardize_name(zd)] = ind
    ind += 1
  for cl in classes:
    ans["Class_" + standardize_name(cl)] = ind
    ind += 1
  for it in items:
    ans["Item_" + standardize_name(it)] = ind
    ind += 1
  for ab in ability:
    ans["Ability_" + standardize_name(ab)] = ind
    ind += 1

  return ans

def api_parse_winners(tournament):
  # "red": 0, "blue": 1, "green": 2, "yellow": 3,
  # "white": 4, "black": 5, "purple": 6, "brown": 7, "champion": 8
  left_side = [-1]*8
  right_side = [-1]*8
  left_won = [-1]*8
  winners = tournament["Winners"]

  # red vs blue
  left_side[0] = 0
  right_side[0] = 1
  left_side[4], left_won[0] = (0, 1) if winners[0] == "red" else (1, 0)

  # green vs yellow
  left_side[1] = 2
  right_side[1] = 3
  right_side[4], left_won[1] = (2, 1) if winners[1] == "green" else (3, 0)
 
  # white vs black
  left_side[2] = 4
  right_side[2] = 5
  left_side[5], left_won[2] = (4, 1) if winners[2] == "white" else (5, 0)   

  # purple v brown
  left_side[3] = 6
  right_side[3] = 7
  right_side[5], left_won[3] = (6, 1) if winners[3] == "purple" else (5, 0)   

  # (red, blue) vs (green, yellow)
  left_side[6], left_won[4] = (left_side[4], 1) if winners[4] == winners[0] else (right_side[4], 0)

  # (white, black) vs (purple, brown)
  right_side[6], left_won[5] = (left_side[5], 1) if winners[5] == winners[2] else (right_side[5], 0)

  # (red, blue, green, yellow) vs (white, black, purple, brown)
  left_side[7], left_won[6] = (left_side[6], 1) if winners[6] == winners[4] else (right_side[6], 0)

  right_side[7] = 8 # champion
  left_won[7] = 0 if winners[7] == "champion" else 1

  return [(left_side[i], right_side[i]) for i in range(8)], left_won
