import datetime as dt
import matplotlib.pyplot as plt
import pandas_datareader as web

plt.style.use("dark_background")

# Moving Averages

ma_1 = 20
ma_2 = 50

# Define Time Frame
start = dt.datetime.now() - dt.timedelta(days=365 * 3)
end = dt.datetime.now()

data = web.DataReader('GS', 'yahoo', start, end)
data[f'SMA_{ma_1}'] = data['adj Close'].rolling(window=ma_1).mean()
data[f'SMA_{ma_2}'] = data['adj Close'].rolling(window=ma_2).mean()

data = data.iloc[ma_2:]

plt.plot(data['adj Close'], label="Share Price", color="lightblue")
plt.plot(data [f'SMA_{ma_1}'], label=f"SMA_{ma_1}", color="red")
plt.plot(data [f'SMA_{ma_2}'], label=f"SMA_{ma_2}", color="yellow")
plt.legend(loc="upper left")
plt.show()

# Long/Short Strategy based on MA Crossovers

long_signals = []
short_signals = []
trigger = 0

for x in range(len(data)):
    if data[f'SMA_{ma_1}'].iloc[x] > data[f'SMA_{ma_2}'].iloc[x] and trigger != 1:
        long_signals.append(data['Adj Close'].iloc[x])
        short_signals.append(float('nan'))
        trigger = 1
    elif data[f'SMA_{ma_1}'].iloc[x] < data[f'SMA_{ma_2}'].iloc[x] and trigger != -1:
        long_signals.append(float('nan'))
        short_signals.append(data['Adj Close'].iloc[x])
        trigger = -1
    else:
        long_signals.append(float('nan'))
        short_signals.append(float('nan'))

data['long Signals'] = long_signals
data['Short Signals'] = short_signals


plt.plot(data['adj Close'], label="Share Price", alpha=0.75)
plt.plot(data [f'SMA_{ma_1}'], label=f"SMA_{ma_1}", color="red", linestyle="--")
plt.plot(data [f'SMA_{ma_2}'], label=f"SMA_{ma_2}", color="white", linestyle="--")
plt.scatter(data.index, data['Long Signals'], label="Long Signal", marker="^", color="#00ff00", lw=3)
plt.scatter(data.index, data['Short Signals'], label="Short Signal", marker="v", color="#ff0000", lw=3)
plt.legend(loc="upper left")