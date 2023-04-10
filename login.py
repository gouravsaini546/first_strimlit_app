import streamlit as st
import snowflake.connector
import hashlib
import pandas as pd

st.set_page_config(page_title="Karigari", page_icon=":fork_and_knife:")

def connect_to_snowflake():
  conn = snowflake.connector.connect(**st.secrets[ "snowflake" ])
  return conn

def create_new_user_profile(name, email, password,gender, age, weight, height, activity_level):
    # Hash the password using SHA-256 algorithm
  password_hash = hashlib.sha256(password.encode()).hexdigest()
  conn = connect_to_snowflake()
  cursor = conn.cursor()
  cursor.execute("INSERT INTO user_profiles (name, email, password_hash, gender, age, weight, height, activity_level) VALUES (%s,%s, %s, %s, %s, %s, %s, %s)", (name, email, password_hash,gender, age, weight, height, activity_level))
  conn.commit()
  cursor.close()
  conn.close()
def create_favourite(email,food_type, food_title,topping, calories, protein, fat, sodium):
  conn = connect_to_snowflake()
  cursor = conn.cursor()
  cursor.execute("INSERT INTO favourite (email, type, title,topping, calories, protein, fat, sodium) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",(email,selected_food_type,selected_food_item,selected_toppings,calories_value,Protein_value,Fat_value,Sodium_value))
  conn.commit()
  cursor.close()
  conn.close()

def authenticate_user_login(email, password):
  conn = connect_to_snowflake()
  cursor = conn.cursor()
  cursor.execute("SELECT password_hash FROM user_profiles WHERE email = %s", (email,))
  result = cursor.fetchone()
  cursor.close()
  conn.close()
  if result is not None:
    stored_hash = result[0]
    input_hash = hashlib.sha256(password.encode()).hexdigest()
    if stored_hash == input_hash:
      return True
  return False

