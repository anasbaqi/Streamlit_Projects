import wbgapi as wb
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import altair as alt

#ISO3 Dictionary:
iso3 = {'Afghanistan': 'AFG', 'Albania': 'ALB', 'Algeria': 'DZA', 'American Samoa': 'ASM', 'Andorra': 'AND', 'Angola': 'AGO', 'Anguila': 'AIA', 'Antigua and Barbuda': 'ATG', 'Argentina': 'ARG', 'Armenia': 'ARM', 'Aruba': 'ABW', 'Australia': 'AUS', 'Austria': 'AUT', 'Azerbaijan': 'AZE', 'Gambia': 'GMB', 'Bahrain': 'BHR', 'Bangladesh': 'BGD', 'Barbados': 'BRB', 'Belarus': 'BLR', 'Belgium': 'BEL', 'Belgium-Luxembourg': 'BLX', 'Belize': 'BLZ', 'Benin': 'BEN', 'Bermuda': 'BMU', 'Bhutan': 'BTN', 'Bolivia': 'BOL', 'Bosnia and Herzegovina': 'BIH', 'Botswana': 'BWA', 'Br. Antr. Terr': 'BAT', 'Brazil': 'BRA', 'British Indian Ocean Ter.': 'IOT', 'British Virgin Islands': 'VGB', 'Brunei': 'BRN', 'Bulgaria': 'BGR', 'Burkina Faso': 'BFA', 'Burundi': 'BDI', 'Cambodia': 'KHM', 'Cameroon': 'CMR', 'Canada': 'CAN', 'Cape Verde': 'CPV', 'Cayman Islands': 'CYM', 'Central African Republic': 'CAF', 'Chad': 'TCD', 'Chile': 'CHL', 'China': 'HKG', 'Christmas Island': 'CXR', 'Cocos (Keeling) Islands': 'CCK', 'Colombia': 'COL', 'Comoros': 'COM', 'Dem. Rep.': 'PRK', 'Yemen Rep.': 'YEM', 'Cook Islands': 'COK', 'Costa Rica': 'CRI', "Cote d'Ivoire": 'CIV', 'Croatia': 'HRV', 'Cuba': 'CUB', 'Cyprus': 'CYP', 'Czech Republic': 'CZE', 'Czechoslovakia': 'CSK', 'Denmark': 'DNK', 'Djibouti': 'DJI', 'Dominica': 'DMA', 'Dominican Republic': 'DOM', 'East Timor': 'TMP', 'Ecuador': 'ECU', 'Egypt': 'EGY', 'El Salvador': 'SLV', 'Equatorial Guinea': 'GNQ', 'Eritrea': 'ERI', 'Estonia': 'EST', 'Ethiopia (excludes Eritrea)': 'ETH', 'Ethiopia (includes Eritrea)': 'ETF', 'European Union': 'EUN', 'Faeroe Islands': 'FRO', 'Falkland Island': 'FLK', 'Fiji': 'FJ', 'Finland': 'FIN', 'Fm Panama Cz': 'PCZ', 'Fm Rhod Nyas': 'ZW1', 'Fm Tanganyik': 'TAN', 'Fm Vietnam Dr': 'VDR', 'Fm Vietnam Rp': 'SVR', 'Fm Zanz-Pemb': 'ZPM', 'Fr. So. Ant. Tr': 'ATF', 'France': 'FRA', 'Free Zones': 'FRE', 'French Guiana': 'GUF', 'French Polynesia': 'PYF', 'Gabon': 'GAB', 'Gaza Strip': 'GAZ', 'Georgia': 'GEO', 'German Democratic Republic': 'DDR', 'Germany': 'DEU', 'Ghana': 'GHA', 'Gibraltar': 'GIB', 'Greece': 'GRC', 'Greenland': 'GRL', 'Grenada': 'GRD', 'Guadeloupe': 'GLP', 'Guam': 'GUM', 'Guatemala': 'GTM', 'Guinea': 'GIN', 'Guinea-Bissau': 'GNB', 'Guyana': 'GUY', 'Haiti': 'HTI', 'Holy See': 'VAT', 'Honduras': 'HND', 'Hungary': 'HUN', 'Iceland': 'ISL', 'India': 'IND', 'Indonesia': 'IDN', 'Iran': 'IRN', 'Iraq': 'IRQ', 'Ireland': 'IRL', 'Palestine': 'ISR', 'Italy': 'ITA', 'Jamaica': 'JAM', 'Japan': 'JPN', 'Jhonston Island': 'JTN', 'Jordan': 'JOR', 'Kazakhstan': 'KAZ', 'Kenya': 'KEN', 'Kiribati': 'KIR', 'Kuwait': 'KWT', 'Kyrgyz Republic': 'KGZ', 'Lao PDR': 'LAO', 'Latvia': 'LVA', 'Lebanon': 'LBN', 'Lesotho': 'LSO', 'Liberia': 'LBR', 'Libya': 'LBY', 'Liechtenstein': 'LIE', 'Lithuania': 'LTU', 'Luxembourg': 'LUX', 'Macao': 'MAC', 'FYR': 'MKD', 'Madagascar': 'MDG', 'Malawi': 'MWI', 'Malaysia': 'MYS', 'Maldives': 'MDV', 'Mali': 'MLI', 'Malta': 'MLT', 'Marshall Islands': 'MHL', 'Martinique': 'MTQ', 'Mauritania': 'MRT', 'Mauritius': 'MUS', 'Mexico': 'MEX', 'Fed. Sts.': 'FSM', 'Midway Islands': 'MID', 'Moldova': 'MDA', 'Monaco': 'MCO', 'Mongolia': 'MNG', 'Montserrat': 'MSR', 'Morocco': 'MAR', 'Mozambique': 'MOZ', 'Myanmar': 'MMR', 'Namibia': 'NAM', 'Nauru': 'NRU', 'Nepal': 'NPL', 'Netherlands': 'NLD', 'Netherlands Antilles': 'ANT', 'Neutral Zone': 'NZE', 'New Caledonia': 'NCL', 'New Zealand': 'NZL', 'Nicaragua': 'NIC', 'Niger': 'NER', 'Nigeria': 'NGA', 'Niue': 'NIU', 'Norfolk Island': 'NFK', 'Northern Mariana Islands': 'MNP', 'Norway': 'NOR', 'Oman': 'OMN', 'Pacific Islands': 'PCE', 'Pakistan': 'PAK', 'Palau': 'PLW', 'Panama': 'PAN', 'Papua New Guinea': 'PNG', 'Paraguay': 'PRY', 'Pen Malaysia': 'PMY', 'Peru': 'PER', 'Philippines': 'PHL', 'Pitcairn': 'PCN', 'Poland': 'POL', 'Portugal': 'PRT', 'Puerto Rico': 'PRI', 'Qatar': 'QAT', 'Reunion': 'REU', 'Romania': 'ROM', 'Russian Federation': 'RUS', 'Rwanda': 'RWA', 'Ryukyu Is': 'RYU', 'Sabah': 'SBH', 'Saint Helena': 'SHN', 'Saint Kitts-Nevis-Anguilla-Aru': 'KN1', 'Saint Pierre and Miquelon': 'SPM', 'Samoa': 'WSM', 'San Marino': 'SMR', 'Sao Tome and Principe': 'STP', 'Sarawak': 'SWK', 'Saudi Arabia': 'SAU', 'Senegal': 'SEN', 'Seychelles': 'SYC', 'Sierra Leone': 'SLE', 'SIKKIM': 'SIK', 'Singapore': 'SGP', 'Slovak Republic': 'SVK', 'Slovenia': 'SVN', 'Solomon Islands': 'SLB', 'Somalia': 'SOM', 'South Africa': 'ZAF', 'Soviet Union': 'SVU', 'Spain': 'ESP', 'Special Categories': 'SPE', 'Sri Lanka': 'LKA', 'St. Kitts and Nevis': 'KNA', 'St. Lucia': 'LCA', 'St. Vincent and the Grenadines': 'VCT', 'Sudan': 'SDN', 'Suriname': 'SUR', 'Svalbard and Jan Mayen Is': 'SJM', 'Swaziland': 'SWZ', 'Sweden': 'SWE', 'Switzerland': 'CHE', 'Syrian Arab Republic': 'SYR', 'Taiwan': 'TWN', 'Tajikistan': 'TJK', 'Tanzania': 'TZA', 'Thailand': 'THA', 'Togo': 'TGO', 'Tokelau': 'TKL', 'Tonga': 'TON', 'Trinidad and Tobago': 'TTO', 'Tunisia': 'TUN', 'Turkey': 'TUR', 'Turkmenistan': 'TKM', 'Turks and Caicos Isl.': 'TCA', 'Tuvalu': 'TUV', 'Uganda': 'UGA', 'Ukraine': 'UKR', 'United Arab Emirates': 'ARE', 'United Kingdom': 'GBR', 'United States': 'USA', 'Unspecified': 'UNS', 'Uruguay': 'URY', 'Us Msc.Pac.I': 'USP', 'Uzbekistan': 'UZB', 'Vanuatu': 'VUT', 'Venezuela': 'VEN', 'Vietnam': 'VNM', 'Virgin Islands (U.S.)': 'VIR', 'Wake Island': 'WAK', 'Wallis and Futura Isl.': 'WLF', 'Western Sahara': 'ESH', 'World': 'WLD', 'Yemen Democratic': 'YDR', 'Yugoslavia': 'SER', 'FR (Serbia/Montene': 'YUG', 'Zambia': 'ZMB', 'Zimbabwe': 'ZWE'}

