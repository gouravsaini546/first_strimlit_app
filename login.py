import streamlit as st
import snowflake.connector
import hashlib

st.title('Karigari')

def connect_to_snowflake():
  conn = snowflake.connector.connect(**st.secrets[ "snowflake" ])
  return conn
def create_new_user_profile(name, email, password, weight, height, activity_level):
    # Hash the password using SHA-256 algorithm
  password_hash = hashlib.sha256(password.encode()).hexdigest()
  conn = connect_to_snowflake()
  cursor = conn.cursor()
  cursor.execute("INSERT INTO user_profiles (name, email, password_hash, weight, height, activity_level) VALUES (%s, %s, %s, %s, %s, %s)", (name, email, password_hash, weight, height, activity_level))
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

st.sidebar.header('Navigation')
page = st.sidebar.radio('Go to', ['Create Profile', 'Login'])


if page == 'Create Profile':
    st.header('Create Your Profile')
    name = st.text_input('Name')
    email = st.text_input('Email')
    password = st.text_input('Password', type='password')
    weight = st.number_input('Weight(In KG)', min_value=0, max_value=1000)
    height = st.number_input('Height(In CM)', min_value=0, max_value=500)
    activity_level = st.selectbox('Activity Level', options=['Sedentary',  'Moderately Active', 'Very Active'])
    if st.button('Create Profile'):
        create_new_user_profile(name, email, password, height, weight, activity_level)
        st.success('Profile created successfully!')
        
if page == 'Login':
    st.header('Login')
    email = st.text_input('Email')
    password = st.text_input('Password', type='password')
    if st.button('Login'):
        if authenticate_user_login(email, password):
            st.success('Login successful!')
        else:
            st.error('Incorrect email or password. Please try again.')