def get_user_data(email):
    conn = connect_to_snowflake()
    cursor = conn.cursor()
    cursor.execute("SELECT name, email,gender, age, weight, height, activity_level, BMI FROM user_profiles WHERE email = %s", (email,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result

def get_user_favourites(email):
    conn = connect_to_snowflake()
    cursor = conn.cursor()
    cursor.execute("SELECT type, title, topping, calories, protein, fat, sodium FROM favourite WHERE email = %s limit 3", (email,))
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return [result[0] for result in results]

def add_user_favourite(email, recipe_name):
    conn = connect_to_snowflake()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO user_favourites (email, recipe_name) VALUES (%s, %s)", (email, recipe_name))
    conn.commit()
    cursor.close()
    conn.close()
def get_food_items_by_type(food_type=None):
    conn = connect_to_snowflake()
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT TYPE FROM FOOD_ITEMS WHERE TYPE IS NOT NULL ")
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return [row[0] for row in result]
  
def get_food_items_by_title(food_title):
    conn = connect_to_snowflake()
    cursor = conn.cursor()
    cursor.execute("SELECT TITLE FROM FOOD_ITEMS WHERE TYPE = %s", (food_title,))
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return [row[0] for row in result]

def get_food_item_info(food_calorie):
    conn = connect_to_snowflake()
    cursor = conn.cursor()
    cursor.execute("SELECT to_number(CALORIES) AS CALORIES, to_number(PROTEIN) AS PROTEIN, to_number(FAT) AS FAT, to_number(SODIUM) AS SODIUM  FROM FOOD_ITEMS WHERE TITLE = %s", (food_calorie,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result
def get_toppings(food_toppings):
    conn = connect_to_snowflake()
    cursor = conn.cursor()
    cursor.execute("SELECT NAME FROM toppings WHERE TYPE = upper(%s)", (food_toppings,))
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return [row[0] for row in result]
def get_toppings_item_info(toppings_calorie):
    conn = connect_to_snowflake()
    cursor = conn.cursor()
    cursor.execute("SELECT SUM(to_number(CALORIE)) AS CALORIES, to_number(SUM(PROTEIN)) AS PROTEIN, to_number(SUM(FAT)) AS FAT, to_number(SUM(SODIUM)) AS SODIUM FROM toppings WHERE NAME IN (%s)", (toppings_calorie,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result


    

st.title('Karigari👨‍🍳')
st.sidebar.header('Navigation')
page = st.sidebar.radio('Go to', ['Create Profile', 'Login', 'Dashboard'])

if page == 'Create Profile':
    st.header('Create Your Profile')
    name = st.text_input('Name')
    email = st.text_input('Email')
    password = st.text_input('Password', type='password')
    gender = st.selectbox('Gender', options=['Male',  'Female', 'Others'])
    age = st.number_input('Age(In Years)', min_value=0, max_value=200)
    weight = st.number_input('Weight(In KG)', min_value=0, max_value=1000)
    height = st.number_input('Height(In CM)', min_value=0, max_value=500)
    activity_level = st.selectbox('Activity Level', options=['Sedentary',  'Moderately Active', 'Very Active'])
    if st.button('Create Profile'):
        create_new_user_profile(name, email, password,gender, age, weight, height, activity_level)
        st.success('Profile created successfully!')

elif page == 'Login':
    st.title('Login')
    email = st.text_input('Email')
    password = st.text_input('Password', type='password')
    if st.button('Login'):
        if authenticate_user_login(email, password):
            st.success('Login successful!')
            st.session_state.logged_in = True
            st.session_state.email = email
        else:
            st.error('Incorrect email or password. Please try again.')

if st.session_state.get('logged_in'):
    st.title('Dashboard')
    st.write(f"Welcome {get_user_data(st.session_state.email)[0]}!")

    if st.button('View Profile Details'):
        with st.expander('User Profile'):
            name, email,gender, age, weight, height, bmi, activity_level = get_user_data(st.session_state.email)
            st.write(f"Name: {get_user_data(st.session_state.email)[0]}")
            st.write(f"Email: {get_user_data(st.session_state.email)[1]}")
            st.write(f"Age: {get_user_data(st.session_state.email)[3]}")
            st.write(f"Weight: {get_user_data(st.session_state.email)[4]}")
            st.write(f"Height: {get_user_data(st.session_state.email)[5]}")
            st.write(f"BMI: {get_user_data(st.session_state.email)[7]}")
            st.write(f"Activity Level: {get_user_data(st.session_state.email)[6]}")
    st.header('🍰🍛 Favourites 🍕🍗')
    favourites = get_user_favourites(get_user_data(st.session_state.email)[1])
    df3 = pd.DataFrame(favourites, columns=["Type", "Title", "Topping", "Calories", "Protein", "Fat", "Sodium"])
    #df3 = pd.DataFrame({'favourites':rows ,
                                        #'Amount':["Type", "Title", "Topping", "Calories", "Protein", "Fat", "Sodium"]})
    st.write(df3)
    #df3 = pd.DataFrame(rows, columns=["Type", "Title", "Topping", "Calories", "Protein", "Fat", "Sodium"])
    # Hide nutritional information by default
    #df3 = df3[["Type", "Title", "Topping"]]
    #st.write(df3)
    #if st.button("Show Nutritional Information"):
        #df = pd.DataFrame(rows, columns=["Type", "Title", "Topping", "Calories", "Protein", "Fat", "Sodium"])
        #st.write(df)
    
    
    st.header('🍰🍛 Build Your Own Receipe 🍕🍗')
    selected_food_type = st.selectbox('Select a Food Type', get_food_items_by_type())
    selected_food_item = st.selectbox('Select a Food variant', get_food_items_by_title(selected_food_type))
    selected_toppings = 'N/A'
    if len(get_toppings(selected_food_type)) > 0:
        selected_toppings = st.multiselect("Pick some toppings:", get_toppings(selected_food_type))
        if selected_toppings:
            toppings_details = get_toppings_item_info(selected_toppings)
            toppings_df = pd.DataFrame({'Nutrient': ['Calories', 'Protein', 'Fat', 'Sodium'],
                                        'Amount': toppings_details})
            selected_toppings = ';'.join(selected_toppings)
            
        else:
            toppings_df = pd.DataFrame({'Nutrient': ['Calories', 'Protein', 'Fat', 'Sodium'],
                                        'Amount': [0, 0, 0, 0]})
    else:
        toppings_df = pd.DataFrame({'Nutrient': ['Calories', 'Protein', 'Fat', 'Sodium'],
                                    'Amount': [0, 0, 0, 0]})

    if selected_food_item:
        food_details = get_food_item_info(selected_food_item)
        food_df = pd.DataFrame({'Nutrient': ['Calories', 'Protein', 'Fat', 'Sodium'],
                                'Amount': food_details})
    else:
        food_df = pd.DataFrame({'Nutrient': ['Calories', 'Protein', 'Fat', 'Sodium'],
                                'Amount': [0, 0, 0, 0]})

    # Sum the nutrient amounts from both dataframes
    total_df = toppings_df.add(food_df, fill_value=0)
    total_food_df = pd.DataFrame({'Nutrient': ['Calories', 'Protein', 'Fat', 'Sodium'],
                                'Amount': total_df['Amount']})
    # Display the total nutrient amounts in a table
    calories_value = total_food_df.loc[total_food_df['Nutrient'] == 'Calories', 'Amount'].item()
    Protein_value = total_food_df.loc[total_food_df['Nutrient'] == 'Protein', 'Amount'].item()
    Fat_value = total_food_df.loc[total_food_df['Nutrient'] == 'Fat', 'Amount'].item()
    Sodium_value = total_food_df.loc[total_food_df['Nutrient'] == 'Sodium', 'Amount'].item()
    st.table(total_food_df)
    email = get_user_data(st.session_state.email)[1]
    if st.button("Save as Favorites"):
      create_favourite(email,selected_food_type,selected_food_item,selected_toppings,calories_value,Protein_value,Fat_value,Sodium_value)
      st.success('favorites created')
    

      
    