#list of OIC counties:
oic_countries = ['Azerbaijan', 'Jordan', 'Afghanistan', 'Albania', 'United Arab Emirates', 'Indonesia', 'Uzbekistan', 'Uganda', 'Iran', 'Pakistan', 'Bahrain', 'Brunei', 'Bangladesh', 'Benin', 'Burkina Faso', 'Tajikistan', 'Turkey', 'Turkmenistan', 'Chad', 'Togo', 'Tunisia', 'Algeria', 'Djibouti', 'Saudi Arabia', 'Senegal', 'Sudan', 'Syrian Arab Republic', 'Suriname', 'Sierra Leone', 'Somalia', 'Iraq', 'Oman', 'Gabon', 'Gambia', 'Guyana', 'Guinea', 'Guinea-Bissau', 'Comoros', 'Kyrgyz Republic', 'Qatar', 'Kazakhstan', 'Cameroon', "Cote d'Ivoire", 'Kuwait', 'Lebanon', 'Libya', 'Maldives', 'Mali', 'Malaysia', 'Egypt', 'Morocco', 'Mauritania', 'Mozambique', 'Niger', 'Nigeria', 'Yemen Rep.']

#list of important indicator ids:
default_indicators = ['NY.GDP.MKTP.CD', 'NY.GNP.MKTP.CD', 'FP.CPI.TOTL.ZG', 'GC.XPN.TOTL.GD.ZS', 'SE.ADT.LITR.ZS', 'EG.ELC.ACCS.ZS', 'EN.ATM.CO2E.PC', 'EN.ATM.GHGT.KT.CE', 'SL.UEM.TOTL.NE.ZS', 'SI.POV.NAHC', 'SP.DYN.TFRT.IN']
# default_indicators =

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


