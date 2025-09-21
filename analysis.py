import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
df = pd.read_csv("metadata.csv")

# Basic info
print(df.shape)
print(df.info())
print(df.head())