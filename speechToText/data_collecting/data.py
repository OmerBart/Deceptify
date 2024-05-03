"""File for data generation for the fine-tune process"""
import os

import pandas as pd


# Loading the knowledgebase dataset.
general_script_dir = os.path.dirname(os.path.abspath(__file__))
knowledgebase_filename = general_script_dir + "/knowledgebase.csv"
knowledgebase_df = pd.DataFrame(knowledgebase_filename)
knowledgebase_df = knowledgebase_df.dropna(how='any')

# Data preprocessing
X = knowledgebase_df['Question'].values  # numpy array.
Y = knowledgebase_df['Answer'].values  # numpy array too.

