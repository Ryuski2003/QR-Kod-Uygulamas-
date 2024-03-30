import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

df = pd.read_csv('StudentsPerformance.csv')

sns.set(style='dark')
sns.violinplot(df, x = 'gender', y = 'math score', hue = 'race/ethnicity')
plt.show()
