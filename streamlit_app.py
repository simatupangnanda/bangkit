import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Set style seaborn
sns.set(style='dark')

# Menyiapkan data df
df = pd.read_csv("https://raw.githubusercontent.com/simatupangnanda/data_bangkit/main/day_data.csv")


# Mengubah nama kolom
df.rename(columns={
    'dteday': 'dateday',
    'yr': 'year',
    'mnth': 'month',
    'cnt': 'count'
}, inplace=True)

# Nama Bulan
df['month'] = df['month'].map({
    1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
    7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'
})

# Menyiapkan harian_df
def data_harian(df):
    harian_df = df.groupby(by='dateday').agg({
    'count': 'sum'
    }).reset_index()
    return harian_df
    
# Menyiapkan season_df
def data_season(df):
    season_df = df.groupby(by="season").agg({
    "count": "sum"
})
    return season_df

# Menyiapkan bulanan_df
def data_bulanan(df):
    bulanan_df = df.groupby(by='month').agg({
    'temp':'mean',
    'count': 'sum'
    })
    ordered_months = [
        'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
        'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
    ]
    bulanan_df = bulanan_df.reindex(ordered_months, fill_value=0)
    return bulanan_df

# komponen filter
min_date = pd.to_datetime(df['dateday']).dt.date.min()
max_date = pd.to_datetime(df['dateday']).dt.date.max()
 
with st.sidebar:    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value= min_date,
        max_value= max_date,
        value=[min_date, max_date]
    )

main_df = df[(df['dateday'] >= str(start_date)) & 
                (df['dateday'] <= str(end_date))]

# Datafram yang akan digunakan utuk membut visualisasi
harian_df = data_harian(main_df)
season_df = data_season(main_df)
bulanan_df = data_bulanan(main_df)

# Judul
st.title('Dashboard Penyewaan Sepeda')

# Jumlah rental harian
st.subheader('Berdasarkan Hari')
col1,= st.columns(1)
with col1:
    daily_rent_total = harian_df['count'].sum()
    st.metric('Total User', value= daily_rent_total)

# Jumlah rental bulanan
st.subheader('Jumlah rental Bulanan')
fig, ax = plt.subplots(figsize=(24, 8))
ax.plot(
    bulanan_df.index,   
    bulanan_df['count'],
    marker='o', 
    linewidth=2,
    color='tab:blue'
)

for index, row in enumerate(bulanan_df['count']):
    ax.text(index, row + 1, str(row), ha='center', va='bottom', fontsize=12)

ax.tick_params(axis='x', labelsize=25)
ax.tick_params(axis='y', labelsize=20)
st.pyplot(fig)

# Jumlah rental berdasarkan musim
st.subheader('Berdasarkan Musim')

fig, ax = plt.subplots(figsize=(16, 8))
sns.barplot(x='season', y='count', data=season_df)
plt.xlabel("Musim")
plt.ylabel("Jumalah Perentalan")
plt.title("Jumlah Perentalan Berdasarkan Musim")

st.pyplot(fig)

# Jumlah rental Berdasarkan Suhu
st.subheader('Rental Berdasarkan Suhu')

fig, ax = plt.subplots(figsize=(16, 8))

sns.lineplot(x='temp', y='count', data=bulanan_df)
plt.xlabel("Temperatur") 
plt.ylabel("Jumlah Perentalan")
plt.title("Jumlah Perentalan Berdasarkan Temperatur")

st.pyplot(fig)

# Jumlah penyewaan berdasarkan temperatur
st.subheader('Cluster Berdasarkan Musim')

fig, ax = plt.subplots(figsize=(16, 8))
sns.scatterplot(x='temp', y='count', data=df, hue='season',style="season")
plt.xlabel("Temperature (degC)")
plt.ylabel("Jumlah Perentalan")
plt.title("Cluster penyewaan sepeda berdasarkan Musimnya")

st.pyplot(fig)

st.caption('copyright (c) Nanda Simatupang 2024')