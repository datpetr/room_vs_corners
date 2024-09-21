import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# lets create a pandas DataFrame with some dummy data
data = {'model': ['A', 'B', 'C', 'D', 'E'],
        'inference_speed': [1000, 800, 300, 600, 900],
        'accuracy': [70., 80., 90., 85., 65.]}
df = pd.DataFrame(data)

# set the weights for the score calculation
# weight for accuracy
w1 = 0.7
# weight for inference_speed
w2 = 0.3

# calculate the score for each model, make sure they have similar scale
df['score'] = (w1 * (df['accuracy'] / np.max(df['accuracy']))
               + w2 * (df['inference_speed'] / np.max(df['inference_speed'])))

# create a scatter plot with the score as the point size, scale by 10 to make it more pronounced!
plt.scatter(df['inference_speed'], df['accuracy'], s=100*df['score'])

# add a title and axis labels
plt.title('Model Performance')
plt.xlabel('Inference Speed (samples/sec)')
plt.ylabel('Accuracy')

# add annotations for each model
for i, row in df.iterrows():
    plt.annotate(row['model'], (row['inference_speed'], row['accuracy']))

# show the plot
plt.show()
