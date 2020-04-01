import pandas as pd
import matplotlib.pyplot as plt
import pathlib
print(pathlib.Path().absolute())


def EMA(samples, n, index):
    alfa = 2 / (n + 1)
    numerator = samples[index]
    denominator = 1
    for i in range(1, n + 1):
        numerator += ((1 - alfa) ** (i)) * samples[index - i]
        denominator += ((1 - alfa) ** (i))
    return numerator / denominator


# WIG20 values
stock_data = pd.read_csv('wig20_d.csv')
stock_data = stock_data.head(1000)

stock_df = pd.DataFrame()
stock_df['data'] = stock_data['Data']
stock_df['value'] = stock_data['Zamkniecie']
prices = stock_df['value'].to_list()

DAYS = [i for i in range(1000)]
MACD = [0] * 1000
SIGNAL = [0] * 1000
# calculating MACD and SIGNAL
for i in range(26, 1000):
    MACD[i] = EMA(prices, 12, i) - EMA(prices, 26, i)
    if(i >= 35):
        SIGNAL[i] = EMA(MACD, 9, i)

# analyse of game
budget = 10000
stocks = 0
last_difference = 0
for i in range(35, 1000):
    difference = MACD[i] - SIGNAL[i]
    if difference < 0 and last_difference > 0 and stocks > 0:
        budget += prices[i]
        stocks -= 1
    if difference > 0 and last_difference < 0 and budget > prices[i]:
        budget -= prices[i]
        stocks += 1
    last_difference = difference
print(stocks, budget, prices[999], sep=' ')

# own algorithm
# idea is same, but now after unprofitable transactions we buy more stocks
budget = 10000
stocks = 0
purchase_price = 0
multiplier = 0.3  # tells what part of stock we should buy
last_difference = 0
for i in range(35, 1000):
    difference = MACD[i] - SIGNAL[i]
    if difference < 0 and last_difference > 0 and stocks > 0:
        budget += prices[i] * multiplier
        stocks -= multiplier
        if prices[i] < purchase_price:
            multiplier *= 2
        else:
            multiplier = 0.1

    if difference > 0 and last_difference < 0 and budget > prices[i]:
        budget -= prices[i] * multiplier
        stocks += multiplier
        purchase_price = prices[i]
    elif difference > 0 and last_difference < 0 and budget < prices[i]:
        multiplier /= 2
    last_difference = difference
print(stocks, budget, prices[999], sep=' ')


plt.figure(1)
plt.plot(DAYS, MACD, label='macd', color='red')
plt.plot(DAYS, SIGNAL, label='signal', color='blue')
plt.title("MACD")
plt.ylabel("macd and signal values")
plt.xlabel("days")
plt.legend(loc="upper left")

plt.figure(2)
plt.plot(DAYS, prices, label='prices', color='green')
plt.title("Prices")
plt.ylabel("WIG20 close values")
plt.xlabel("days")
plt.legend(loc="upper left")
plt.show()
