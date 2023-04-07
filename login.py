import streamlit as st
import snowflake.connector
import hashlib

# import necessary packages
import streamlit as st
import snowflake.connector
import requests

# initialize the Streamlit app
st.set_page_config(page_title='Karigari - Evolving Food Industry', page_icon=':apple:', layout='wide', initial_sidebar_state='auto')
st.markdown('<style>body{background-color: #e6f7ff;}</style>', unsafe_allow_html=True)
st.title('Karigari - Evolving Food Industry')

# define the login page
def login():
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

# define the user dashboard page
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
        st.image('https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/240/twitter/282/heart-with-arrow_1f498.png', width=100)
        st.write('')
    st.subheader('Search Recipes')
    # allow the user to search for recipes using the Recipe API

# define a function to authenticate the user login
def authenticate_user_login(email, password):
    # authenticate the user using the Snowflake data warehouse
    # return True and the user's name if successful, False otherwise
    return True, 'John Doe'

# initialize the session state
if 'name' not in st.session_state:
    st.session_state['name'] = None

# create a dictionary to map page names to functions
pages = {
    'Login': login,
    'User Dashboard': user_dashboard
}

# define the page selection dropdown
page = st.sidebar.selectbox('Select a page', options=list(pages.keys()))

# display the selected page
pages[page]()

# redirect the user to the user dashboard after successful login
if st.session_state['name'] is not None and page == 'Login':
    st.experimental_rerun()  # this will automatically switch the page to the user dashboard


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






