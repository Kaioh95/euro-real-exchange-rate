"""
Author: Kaio Henrique de Sousa
Date: May 2022
"""

import logging
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import style
# %matplotlib inline

#config logging
logging.basicConfig(
    filename='./results.log',
    level=logging.INFO,
    filemode='w',
    format='%(name)s - %(levelname)s - %(message)s')

def read_dataset(file_path):
    """ Read data from csv

    Args:
      file_path (str): file path to read

    Returns:
      data (DataFrame): returns file read as a dataframe.
    """
    try:
        data = pd.read_csv(file_path)
        return data
    except: # pylint: disable=bare-except
        logging.error("There is no such %s", file_path)
    return None

exchange_rates = read_dataset('euro-daily-hist_1999_2020.csv')

exchange_rates.info()

exchange_rates.rename(columns={'[Brazilian real ]': 'BR_real', # pylint: disable=E1101
                               'Period\\Unit:': 'Time'},
                      inplace=True)

exchange_rates['Time'] = pd.to_datetime(exchange_rates['Time'])
exchange_rates.sort_values('Time', inplace=True)
exchange_rates.reset_index(drop=True, inplace=True) # pylint: disable=E1101
exchange_rates.head(5) # pylint: disable=E1101

#Selecionando apenas os dados a serem utilizados
euro_to_real = exchange_rates[['Time', 'BR_real']] # pylint: disable=E1136  # pylint/issues/3139
euro_to_real.head(5)

# limpando dados
euro_to_real = euro_to_real[euro_to_real['BR_real'] != '-']

euro_to_real['BR_real'].value_counts()

euro_to_real['BR_real'] = euro_to_real['BR_real'].astype('float')
euro_to_real.info()

style.use('fivethirtyeight')
plt.plot(euro_to_real['Time'],
        euro_to_real['BR_real'])

plt.show()

# Média móvel
euro_to_real['rolling_mean'] = euro_to_real['BR_real'].rolling(30).mean()
euro_to_real.tail(5)

plt.plot(euro_to_real['Time'],
        euro_to_real['rolling_mean'])

plt.show()

lula_dilma_bolsonaro = euro_to_real[(euro_to_real.Time.dt.year >= 2003)
               & (euro_to_real.Time.dt.year < 2021)]

lula = euro_to_real[(euro_to_real.Time.dt.year >= 2003)
               & (euro_to_real.Time.dt.year < 2011)]

dilma_temer = euro_to_real[(euro_to_real.Time.dt.year >= 2011)
                       & (euro_to_real.Time.dt.year < 2019)]

bolsonaro = euro_to_real[(euro_to_real.Time.dt.year >= 2019)
               & (euro_to_real.Time.dt.year < 2021)]

fig_lula, ax_lula = plt.subplots()
ax_lula.plot(lula['Time'],
         lula['rolling_mean'],
         color='purple', alpha=0.7)

ax_lula.text(x=732512, y=4.2, s='LULA',
         color='purple', weight='bold',
         size=15, alpha=0.7)
ax_lula.text(x=732312, y=4.1, s='(2003-2011)', color='gray')

plt.xticks(rotation=35)

#plt.savefig('underLula.png', format='png')
plt.show()

fig_dilma_temer, ax_dilma_temer = plt.subplots()
ax_dilma_temer.plot(dilma_temer['Time'],
         dilma_temer['rolling_mean'],
         color='orange', alpha=0.7)

ax_dilma_temer.text(x=735114, y=5.2, s='DILMA-TEMER',
         color='orange', weight='bold',
         size=15, alpha=0.7)
ax_dilma_temer.text(x=735234, y=5.05, s='(2011-2019)', color='gray')

plt.xticks(rotation=35)

#plt.savefig('underDilma-Temer.png', format='png')
plt.show()

fig_bolsonaro, ax_bolsonaro = plt.subplots()
ax_bolsonaro.plot(bolsonaro['Time'],
         bolsonaro['rolling_mean'],
         color='blue', alpha=0.7)

ax_bolsonaro.text(x=737333, y=7, s='BOLSONARO',
         color='blue', weight='bold',
         size=15, alpha=0.7)
ax_bolsonaro.text(x=737333, y=6.85, s='(2019-CURRENT)', color='gray')

plt.xticks(rotation=35)

#plt.savefig('underBolsonaro.png', format='png')
plt.show()

ax_bolsonaro.get_xticks()

style.use('fivethirtyeight')
plt.figure(figsize=(12, 6))

ax1 = plt.subplot(2, 3, 1)
ax2 = plt.subplot(2, 3, 2)
ax3 = plt.subplot(2, 3, 3)
ax4 = plt.subplot(2, 1, 2)
axes = [ax1, ax2, ax3, ax4]

for ax in axes:
    for location in ['top', 'right', 'bottom', 'left']:
        ax.spines[location].set_visible(False)
        ax.set_ylim(1.5, 7)
        ax.set_yticks([2, 3, 4, 5, 6])
        ax.set_yticklabels(['2', '3', '4', '5', '6'])
        ax.grid(0.5)

ax1.plot(lula['Time'],
         lula['rolling_mean'],
         color='purple', alpha=0.7)

ax2.plot(dilma_temer['Time'],
         dilma_temer['rolling_mean'],
         color='orange', alpha=0.7)

ax3.plot(bolsonaro['Time'],
         bolsonaro['rolling_mean'],
         color='blue', alpha=0.7)

ax1.text(x=732390, y=7.8, s='LULA',
         color='purple', weight='bold',
         size=15, alpha=0.7)
ax1.text(x=732070, y=7.3, s='(2003-2011)', color='gray')
ax1.set_xticklabels(['', '2003', '', '2005', '',
                     '2007', '', '2009', '',
                     '2011'])

ax2.text(x=734829, y=7.8, s='DILMA-TEMER',
         color='orange', weight='bold',
         size=15, alpha=0.7)
ax2.text(x=734999, y=7.3, s='(2011-2019)', color='gray')
ax2.set_xticklabels(['', '2011', '', '2013',
                     '', '2015', '', '2017',
                     '', '2019'])

ax3.text(x=737241, y=7.8, s='BOLSONARO',
         color='blue', weight='bold',
         size=15, alpha=0.7)
ax3.text(x=737271, y=7.3, s='(2019-Current)', color='gray')
ax3.set_xticklabels(['2019', '', '', '',
                     '2020', '', '', '',
                     '2021'])

ax4.plot(lula['Time'], lula['rolling_mean'],
        color='purple', alpha=0.7)
ax4.plot(dilma_temer['Time'], dilma_temer['rolling_mean'],
        color='orange', alpha=0.7)
ax4.plot(bolsonaro['Time'], bolsonaro['rolling_mean'],
        color='blue', alpha=0.7)
ax4.grid(alpha=0.5)

ax1.text(x=731000, y=9,
         s='EURO-REAL exchange rates under the last three Brazilian presidents',
         fontsize=20, weight='bold')

ax4.text(730690, 0.0, 'Author: Kaio Henrique' + ' '*103 + 'Fonte: European Central Bank',
         color='#f0f0f0', backgroundcolor='#4d4d4d', size=14)

#plt.savefig('underThree.png', format='png')
plt.show()
