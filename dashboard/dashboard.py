import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
sns.set(style='dark')


# Helper function yang dibutuhkan untuk menyiapkan berbagai dataframe

def create_monthly_user_df(df):
    monthly_user_df = df.groupby(by=["yr","mnth"], as_index=False).agg({
    "casual": "mean",
    "registered": "mean",
    "cnt": "mean"
    })
    monthly_user_df['casual'] = monthly_user_df['casual'].astype('int')
    monthly_user_df['registered'] = monthly_user_df['registered'].astype('int')
    return monthly_user_df

def create_first_year_user_df(df):
    first_year_user_df = df.head(12)
    return first_year_user_df

def create_second_year_user_df(df):
    second_year_user_df = df.tail(12)
    return second_year_user_df

def create_avg_year_user_df(df):
    avg_year_user_df = df.groupby(by="mnth", as_index=False).agg({
     "casual": "mean",
    "registered": "mean",
    "cnt": "mean"
    })
    avg_year_user_df['casual'] = avg_year_user_df['casual'].astype('int')
    avg_year_user_df['registered'] = avg_year_user_df['registered'].astype('int')
    return avg_year_user_df

def create_byweathersit_df(df):
    byweathersit_df = df.groupby(by="weathersit", as_index = False).cnt.mean().sort_values(by='cnt', ascending=False)
    byweathersit_df['weathersit'] = byweathersit_df['weathersit'].replace([1, 2, 3], ['Clear/Partly Cloudy', 'Mist/Cloudy', 'Light Snow/Light Rain'])  
    return byweathersit_df

def create_byday_df(df):
    byday_df = df.groupby(by="weekday", as_index=False).cnt.mean().sort_values(by="cnt", ascending=False)
    byday_df['weekday'] = byday_df['weekday'].replace([0, 1, 2, 3, 4, 5, 6],['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']) 
    return byday_df



# Load cleaned data

daily_df = pd.read_csv('data/day.csv')

# Menyiapkan berbagai dataframe
monthly_user_df = create_monthly_user_df(daily_df)
first_year_user_df = create_first_year_user_df(monthly_user_df)
second_year_user_df = create_second_year_user_df(monthly_user_df)
avg_year_user_df = create_avg_year_user_df(monthly_user_df)
byweathersit_df = create_byweathersit_df(daily_df)
byday_df = create_byday_df(daily_df)


# menyusun dashboard

with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://img.freepik.com/free-vector/bicycle-logo-template-design_23-2150367174.jpg?w=740&t=st=1700220929~exp=1700221529~hmac=509860960115aaf161cb0ef0d374bc5da4adbbe997a97eb7ed5ad11830380105")

    st.subheader('Proyek Akhir Kelas Belajar Analisa dengan Python')
    st.text('isham Fakhri Rahman')
    st.text('ishamfakhri01@gmail.com')

st.header('Bike Rents Report :sparkles:')
st.markdown('This webpage is designed to report and share information about bicycle rentals over 2011 and 2012.The data compiled here delves into the usage, trends, and patterns of bike rentals throughout these consecutive years, shedding light on the varying dynamics and potential insights during that time frame.')

st.subheader('Monthly Users in 2011 and 2012')

fig, ax = plt.subplots(nrows=2, ncols=1, figsize=(8, 12), layout='constrained')

first_year = first_year_user_df['mnth']                   
count_first = {
    "Casual": first_year_user_df['casual'],
    "Registered": first_year_user_df['registered']
}                                                         

second_year = second_year_user_df['mnth']                  
count_second = {
    "Casual": second_year_user_df['casual'],
    "Registered": second_year_user_df['registered']
}                                                         

x_1 = np.arange(len(first_year))  
x_2 = np.arange(len(second_year))
width = 0.3  
multiplier = 0

for firstyear, measurement in count_first.items():
    offset = width * multiplier
    rects = ax[0].bar(x_1 + offset, measurement, width, label=firstyear)
    ax[0].bar_label(rects, padding=3)
    multiplier += 1

ax[0].set_xlabel('Month')
ax[0].set_title('Number of users in 2011')
ax[0].set_xticks(x_1 + width, first_year)
ax[0].legend(loc='upper left')

for secondyear, measurement in count_second.items():
    offset = width * multiplier
    rects = ax[1].bar(x_2 + offset, measurement, width, label=secondyear)
    ax[1].bar_label(rects, padding=3)
    multiplier += 1

ax[1].set_xlabel('Month')
ax[1].set_title('Number of users in 2012')
ax[1].set_xticks(x_2 + width, second_year)
ax[1].legend(loc='upper left')

st.pyplot(fig)

st.subheader('Average User permonth')

avg_year_user_df = monthly_user_df.groupby(by="mnth", as_index=False).agg({
     "casual": "mean",
    "registered": "mean"
})
avg_year_user_df['casual'] = avg_year_user_df['casual'].astype('int')
avg_year_user_df['registered'] = avg_year_user_df['registered'].astype('int')

months = avg_year_user_df['mnth']                    
counts = {
    "Casual": avg_year_user_df['casual'],
    "Registered": avg_year_user_df['registered']
}                                                         

x = np.arange(len(months))  
width = 0.3  
multiplier = 0

plt.figure(figsize=(8, 7))
fig, ax = plt.subplots(layout='constrained')

for attribute, measurement in counts.items():
    offset = width * multiplier
    rects = ax.bar(x + offset, measurement, width, label=attribute)
    ax.bar_label(rects, padding=3)
    multiplier += 1

ax.set_xlabel('Month')
ax.set_title('Average User per month in 2011 and 2012')
ax.set_xticks(x + width, months)
ax.legend(loc='upper left')

st.pyplot(fig)



st.subheader('Weather Trends on the Number of Users')

st.markdown("Clear/Partly Cloud = Clear, Few clouds, Partly cloudy, Partly cloudy")
st.markdown("Mist/Cloudy = Mist + Cloudy, Mist + Broken clouds, Mist + Few clouds, Mist")
st.markdown("Light Snow/Light Rain = Light Snow, Light Rain + Thunderstorm + Scattered clouds, Light Rain + Scattered clouds")
fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(
    x="cnt", 
    y="weathersit",
    data=byweathersit_df.sort_values(by="cnt", ascending=False),
    palette="tab10",
    orient='h',
    ax=ax)
ax.set_title("Number of User by Weathersit", loc="center", fontsize=15)
ax.set_ylabel(None)
ax.set_xlabel('Average')
ax.tick_params(axis='y', labelsize=12)

st.pyplot(fig)

st.subheader('Days by the Users')


fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(28, 10))

colors = "colorblind"

sns.barplot(x="cnt", y="weekday", data=byday_df, palette=colors, ax=ax[0], orient='h')
ax[0].set_ylabel(None)
ax[0].set_xlabel('User')
ax[0].set_title("Most User Days", loc="center", fontsize=20)
ax[0].tick_params(axis ='y', labelsize=18)
ax[0].tick_params(axis ='x', labelsize=18)

sns.barplot(x="cnt", y="weekday", data=byday_df.sort_values(by="cnt", ascending=True), palette=colors, ax=ax[1], orient='h')
ax[1].set_ylabel(None)
ax[1].set_xlabel('User')
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_title("Fewest User Days", loc="center", fontsize=20)
ax[1].tick_params(axis='y', labelsize=18)
ax[1].tick_params(axis ='x', labelsize=18)

plt.suptitle("Most and Fewest User Days", fontsize=20)

st.pyplot(fig)
st.caption('Copyright (c) by sam.fakhri')
