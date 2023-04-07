import streamlit as st
import snowflake.connector
import hashlib
# import necessary packages
import requests

# initialize the Streamlit app
st.set_page_config(page_title='Karigari - Evolving Food Industry', page_icon=':apple:', layout='wide', initial_sidebar_state='auto')
st.markdown('<style>body{background-color: #e6f7ff;}</style>', unsafe_allow_html=True)
st.title('Karigari - Evolving Food Industry')

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
page = st.sidebar.radio('Go to', ['Create Profile', 'Login','User Dashboard'])

def user_dashboard():
    st.header(f'Welcome, {st.session_state["name"]}!')
    st.image('https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/240/google/298/green-apple_1f34f.png', width=100)
    st.write('')
    with st.beta_container():
        st.subheader('Nutrients Selected')
        st.write(f'Fats: {fats}%')
        st.write(f'Carbohydrates: {carbohydrates}%')
        st.write(f'Protein: {protein}%')
    cols = st.beta_columns(2)
    with cols[0]:
        st.subheader('Favorites')
        # display the user's favorite recipes
    with cols[1]:
        st.write('')
    st.subheader('Search Recipes')

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
    st.image('https://cdn-icons-png.flaticon.com/512/2592/2592317.png', width=100)
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

with st.container():
    st.subheader('Nutrients Selected')
    st.write(f'Fats: {fats}%')
    st.write(f'Carbohydrates: {carbohydrates}%')
    st.write(f'Protein: {protein}%')
    st.image('https://w7.pngwing.com/pngs/493/176/png-transparent-apple-green-apple-food-image-file-formats-leaf-thumbnail.png', width=100)
    st.write('')
    
cols = st.beta_columns(2)
with cols[0]:
    st.subheader('Favorites')
    # display the user's favorite recipes
with cols[1]:
   # st.image('https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/240/twitter/282/heart-with-arrow_1f498.png', width=100)
    st.write('')
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
