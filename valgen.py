import sys
import numpy as np
import pandas as pd


import random
NO_PREFERENCE = 2

def get_args(arg, categories, slang_choice):
  cats = []
  slang = NO_PREFERENCE
  for i in range(len(arg)):
    num = int(arg[i])
    if i < NO_PREFERENCE and num <= NO_PREFERENCE:
      if categories[num] not in cats:
        cats.append(categories[num])
    elif i >= NO_PREFERENCE and int(arg[i]) < NO_PREFERENCE:
      slang = int(slang_choice[num])
  return (cats, slang)

def get_valentine(df, cats = [], slang = NO_PREFERENCE):
  cond1 = (df['Category_1'].isin(cats)) | (df['Category_2'].isin(cats))
  if (cats and 'No preference' not in cats):
    df = df[cond1]
  if (slang < NO_PREFERENCE):
    cond2 = (df['Is_slang'] == slang)
    df = df[cond2]
  return random.choice(list(df['Name']))


def get_values(df, col):
  l = list(df[col].value_counts().index)
  l.append('No preference')
  return l

#### MAIN FUNCTION SORTA ###
valentines = pd.read_csv("valentines.txt", sep = ',', on_bad_lines = 'skip')
valentines['Is_slang'] = np.where(valentines['Is_slang'] == 0, False, True)
categories = get_values(valentines, 'Category_1')
slang_choice = get_values(valentines, 'Is_slang')

(cats, slang) = ([], NO_PREFERENCE)
if len(sys.argv) > 1:
  (cats, slang) = get_args(sys.argv[1], categories, slang_choice)
valentine = get_valentine(valentines, cats, slang)
print(valentine)
