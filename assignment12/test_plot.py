import pandas as pd
import matplotlib.pyplot as plt

data = pd.DataFrame({
    "x": [1, 2, 3, 4],
    "y": [10, 20, 15, 25]
})

data.plot(x="x", y="y")
plt.title("Simple Plot Test")
plt.show()
  