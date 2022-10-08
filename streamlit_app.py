
import streamlit
import pandas

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

streamlit.title('My Parents New Healthy Dinner')
streamlit.header('Breakfast Menu')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]
streamlit.dataframe(fruits_to_show)

fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
streamlit.write('The user entered ', fruit_choice)

import requests
streamlit.header("Fruityvice Fruit Advice!")
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+fruit_choice)

# flatten the JSON Data
fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
# show the flattened data in table
streamlit.dataframe(fruityvice_normalized)

import snowflake.connector

my_cnx = snowflake.connector.connect (**streamlit.secrets[ "snowflake"])
my_cur = my_cnx.cursor()
select_data = my_cur.execute("select * from fruit_load_list")
my_data_row = select_data.fetchall()
streamlit.header("The fruit load list contains : ")
streamlit.dataframe(my_data_row)

add_fruit = streamlit.text_input('What fruit would you like to add?')
my_cur.execute("insert into fruit_load_list values (" +"'"+add_fruit+"'"+")" )

