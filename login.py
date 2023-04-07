import streamlit as st
import snowflake.connector
import hashlib

st.set_page_config(page_title="Karigari", page_icon=":fork_and_knife:")

def connect_to_snowflake():
  conn = snowflake.connector.connect(**st.secrets[ "snowflake" ])
  return conn

def create_new_user_profile(name, email, password, age, weight, height, activity_level):
    # Hash the password using SHA-256 algorithm
  password_hash = hashlib.sha256(password.encode()).hexdigest()
  conn = connect_to_snowflake()
  cursor = conn.cursor()
  cursor.execute("INSERT INTO user_profiles (name, email, password_hash, age, weight, height, activity_level) VALUES (%s, %s, %s, %s, %s, %s, %s)", (name, email, password_hash, age, weight, height, activity_level))
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
    cursor.execute("SELECT name, email, age, weight, height, activity_level, BMI FROM user_profiles WHERE email = %s", (email,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result

def get_user_favourites(email):
    conn = connect_to_snowflake()
    cursor = conn.cursor()
    cursor.execute("SELECT recipe_name FROM user_favourites WHERE email = %s", (email,))
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
  
def get_food_items_by_type(food_title):
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
    cursor.execute("SELECT CALORIES, PROTEIN, FAT, SODIUM FROM FOOD_ITEMS WHERE TITLE = %s", (food_calorie,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result

def create_custom_food_item(food_type, food_title, calories, protein, fat, sodium):
    conn = connect_to_snowflake()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO CUSTOM_FOOD_ITEMS (EMAIL, TYPE, TITLE, CALORIES, PROTEIN, FAT, SODIUM) VALUES (%s, %s, %s, %s, %s, %s, %s)",
        (st.session_state.email, food_type, food_title, calories, protein, fat, sodium),
    )
    conn.commit()
    cursor.close()
    conn.close()
    


st.sidebar.header('Navigation')
page = st.sidebar.radio('Go to', ['Create Profile', 'Login', 'Dashboard'])

if page == 'Create Profile':
    st.header('Create Your Profile')
    name = st.text_input('Name')
    email = st.text_input('Email')
    password = st.text_input('Password', type='password')
    age = st.number_input('Age(In Years)', min_value=0, max_value=200)
    weight = st.number_input('Weight(In KG)', min_value=0, max_value=1000)
    height = st.number_input('Height(In CM)', min_value=0, max_value=500)
    activity_level = st.selectbox('Activity Level', options=['Sedentary',  'Moderately Active', 'Very Active'])
    if st.button('Create Profile'):
        create_new_user_profile(name, email, password, age, weight, height, activity_level)
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
            name, email, age, weight, height, bmi, activity_level = get_user_data(st.session_state.email)
            st.write(f"Name: {get_user_data(st.session_state.email)[0]}")
            st.write(f"Email: {get_user_data(st.session_state.email)[1]}")
            st.write(f"Age: {get_user_data(st.session_state.email)[2]}")
            st.write(f"Weight: {get_user_data(st.session_state.email)[3]}")
            st.write(f"Height: {get_user_data(st.session_state.email)[4]}")
            st.write(f"BMI: {get_user_data(st.session_state.email)[6]}")
            st.write(f"Activity Level: {get_user_data(st.session_state.email)[5]}")
    st.header('🍰🍛 Build Your Own Receipe 🍕🍗')
    selected_food_type = st.selectbox('Select a Food Type', get_food_items_by_type())
      
    
    st.write('Search recipes based on ingredients:')
    ingredients = st.text_input('Enter ingredients separated by commas')
    if st.button('Search'):
        recipes = search_recipes(ingredients)
        for r in recipes:
            st.write(r['title'])
            st.write(f"Ready in {r['readyInMinutes']} minutes")
            st.write(f"Serves {r['servings']} people")
            st.write(f"Link: {r['sourceUrl']}")
            st.image(r['image'])
