import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pandas_datareader as data
from keras.models import load_model
import streamlit as st
import yfinance as yf





tickers=["GOOGL"]
st.title('Stock Trend Prediction')

user_input = st.text_input('Enter Stock Ticker','GOOGL')
df=yf.download(user_input,start="2010-1-1",end="2023-1-22",group_by=user_input)

#describing data
st.subheader('Data from 2010 - 2023')
st.write(df.describe())

#visualizations
st.subheader('Closing Price vs Time chart')
fig= plt.figure(figsize = (12,6))
plt.plot(df.Close)
st.pyplot(fig)

st.subheader('Closing Price vs Time chart with 100MA')
ma100= df.Close.rolling(100).mean()
fig= plt.figure(figsize = (12,6))
plt.plot(ma100)
plt.plot(df.Close)
st.pyplot(fig)

st.subheader('Closing Price vs Time chart with 100MA & 200MA')
ma100= df.Close.rolling(100).mean()
ma200= df.Close.rolling(200).mean()
fig= plt.figure(figsize = (12,6))
plt.plot(ma100)
plt.plot(ma200)
plt.plot(df.Close)
st.pyplot(fig)


data_training = pd.DataFrame(df['Close'][0:int(len(df)*0.70)])
data_testing = pd.DataFrame(df['Close'][int(len(df)*0.70): int(len(df))])
print(data_training.shape)
print(data_testing.shape)


from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler (feature_range=(0,1))
data_training_array = scaler.fit_transform(data_training)




model = load_model('keras_model.h5')

#testing part
past_100_days = data_training.tail(100)

final_df = past_100_days.append(data_testing, ignore_index=True)
input_data= scaler.fit_transform(final_df)

x_test = []

y_test = []

for i in range(100, input_data.shape[0]):

    x_test.append(input_data[i-100: i])
    y_test.append(input_data[i, 0]) 


x_test, y_test = np.array(x_test), np.array(x_test)
y_predicted = model.predict(x_test)
scaler= scaler.scale_

scale_factor = 1/0.02099517

y_predicted = y_predicted * scale_factor

y_test = y_test * scale_factor 



#final graph
st.subheader('PREDICTION VS Original')
fig2= plt.figure(figsize=(12,6))
y_test = y_test.reshape(y_test.shape[0], y_test.shape[1])
y_predicted = y_predicted.reshape(y_predicted.shape[0], y_predicted.shape[1])
plt.plot(y_test, 'b', label = 'Original Price')
plt.plot(y_predicted, 'r', label = 'Predicted Price')
plt.xlabel('Time')
plt.ylabel('Price')
plt.legend()
st.pyplot(fig2)