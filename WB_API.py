import wbgapi as wb
import pandas as pd
import streamlit as st

 

# Function to make list into a markdown for easier viewability:
def list_to_markdown(selected_data):
    s = ''
    for i in selected_data:
        s += "- " + i + "\n"
    st.markdown(s)


def main():
    st.set_page_config(page_title="World Bank Indicator Simple Search")
    st.header(" World Bank Indicator Simple Search ")
    st.subheader("A work in progress by Anas AbdulBaqi :construction_worker:")

    # User text input for the topic
    topic = st.text_input('Select a topic to start searching for relevant data: ')

    # When the user selects a topic and enters it
    if topic is not None and topic != "":

        st.write('Your topic is: ', topic)

        # Search the API with the topic
        search_results = wb.series.info(q=topic)

        num_results = len(search_results.items)
        # Display the number of results
        if num_results == 0:
            st.write('0 results with this topic, try a different topic or capitalize/uncapitalize the word')
            
        else:
            st.write(num_results, 'results') 
        
            search_results_value = [item['value'] for item in search_results.items]

            selected_data = st.multiselect('Select multiple data from results', search_results_value)
            count = 0
            if st.button('Done selecting data!'):
                st.write('You picked these data:')
                list_to_markdown(selected_data)
                new_results = [item for item in search_results.items if item['value'] in selected_data]
                count = 1
                
            if count == 1: 
                st.write('Which countries would you like to select data for?')


        


if __name__ == "__main__":
    main()
