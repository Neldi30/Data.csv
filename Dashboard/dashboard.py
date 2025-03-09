import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import seaborn as sns
sns.set(style='dark')

st.set_page_config(
    page_title="Bike Sharing Dashboard Dicoding❤️",
    page_icon=":bike:",
    initial_sidebar_state="expanded"
)

# Load cleaned data
day_df_clean = pd.read_csv('C:/Users/taufi/streamlit_dashboard/cleaned_day_df.csv')
hour_df_clean = pd.read_csv('C:/Users/taufi/streamlit_dashboard/cleaned_hour.csv')

# Data preparation functions
def create_hourly_data(df):
    hourly_data = df.groupby(by='Hour').agg({
        'Casual': 'mean',
        'Registered': 'mean',
    }).reset_index()
    return hourly_data

def create_working_day_data(df):
    working_day_data = df.groupby(by='Working Day').agg({
        'Casual': 'mean',
        'Registered': 'mean',
        'Total': 'mean'
    }).reset_index()
    return working_day_data

def create_yearly_data(df):
    yearly_data = df.groupby(by=['Year', 'Month']).agg({
        'Total': 'sum'
    }).reset_index()
    yearly_data['Date'] = pd.to_datetime(yearly_data['Year'].astype(str) + '-' + yearly_data['Month'].astype(str), format='%Y-%B')
    yearly_data = yearly_data.sort_values(by='Date')
    return yearly_data

# Sidebar
with st.sidebar:
    st.image("https://svgsilh.com/svg/307877.svg", caption="Bike Sharing", use_column_width=True)
    st.title('Capital Bikeshare Dashboard')
    st.markdown("[Dataset Source](https://archive.ics.uci.edu/dataset/275/bike+sharing+dataset)")
    st.markdown("[Source Code](https://github.com/Neldi30/Data.csv.git)")


# Data preparation
hourly_data = create_hourly_data(hour_df_clean)
working_day_data = create_working_day_data(hour_df_clean)
yearly_data = create_yearly_data(day_df_clean)

# Menghitung total, casual, dan registered untuk plot hourly
hourly_counts = hourly_data['Casual'] + hourly_data['Registered']
hourly_casual = hourly_data['Casual']
hourly_registered = hourly_data['Registered']

st.header("Bike Sharing Dashboard :bike:")
st.subheader("Rata-rata Penyewaan Sepeda per Jam")

fig = plt.figure(figsize=(10, 6))
sns.lineplot(x=hourly_data['Hour'], y=hourly_counts, label='Total', marker='o')
sns.lineplot(x=hourly_data['Hour'], y=hourly_casual, label='Casual', marker='o')
sns.lineplot(x=hourly_data['Hour'], y=hourly_registered, label='Registered', marker='o')

plt.title('Rata-rata Penyewaan Sepeda per Jam')
plt.xlabel('Jam')
plt.ylabel('Jumlah Penyewaan')
plt.xticks(hourly_data['Hour'].unique())
plt.legend(title='Tipe Penyewaan')
plt.grid(True)

st.pyplot(fig)

st.divider()

st.subheader("Peminjaman Sepeda Berdasarkan Hari Kerja dan Akhir Pekan")
fig, ax = plt.subplots(figsize=(8, 5))
working_day_data.set_index('Working Day')[['Casual', 'Registered', 'Total']].plot(
    kind='bar', stacked=False, ax=ax
)

ax.set_title('Rata-rata Peminjaman Sepeda Berdasarkan Hari Kerja dan Akhir Pekan')
ax.set_xlabel('Kategori Hari')
ax.set_ylabel('Rata-rata Jumlah Peminjaman')
ax.set_xticks(range(len(working_day_data['Working Day'])))
ax.set_xticklabels(working_day_data['Working Day'], rotation=0)
ax.legend(title='Tipe Peminjaman')
ax.grid(True)

st.pyplot(fig)

st.divider()

st.subheader("Peminjaman Sepeda Tahun 2011 dan 2012 ")
fig, ax = plt.subplots(figsize=(12, 6))
sns.lineplot(data=yearly_data, x='Date', y='Total', marker='o', color='red', ax=ax)

ax.set_title('Perkembangan Peminjaman Sepeda (Januari 2011 - Desember 2012)')
ax.set_xlabel('Bulan')
ax.set_ylabel('Jumlah Peminjaman')
plt.xticks(rotation=45)
ax.grid(True)

st.pyplot(fig)
