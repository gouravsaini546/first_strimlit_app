import streamlit as st
import snowflake.connector
import hashlib

st.title('Karigari - Evolving Food Industry')

def connect_to_snowflake():
  conn = snowflake.connector.connect(**st.secrets[ "snowflake" ])
  return conn
def create_new_user_profile(name, email, password, fats, carbohydrates, protein):
    # Hash the password using SHA-256 algorithm
  password_hash = hashlib.sha256(password.encode()).hexdigest()
  conn = connect_to_snowflake()
  cursor = conn.cursor()
  cursor.execute("INSERT INTO user_profiles (name, email, password_hash, fats, carbohydrates, protein) VALUES (%s, %s, %s, %s, %s, %s)", (name, email, password_hash, fats, carbohydrates, protein))
  conn.commit()
  cursor.close()
  conn.close()

def authenticate_user_login(email, password):
    conn = connect_to_snowflake()
    cursor = conn.cursor()
    cursor.execute("SELECT name, password_hash FROM user_profiles WHERE email=%s", (email,))
    result = cursor.fetchone()
    if result is None:
        return False, None
    name, password_hash = result
    entered_password_hash = hashlib.sha256(password.encode()).hexdigest()
    if password_hash == entered_password_hash:
        return True, name
    else:
        return False, None


st.sidebar.header('Navigation')
page = st.sidebar.radio('Go to', ['Create Profile', 'Login'])


if page == 'Create Profile':
    st.header('Create Your Profile')
    name = st.text_input('Name')
    email = st.text_input('Email')
    password = st.text_input('Password', type='password')
    fats = st.number_input('Fats', min_value=0, max_value=100)
    carbohydrates = st.number_input('Carbohydrates', min_value=0, max_value=100)
    protein = st.number_input('Protein', min_value=0, max_value=100)
    if st.button('Create Profile'):
        create_new_user_profile(name, email, password, fats, carbohydrates, protein)
        st.success('Profile created successfully!')
        
if page == 'Login':
    st.header('Login')
    st.image('https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/240/apple/285/shield_1f6e1.png', width=100)
    email = st.text_input('Email')
    password = st.text_input('Password', type='password')
    if st.button('Login'):
        success, name = authenticate_user_login(email, password)
        if success:
            st.success(f'Welcome back, {name}!')
            st.session_state['name'] = name
            st.experimental_rerun()
        else:
            st.error('Incorrect email or password. Please try again.')

            
if page == 'User Dashboard':
    st.header(f'Welcome, {st.session_state["name"]}!')
    st.subheader('Nutrients Selected')
    st.write(f'Fats: {fats}%')
    st.write(f'Carbohydrates: {carbohydrates}%')
    st.write(f'Protein: {protein}%')
    
    st.subheader('Favorites')
    # display the user's favorite recipes
    
    st.subheader('Recipe Search Tool')
    # display a tool to search for recipes based on ingredients using the recipe API