@st.cache_data
def metadata_info(id):
    return wb.series.metadata.get(id)

def more_info(meta_info):
    st.write("This data is about:")
    st.write(meta_info.metadata['Longdefinition'], "\n")
    st.write('Source:')
    st.write(meta_info.metadata['Source'])

@st.cache_data
def final_data(id, country, time_start, time_end):
    return wb.data.DataFrame(id, country, time=range(time_start, time_end, 1), labels=True)

def country_to_code(list_country):
    # Extract the codes of the countries based on the 'country_names' list
    country_codes_list = [iso3[name].lower() for name in list_country]
    return country_codes_list


@st.cache_data
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')



def main():
    
    #Setting up the page: 
    st.set_page_config(page_title="World Bank Indicator Simple Search")

#---------------------------------------------------------------------------------------------------------------------------------
    with st.sidebar:
        st.header(" World Bank Indicator Simple Search ")
        st.subheader("A work in progress by Anas AbdulBaqi")
        st.header("Enter information for data:")
        #User picks his topic
        topic_form = st.form("topic")
        topic = topic_form.text_input("Pick a topic to search:")

        #Search API for the results:
        if topic != "":
            search_results = search_web(topic)
            search_results_value = [item['value'] for item in search_results.items]
        search_done = topic_form.form_submit_button("Start the search!")


        #User selects data from the results
        text_form = st.form("form")
        if topic != "": 
            val = text_form.selectbox("select your indicator from the results:", search_results_value)
            selected_data = text_form.form_submit_button("Finished selecting data")

        
            new_results = [item for item in search_results.items if item['value'] in val]
            new_results_id = [item['id'] for item in new_results]
            if 'more_info' not in st.session_state:
                st.session_state.more_info = True

            if selected_data:
                st.session_state.more_info = True

            # if 'more_info' in st.session_state:
            #     if st.session_state.more_info == True:
            #         st.write("more information about your indicators:")

            #         #Option for more info about the data
            #         counter = 0
            #         for id in new_results_id:
            #             id_info = metadata_info(id)
            #             with st.expander(val):
            #                 id_info
            #             counter += 1
            #------------------Range and Country-----------------------------------------------------------
        if topic != "":
            #multiple countries ?
            country_form = st.form("country form")
            oic_all = country_form.checkbox('Select all member counties')
            oic_input = country_form.multiselect('Select from member countries:', oic_countries)
            country_input = country_form.multiselect('Select from non-member countries:', iso3.keys())

            if oic_all:
                oic_input = oic_countries
            
            country_all = country_to_code(country_input)
            country_oic = country_to_code(oic_input)

            time_start, time_end = country_form.slider("Select the time frame for your data:",
                                min_value=1960, max_value=2023,
                                value=(1990, 2010))
            
            time_start = int(time_start)
            time_end = int(time_end)
            st.write('Data from ', time_start, 'to', time_end)
            # Convert the output to integers
                           
            submitted = country_form.form_submit_button("Show my data!")
            if submitted == True:
                if 'submitted' not in st.session_state:
                    st.session_state.submitted = True

