# Import python packages.
import streamlit as st
from snowflake.snowpark.functions import col

# Write directly to the app.
st.title(f"Choose your Custom Smoothis :cup_with_straw ")
st.write(
  """Choose your fruit in your custom smoothie
  """
)

name_on_order = st.text_input('Name on the Smoothie:')
st.write('The Name on the Smoothie will be', name_on_order)

cnx =st.connection("snowflake")
session =cnx.session()
# Fully qualify the table name and check column names
my_dataframe = session.table("SMOOTHIES.PUBLIC.FRUIT_OPTIONS").select(col('FRUIT_NAME'), col('SEARCH_ON'))

# Convert to Pandas safely
try:
    pd_df = my_dataframe.to_pandas()
except Exception as e:
    st.error("Error connecting to Snowflake table. Please check your column names.")
    st.stop() # Stops the app here so you don't get more errors
# ... (previous code for imports and name_on_order)

ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:",
    my_dataframe,
    max_selections=5
)

if ingredients_list: 
    ingredients_string = ""

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '

        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        st.write('The search value for ', fruit_chosen,' is ', search_on, '.')

        # --- NEW CODE PLACEMENT ---
        st.subheader(f"{fruit_chosen} Nutrition Information")
        # Ensure the URL does not have brackets []
        search_url = f"https://my.smoothiefroot.com/api/fruit/{SEARCH_ON}"
        smoothiefroot_response = requests.get(search_url)
        st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)
        # --------------------------

    # SQL logic follows after the loop
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, "NAME_ON_ORDER")
    values ('""" + ingredients_string + """','"""+name_on_order+ """')"""
    
    #st.write(my_insert_stmt)
    time_to_insert = st.button('Submit Order')
    

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")

import requests  
smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
#st.text(smoothiefroot_response.json())
sf_df= st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)













