import streamlit as st
import snowflake.connector
import hashlib

st.set_page_config(page_title="Karigari", page_icon=":fork_and_knife:")

def connect_to_snowflake():
  conn = snowflake.connector.connect(**st.secrets[ "snowflake" ])
  return conn

def create_new_user_profile(name, email, password):
    # Hash the password using SHA-256 algorithm
  password_hash = hashlib.sha256(password.encode()).hexdigest()
  conn = connect_to_snowflake()
  cursor = conn.cursor()
  cursor.execute("INSERT INTO user_profiles (name, email, password_hash) VALUES (%s, %s, %s)", (name, email, password_hash))
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
    cursor.execute("SELECT name, email, age, weight, height, activity_level FROM user_profiles WHERE email = %s", (email,))
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

st.sidebar.header('Navigation')
page = st.sidebar.radio('Go to', ['Create Profile', 'Login', 'Dashboard'])

if page == 'Create Profile':
    st.title('Create Your Profile')
    name = st.text_input('Name')
    email = st.text_input('Email')
    password = st.text_input('Password', type='password')
    if st.button('Create Profile'):
        create_new_user_profile(name, email, password)
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
    st.write(f"Email: {get_user_data(st.session_state.email)[1]}")
    st.write(f"Nutrients: {get_user_data(st.session_state.email)[3]}")
    new_nutrients = st.text_input('Enter your updated nutrient levels')
    if st.button('Update Nutrients'):
        update_user_nutrients(st.session_state.email, new_nutrients)
        st.success('Nutrients updated successfully!')

    st.write('Favorites:')
    favorites = get_user_favorites(st.session_state.email)
    if favorites:
        for f in favorites:
            st.write(f)

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
