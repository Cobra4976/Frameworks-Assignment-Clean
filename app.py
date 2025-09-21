import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
df = pd.read_csv("metadata.csv")
df['publish_time'] = pd.to_datetime(df['publish_time'], errors='coerce')
df['year'] = df['publish_time'].dt.year

st.title("CORD-19 Data Explorer")
st.write("Simple exploration of COVID-19 research papers")

# Slider to filter by year
years = df['year'].dropna().unique()
min_year, max_year = int(min(years)), int(max(years))
year_range = st.slider("Select year range", min_year, max_year, (2020, 2021))

filtered = df[(df['year'] >= year_range[0]) & (df['year'] <= year_range[1])]

# Visualization: Publications by Year
st.subheader("Publications by Year")
year_counts = filtered['year'].value_counts().sort_index()
fig, ax = plt.subplots()
ax.bar(year_counts.index, year_counts.values)
ax.set_xlabel("Year")
ax.set_ylabel("Number of Publications")
st.pyplot(fig)

# Show sample of data
st.subheader("Sample Data")
st.write(filtered[['title', 'authors', 'journal', 'year']].head(10))