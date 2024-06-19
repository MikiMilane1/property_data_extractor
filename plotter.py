from matplotlib import pyplot as plt
import matplotlib.ticker as ticker
import pandas as pd

def plotter(df, location, lookback_period):
    plt.plot(df['date'], df['price'])
    plt.xticks(rotation=90, fontsize=10)
    plt.subplots_adjust(bottom=0.25)
    plt.title(f'Real estate price for {location} in the previous {lookback_period} years')
    ax = plt.gca()
    ax.xaxis.set_major_locator(ticker.MaxNLocator(nbins=20))
    plt.xlabel('Date')
    plt.ylabel('EUR/m2')
    plt.show()