#--------------------------------------------------------------------------------------------------------------------------------
    #Display the results




    if topic != "":
        
        if time_start is not None:
            data_submitted = True
            if  'submitted' in st.session_state:
                counter = 0
                st.subheader('Your Data')
                for id in new_results_id:
                    with st.expander(val):
                        if country_oic != []:
                            st.write("Data for member countries:")
                            raw_data_m = final_data(id, country_oic, time_start, time_end)
                            your_data_mem = st.dataframe(raw_data_m)
                            st.download_button(
                                label="Download as CSV",
                                data=convert_df(raw_data_m),
                                file_name="member_data.csv",
                                mime='text/csv'
                            )
                        if country_all != []:
                            st.write("Data for non-member countries:")
                            raw_data_nonm = final_data(id, country_all, time_start, time_end)
                            your_data_nonm = st.dataframe(raw_data_nonm)
                            st.download_button(
                                label="Download as CSV",
                                data=convert_df(raw_data_nonm),
                                file_name="nonmember_data.csv",
                                mime='text/csv'
                            )
                        counter += 1

        st.subheader('Visualize the data')
        
        view_form = st.form("view form")
        view_form.write("Select countries to compare and visualize:")
        view_mem = view_form.multiselect("Select member countries:", oic_input)
        view_nonm = view_form.multiselect("Select non-memeber countries:", country_input)

        if 'ready_view' not in st.session_state:
                    st.session_state.ready_view = True
        ready_view = view_form.form_submit_button("Ready to compare")

        # #join 
        if ready_view == True:
            if country_oic != []:
                mem_df = raw_data_m[raw_data_m['Country'].isin(view_mem)]  
            if country_all != []:     
                nonm_df = raw_data_nonm[raw_data_nonm['Country'].isin(view_nonm)]

            if (country_oic != []) and (country_all != []):
                combined_df = pd.concat([mem_df, nonm_df], ignore_index=False)
            else:
                if country_oic != []:
                    combined_df = mem_df
                else:
                    combined_df = nonm_df

            #st.write(val)
            data_format = combined_df.melt(id_vars='Country', var_name='Years', value_name=val)
            # Create the Altair interactive chart with switched x-axis and column
            alt_circle = alt.Chart(data_format).mark_circle(size=100).encode(
                x='Years:N', # Use 'Value' as the x-axis
                y= val+':Q',          # Use 'Country' as the y-axis
                color='Country:N',
                tooltip=['Country:N',val+':Q', 'Years:N']
            )


            alt_line = alt.Chart(data_format).mark_line(size=1).encode(
                x='Years:N', # Use 'Value' as the x-axis
                y= val+':Q',          # Use 'Country' as the y-axis
                color='Country:N',
                tooltip=['Country:N',val+':Q', 'Years:N']
            )


            # Display the Altair chart
            final = alt.layer(
                alt_circle, alt_line
            ).properties(
                title=val,
                width=800,
                height=800
            ).interactive()

            st.altair_chart(final)

            with st.expander("Data used for visualization"):
                st.write(combined_df)




if __name__ == "__main__":
    main()