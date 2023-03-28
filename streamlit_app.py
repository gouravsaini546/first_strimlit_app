
import streamlit
import pandas
import snowflake.connector
import requests
from urllib.error import URLError

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

fruit_choice = streamlit.text_input('What fruit would you like information about?')
streamlit.write('The user entered ', fruit_choice)

def get_fruitvice_data(this_fruit_choice):
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+this_fruit_choice)
  fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
  return fruityvice_normalized

streamlit.header("Fruityvice Fruit Advice!")
try:
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+fruit_choice)
  if not fruit_choice:
    streamlit.error("Please select a fruit to get information.")
  else:
    back_from_function = get_fruitvice_data(fruit_choice)
    streamlit.dataframe(back_from_function)
except URLError as e:
  streamlit.error()


streamlit.header("The fruit load list contains : ")

def get_fruit_load_list():
  with mycnx.cursor() as my_cur:
    my_cur.execute("select * from fruit_load_list")
    return my_cur.fetchall()
  
data = [{"id":642582,"title":"Farfalle With Broccoli, Carrots and Tomatoes","image":"https://spoonacular.com/recipeImages/642582-312x231.jpg","imageType":"jpg","usedIngredientCount":2,"missedIngredientCount":6,"missedIngredients":[{"id":10120420,"amount":1.0,"unit":"pound","unitLong":"pound","unitShort":"lb","aisle":"Pasta and Rice","name":"farfalle pasta","original":"1 pound farfalle pasta","originalName":"farfalle pasta","meta":[],"image":"https://spoonacular.com/cdn/ingredients_100x100/farfalle.png"},{"id":4042,"amount":2.0,"unit":"tablespoons","unitLong":"tablespoons","unitShort":"Tbsp","aisle":"Oil, Vinegar, Salad Dressing","name":"peanut oil","original":"2 tablespoons peanut oil","originalName":"peanut oil","meta":[],"image":"https://spoonacular.com/cdn/ingredients_100x100/peanut-oil.jpg"},{"id":11090,"amount":2.0,"unit":"inches","unitLong":"inches","unitShort":"inches","aisle":"Produce","name":"broccoli heads","original":"2 inches large broccoli heads (that's what she said)","originalName":"broccoli heads (that's what she said)","meta":["(that's what she said)"],"image":"https://spoonacular.com/cdn/ingredients_100x100/broccoli.jpg"}]}]

# normalize the JSON data into a pandas dataframe
df = pandas.json_normalize(data, 
                       record_path='missedIngredients',
                       meta=['id', 'title'], 
                       meta_prefix='recipe_')
 streamlit.dataframe(df)

if streamlit.button('Get Fruit Load List'):
   mycnx = snowflake.connector.connect (**streamlit.secrets[ "snowflake"])
   my_data_rows = get_fruit_load_list()
   streamlit.dataframe(my_data_rows)
    
def insert_row_snowflake(new_fruit):
  with my_cnx.cursor() as my_cur:
    my_cur.execute("insert into fruit_load_list values('"+add_my_fruit+"')")
    return "Thanks for adding " + new_fruit
  
add_my_fruit = streamlit.text_input('What fruit would you like to add?')
if streamlit.button('Add a Fruit to the List'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets[ "snowflake" ])
  back_from_function = insert_row_snowflake(add_my_fruit)
  streamlit.text(back_from_function) 
 
streamlit.stop()

add_fruit = streamlit.text_input('What fruit would you like to add?')
my_cur.execute("insert into fruit_load_list values (" +"'"+add_fruit+"'"+")" )
streamlit.write('Thanks for adding ', add_fruit)

