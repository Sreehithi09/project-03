
import streamlit as st
from assistant import get_response
import pandas as pd
from prophet import Prophet
import plotly.express as px

st.set_page_config(page_title="⚡ Energy Analytics Assistant", layout="wide")
st.title("⚡ Energy Usage Forecasting and Analytics")

# Upload or use sample dataset
uploaded_file = st.file_uploader("Upload energy usage CSV", type=["csv"])
if uploaded_file:
    df = pd.read_csv(uploaded_file)
else:
    st.info("Using sample dataset.")
    df = pd.read_csv("sample_data.csv")

# Prepare data
df['timestamp'] = pd.to_datetime(df['timestamp'])
df = df[['timestamp', 'usage']].rename(columns={'timestamp': 'ds', 'usage': 'y'})

st.subheader("📄 Data Preview")
st.dataframe(df.head())


# Energy usage over time
st.subheader("📊 Energy Usage Over Time")
fig0 = px.line(df, x='ds', y='y', labels={'ds': 'Date', 'y': 'Energy Usage (kWh)'})
st.plotly_chart(fig0, use_container_width=True)


# Forecasting
model = Prophet()
model.fit(df)
future = model.make_future_dataframe(periods=7)
forecast = model.predict(future)

st.subheader("📈 Forecasted Energy Usage (Next 7 Days)")
fig1 = px.line(forecast, x='ds', y='yhat', labels={'ds': 'Date', 'yhat': 'Predicted Usage (kWh)'})
st.plotly_chart(fig1, use_container_width=True)

# Inefficiency detection
st.subheader("⚠️ Detected Inefficiencies")
threshold = df['y'].mean() * 1.2
inefficiencies = df[df['y'] > threshold]
st.write(inefficiencies.tail())

# Categorize usage into 'Hot' and 'Cool'
avg_usage = df['y'].mean()
df['Usage_Type'] = df['y'].apply(lambda x: 'Hot' if x > avg_usage else 'Cool')

# Plot bar graph
st.subheader("🔥❄️ Hot and Cool Energy Usage")
hot_cool_fig = px.bar(
    df,
    x='ds',
    y='y',
    color='Usage_Type',
    color_discrete_map={'Hot': 'red', 'Cool': 'blue'},
    labels={'ds': 'Date', 'y': 'Energy Usage (kWh)', 'Usage_Type': 'Type'}
)
st.plotly_chart(hot_cool_fig, use_container_width=True)


# Assistant Section
st.subheader("🤖 Energy Assistant")
query = st.text_input("Ask me anything about energy usage:")
if query:
    response = get_response(query)
    st.markdown(f"**Assistant:** {response}")
