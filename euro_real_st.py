"""
Author: Kaio Henrique de Sousa
Date: May 2022
"""

import streamlit as st
import logging
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import style
from io import BytesIO
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
                               '[US dollar ]': 'US_dollar',
                               '[Chinese yuan renminbi ]': 'Chinese_yuan_renminbi',
                               '[Canadian dollar ]': 'Canadian_dollar',
                               '[Japanese yen ]': 'Japanese_yen',
                               '[Indian rupee ]': 'Indian_rupee',
                               'Period\\Unit:': 'Time'},
                      inplace=True)

exchange_rates['Time'] = pd.to_datetime(exchange_rates['Time'])
exchange_rates.sort_values('Time', inplace=True)
exchange_rates.reset_index(drop=True, inplace=True) # pylint: disable=E1101
exchange_rates.head(5) # pylint: disable=E1101

#Selecionando apenas os dados a serem utilizados
euro_to_real = exchange_rates[['Time', 'BR_real']] # pylint: disable=E1136  # pylint/issues/3139
exchange_rates_sel = exchange_rates[['Time', 'BR_real', # pylint: disable=E1136  # pylint/issues/3139
                               'US_dollar', 'Chinese_yuan_renminbi',
                               'Canadian_dollar', 'Japanese_yen',
                               'Indian_rupee']]
euro_to_real.head(5)

# limpando dados
euro_to_real = euro_to_real[euro_to_real['BR_real'] != '-']

exchange_rates_sel = exchange_rates_sel[(exchange_rates_sel['BR_real'] != '-') &
                                      (exchange_rates_sel['US_dollar'] != '-') &
                                      (exchange_rates_sel['Chinese_yuan_renminbi'] != '-') &
                                      (exchange_rates_sel['Canadian_dollar'] != '-') &
                                      (exchange_rates_sel['Japanese_yen'] != '-') &
                                      (exchange_rates_sel['Indian_rupee'] != '-')]

euro_to_real['BR_real'].value_counts()

euro_to_real['BR_real'] = euro_to_real['BR_real'].astype('float')
euro_to_real.info()

# Streamlit
st.title('Euro-Real Exchange Rates Under Lula(2003-2011), Dilma-Temer(2011-2019) and Bolsonaro(2019-2021)')

with st.sidebar:
    optionCurrency = st.selectbox(
        'Which currency do you want to choose?',
        ('US_dollar', 'Chinese_yuan_renminbi',
        'BR_real', 'Canadian_dollar',
        'Japanese_yen', 'Indian_rupee'))
    
st.write('You selected:', optionCurrency)

style.use('fivethirtyeight')
fig_real, ax_real = plt.subplots()
ax_real.plot(exchange_rates_sel['Time'],
        exchange_rates_sel[optionCurrency].astype('float'))

st.pyplot(fig_real)

# Média móvel
euro_to_real['rolling_mean'] = euro_to_real['BR_real'].rolling(30).mean()
euro_to_real.tail(5)

st.header('EURO-REAL rolling mean with rolling window of 30')

fig_rm, ax_rm = plt.subplots()
ax_rm.plot(euro_to_real['Time'],
        euro_to_real['rolling_mean'])

st.pyplot(fig_rm)

lula_dilma_bolsonaro = euro_to_real[(euro_to_real.Time.dt.year >= 2003)
               & (euro_to_real.Time.dt.year < 2021)]

lula = euro_to_real[(euro_to_real.Time.dt.year >= 2003)
               & (euro_to_real.Time.dt.year < 2011)]

dilma_temer = euro_to_real[(euro_to_real.Time.dt.year >= 2011)
                       & (euro_to_real.Time.dt.year < 2019)]

bolsonaro = euro_to_real[(euro_to_real.Time.dt.year >= 2019)
               & (euro_to_real.Time.dt.year < 2021)]

with st.sidebar:
    optionPresident = st.selectbox(
         'which president do you want to choose?',
         ('Lula', 'Dilma-Temer', 'Bolsonaro'))

st.header('Exchange Rates Under a Selected Brazilian President')
st.write('You selected:', optionPresident)

if(optionPresident == 'Lula'):
    fig_lula, ax_lula = plt.subplots()
    ax_lula.plot(lula['Time'],
                 lula['rolling_mean'],
                 color='purple', alpha=0.7)
    
    plt.xticks(rotation=35)
    st.pyplot(fig_lula)
    
elif(optionPresident == 'Dilma-Temer'):
    fig_dilma_temer, ax_dilma_temer = plt.subplots()
    ax_dilma_temer.plot(dilma_temer['Time'],
                        dilma_temer['rolling_mean'],
                        color='orange', alpha=0.7)

    plt.xticks(rotation=35)
    st.pyplot(fig_dilma_temer)
    
elif(optionPresident == 'Bolsonaro'):
    fig_bolsonaro, ax_bolsonaro = plt.subplots()
    ax_bolsonaro.plot(bolsonaro['Time'],
                      bolsonaro['rolling_mean'],
                      color='blue', alpha=0.7)

    plt.xticks(rotation=35)
    st.pyplot(fig_bolsonaro)

style.use('fivethirtyeight')
fig_all = plt.figure(figsize=(12, 6))

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

ax1.set_xticklabels(['', '2003', '', '2005', '',
                     '2007', '', '2009', '',
                     '2011'])

ax2.set_xticklabels(['', '2011', '', '2013',
                     '', '2015', '', '2017',
                     '', '2019'])

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


st.header('Exchange Rates Under the Last Three Brazilian Presidents')
st.pyplot(fig_all)

