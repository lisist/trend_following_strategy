import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv("result.csv",index_col="Date",parse_dates=True)

plt.plot(data['pnl'])
plt.show()