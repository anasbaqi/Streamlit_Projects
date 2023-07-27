import wbgapi as wb
import streamlit as st


# Function to make list into a markdown for easier viewability:
def list_to_markdown(selected_data):
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

def select_data(search_results):
    #form for multi-selecting data from search:
    with st.form("multi-select data"):
        selected_data = st.multiselect('View and select data from results', search_results)
        submitted = st.form_submit_button("done selecting data")
    
    if submitted:
        st.write('You picked these data:')
        list_to_markdown(selected_data)

    return selected_data

def select_topic():
    #New form where user will select their topic:
    topic_form =  st.form("enter topic")
    topic = topic_form.text_input("Select a topic to start searching for relevant data: ")
    exec_done = topic_form.form_submit_button("Submit")

    if exec_done == True: 
        st.write("the topic you selected is: ", topic)
    return topic, exec_done


def main():
    #Setting up the page: 
    st.set_page_config(page_title="World Bank Indicator Simple Search")
    st.header(" World Bank Indicator Simple Search ")
    st.subheader("A work in progress by Anas AbdulBaqi :construction_worker:")

    #call select_topic to grab the topic from user:
    topic, exec_done = select_topic()
    
    start_select = False
    if exec_done:
        #call search_web to search the API with topic and output the number of results after form is submitted
        search_results = search_web(topic)
        start_select = True
    
    selected_data = []

    if start_select == True:
        # #form to ask user if he is ready:
        done_selecting = False
        search_results_value = [item['value'] for item in search_results.items]
        selected_data = select_data(search_results_value)
        st.write(selected_data)

    if selected_data is not None and selected_data != []:
            st.write('THIS IS BAD')

    # #Show data:
    # if data_selected == True:
    #     st.write('You picked these data:')
    #     list_to_markdown(selected_data)

if __name__ == "__main__":
    main()