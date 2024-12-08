import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import warnings 
warnings.filterwarnings('ignore')
import plotly.express as px 
import joblib


# -- Header
# -- Subheader 
# -- Diplay image
# -- Background of the project 
# -- Dataframe
# -- Sidebar, user image 
# -- Sidebar, Feature Input



# Add header and Subheader 
st.markdown("<h1 style = 'color: #363062; text-align: center; font-size: 40px; font-family: helvetica'>Advert And Sales Web App</h1>", unsafe_allow_html = True)
st.markdown("<h4 style = 'margin: -30px; color: #E3651D; text-align: center; font-family: helvetica '>Built By 5th Factor Cohort 1</h4>", unsafe_allow_html = True)

# Image 
col1, col2, col3 = st.columns([1, 2, 1])
col2.image('pngwing.com (14).png' )

# Background To project 
st.markdown("<h4 style = 'margin: -30px; color: #0E2954; text-align: center; font-family: helvetica '>Background Of The Project</h4>", unsafe_allow_html = True)
st.write("""
In todays competitive market, understanding the relationship between advertising expenditure and sales performance is crucial for businesses. Machine learning models can analyze historical data to identify patterns and make predictions about future sales based on advertising spend. By leveraging techniques such as regression analysis, businesses can optimize their marketing strategies and allocate budgets more effectively. <br>
The goal of this project is to develop a machine learning model that predicts the sales of a product based on the amount spent on advertising. The model will utilize historical sales data and corresponding advertising expenditures to identify key factors influencing sales performance. The outcome will provide insights into how effectively advertising spend translates into sales, enabling businesses to make data-driven marketing decisions.""")

st.divider()

st.markdown("<br>", unsafe_allow_html= True)
data = pd.read_csv('AdvertAndSales.csv')
st.dataframe(data, use_container_width = True)


st.sidebar.image('pngwing.com (16).png', caption= 'Welcome User')

# Feature Input 
tv = st.sidebar.number_input('Television Advert Expense',min_value = 0.0, max_value = 10000.0, value = data.TV.median())
radio = st.sidebar.number_input('Radio Advert Expense', min_value = 0.0,max_value = 10000.0, value = data.Radio.median())
soc = st.sidebar.number_input('Social Media Advert Expense', min_value =0.0, max_value =10000.0, value = data['Social Media'].median())
inf = st.sidebar.selectbox('Type Of Influencer', data.Influencer.unique(), index=1 )


inputs = {
    'TV': [tv],
    'Radio': [radio],
    'Social Media': [soc],
    'Influencer': [inf]
}
inputVar = pd.DataFrame(inputs)

st.divider()
st.header('User Input')
st.dataframe(inputVar)


# Inport the transformers 
tv_scaler = joblib.load('TV_scaler.pkl')
radio_scaler = joblib.load('Radio_scaler.pkl')
soc_scaler = joblib.load('Social Media_scaler.pkl')
inf_scaler = joblib.load('Influencer_encoder.pkl')

# Use the imported transformers to transform the users input
inputVar['TV'] = tv_scaler.transform(inputVar[['TV']])
inputVar['Radio'] = radio_scaler.transform(inputVar[['Radio']])
inputVar['Social Media'] = soc_scaler.transform(inputVar[['Social Media']])
inputVar['Influencer'] = inf_scaler.transform(inputVar[['Influencer']])


model = joblib.load('advertModel.pkl')

predictButton = st.button('Push To Predict')

if predictButton:
    predicted = model.predict(inputVar)
    st.success(f'The predicted sales Value is ${round(predicted[0], 2)}')