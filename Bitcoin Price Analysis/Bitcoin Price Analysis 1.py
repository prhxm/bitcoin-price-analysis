# -------------------------------
# 📦 Importing Required Libraries
# -------------------------------
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# -------------------------------
# 🧮 Loading and Preprocessing Data
# -------------------------------
df = pd.read_csv("btcusdt.csv", encoding="latin1")
pd.set_option("display.max_row",12220)

#Data Cleaning (Clean column names and values)
df.columns = df.columns.str.strip()
df["Adj Close"] = df["Adj Close"].str.replace(",", "")
df["Adj Close"] = df["Adj Close"].astype(float)
df["Date"] = pd.to_datetime(df["Date"], format='%d-%b-%y')

# -------------------------------
# 📊 Basic Statistical Overview
# -------------------------------
# mean, min, max, STD
print(f"""
Average Price: {df["Adj Close"].mean():.2f}
Minimum Price: {df["Adj Close"].min():.2f}
Maximum Price: {df['Adj Close'].max():.2f}
STD Deviation: {df['Adj Close'].std():.2f}""")

# -------------------------------
# 📈 Daily Percentage Returns
# -------------------------------
df["Daily Return %"] = df['Adj Close'].pct_change().round(4) * 100 

# -------------------------------
# 🧠 Rolling Moving Averages
# -------------------------------
df = df.sort_index(ascending=False)
df["MA 7"] = df["Adj Close"].rolling(window=7).mean().round(2)
df["MA 30"] = df["Adj Close"].rolling(window=30).mean().round(2)
df = df.sort_index(ascending=True)

# -------------------------------
# 📍 Crossover Signal Generation
# -------------------------------
df = df.sort_index(ascending=False)
df["Signal"] = 0
df.loc[df['MA 7'] > df["MA 30"], "Signal"] = 1
df.loc[df['MA 7'] < df["MA 30"], 'Signal'] = -1

# Detect crossover points (for buy/sell signals)
df['Cross Over'] = df['Signal'].diff()    
df = df.sort_index(ascending=True)
Buy_signal = df.loc[df['Cross Over'] == 2]
Sell_signal = df.loc[df["Cross Over"] == -2]


# -------------------------------
# 📈 BTC Line Visualization
# -------------------------------
plt.plot(df['Date'],df['Adj Close'], lw= 2, label= "C-Price")
plt.plot(df['Date'],df['MA 7'], c= "red", lw= 1, label="MA 7")
plt.plot(df['Date'],df['MA 30'], c= "g", lw= 1, label="MA 30")

plt.xlabel("Date")
plt.ylabel("Price")
plt.title("Bitcoin Price Movement")
plt.legend()
plt.grid()
plt.show()

plt.plot(df['Date'],df['Daily Return %'], c= "y", lw= 1, label="Daily Return")
plt.xlabel("Date")
plt.ylabel("Percent %")
plt.legend()
plt.grid()
plt.show()

# -------------------------------
# 🧮 Loading and Preprocessing Data
# -------------------------------
''' 
df = pd.read_csv("Raw XAU.csv", header=None)
df = df.values.reshape(-1,6)
df = pd.DataFrame(df, columns=['Date','Open','High', 'Low', 'Close','Vol'])

df['Date'] = pd.to_datetime(df['Date'])
df['Close'] = df['Close'].astype(float)
df.to_csv("XAU_price.csv")
'''
xdf = pd.read_csv("XAU_price.csv")
XAU_df = pd.DataFrame(xdf)
XAU_df.drop(columns="Unnamed: 0",inplace=True)

# Making New DataFrame of BTC And Gold
XAU_BTC_Corr = XAU_df["Close"] 
XAU_BTC_Corr = pd.DataFrame(XAU_BTC_Corr)
XAU_BTC_Corr['BTC'] = df['Adj Close']
XAU_BTC_Corr.columns = ["XAU", "BTC"]
XAU_BTC_Corr.sort_index(ascending=False,inplace= True)

# -------------------------------
# 🎯 Rolling Correlation with Gold
# -------------------------------
XAU_BTC_Corr['Correlation One-Week'] = XAU_BTC_Corr['BTC'].rolling(window=7).corr(XAU_BTC_Corr['XAU'])
XAU_BTC_Corr['Correlation Four-Week'] = XAU_BTC_Corr['BTC'].rolling(window=28).corr(XAU_BTC_Corr['XAU'])
XAU_BTC_Corr.sort_index(ascending=True,inplace= True)
XAU_BTC_Corr.dropna(inplace=True)
print(XAU_BTC_Corr.head(11))

# -------------------------------
# 🔥 Heatmap Visualization
# -------------------------------
# One week and Four Week correlation of BTC / XAU
plt.plot(df['Date'][:160], XAU_BTC_Corr['Correlation One-Week'], c= 'y', lw=2, label = "Correlation One-Week")
plt.plot(df['Date'][:160], XAU_BTC_Corr['Correlation Four-Week'], c= 'b', lw=2, label = "Correlation Four-Week")

plt.xlabel("Date")
plt.ylabel("Correlation (-1, 1)")
plt.title("Bitcoin and Gold Correlation (One and Four Week)")
plt.legend()
plt.grid()
plt.show()

#BTC XAU Correlation Heatmap
plt.figure(figsize=(12,6))
sns.heatmap(XAU_BTC_Corr[['BTC','XAU']].corr(), annot=True, cmap='YlGnBu',linewidths=0.5, vmin=-1, vmax=1)
plt.show()