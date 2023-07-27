import wbgapi as wb
import streamlit as st


# Function to make list into a markdown for easier viewability:
def list_to_markdown(selected_data):
    st.write('Your Selected Datasets:')
    s = ''
    for i in selected_data:
        s += "- " + i + "\n"
    st.markdown(s)


@st.cache_data
def search_web(topic):
    # Search the API with the topic
    search_results = wb.series.info(q=topic)
    num_of_results = len(search_results.items)
    st.write(num_of_results, "results")
    if num_of_results == 0: 
        st.write('Try a different topic (maybe capitalize / uncapitalize word)')

    return search_results


@st.cache_data
def metadata_info(id):
    return wb.series.metadata.get(id)


@st.cache_data
def final_data(id, country, time_start, time_end):
    return wb.data.DataFrame(id, country, time=range(time_start, time_end, 1), labels=True)

def main():
    #Setting up the page: 
    st.set_page_config(page_title="World Bank Indicator Simple Search")
    st.header(" World Bank Indicator Simple Search ")
    st.subheader("A work in progress by Anas AbdulBaqi :construction_worker:")

    with st.sidebar:
        #User picks his topic
        topic_form = st.form("topic")
        topic = topic_form.text_input("Pick a topic to search:")

        #Search API for the results:
        if topic != "":
            search_results = search_web(topic)
            search_results_value = [item[   'value'] for item in search_results.items]
        topic_form.form_submit_button("Start the search")

        #User selects data from the results
        text_form = st.form("form")
        if topic != "":
            val = text_form.multiselect("select your data from the results:", search_results_value)
            text_form.form_submit_button("Finished selecting data")

            new_results = [item for item in search_results.items if item['value'] in val]
            new_results_id = [item['id'] for item in new_results]

        #------------------Range and Country-----------------------------------------------------------
        if topic != "":
            country_form = st.form("country form")
            country = country_form.text_input("Select countries: ")
            time_start = country_form.number_input("Start Year:" )
            time_end = country_form.number_input("End Year:" )
            if country != "":
                st.write('Your selected country: ' , country)
                st.write('Data from ', time_start, 'to', time_end)

            country_form.form_submit_button("Show my data!")
        #-------------------------------------------------------------------------------------------------

        
        

    st.header('Info about your data')
    #Display the results
    if topic != "":
        list_to_markdown(val)


    #Option for more info about the data
    
        for id in new_results_id:
            id_info = metadata_info(id)
            with st.expander("more info about data"):
                id_info

        if country is not None and time_start is not None:
            if country != "":
                for id in new_results_id:
                    #st.write(id, country, time_start, time_end)
                    time_start = int(time_start)
                    time_end = int(time_end)
                    st.dataframe(final_data(id, country, time_start, time_end))

if __name__ == "__main__":
    main()