import pickle
import streamlit as st 
import numpy as np

with open('model_pickle','rb') as f:
    retrieved_model = pickle.load(f) 

def getSelection(value):
    return 1 if value == 'Yes' else 0

def getPropertyType(value):
    dict_propertytype = {'Apartment': 0,
        'Condominium': 1,
        # 'Flat': 2, 
        # 'Others': 3,  
        'Service Residence': 4}
    return dict_propertytype[value]  
 
def getState(value):
    dict_state = {'Johor': 0,
        'Kuala Lumpur': 1, 
        # 'Melaka': 2, 
        'Penang': 3,
        # 'Perak': 4,
        # 'Putrajaya': 5,
        # 'Sabah': 6, 
        'Selangor': 7}
    return dict_state[value]

def getYear(value):
    dict_year = {'1987': 0,
    '1989': 1, 
    '1992': 2,
    '1994': 3,
    '1995': 4,
    '1996': 5,
    '1997': 6,
    '1998': 7,
    '1999': 8,
    '2000': 9,
    '2001': 10,
    '2002': 11,
    '2003': 12,
    '2004': 13,
    '2005': 14,
    '2006': 15,
    '2007': 16,
    '2008': 17,
    '2009': 18,
    '2010': 19,
    '2011': 20,
    '2012': 21,
    '2013': 22,
    '2014': 23,
    '2015': 24,
    '2016': 25,
    '2017': 26,
    '2018': 27,
    '2019': 28,
    '2020': 29,
    '2021': 30,
    '2022': 31,
    '2023': 32,
    '2024': 33, 
    '2026': 34,
    'Flexible completion date' : 35}  # flexbile completion date = unknown 
    return dict_year[value]

def getLandTitle(value):
    dict_landtitle = {'Bumi Lot': 0, 'Malay Reserved': 1, 'Non Bumi Lot': 2}
    return dict_landtitle[value]

def getTenureType(value):
    dict_tenuretype = {'Freehold': 0, 'Leasehold': 1}
    return dict_tenuretype[value] 


def makePrediction(bedroom,bathroom,property_size,tenure,num_floor,property_type,num_parkinglot,land_title,bus_stop,mall,park,school,hospital,state,highway,year):
    
    encoded_tenure = getTenureType(tenure) 
    encoded_propertyType = getPropertyType(property_type)
    encoded_landTitle = getLandTitle(land_title)
    encoded_busStop = getSelection(bus_stop)
    encoded_mall = getSelection(mall)
    encoded_park = getSelection(park)
    encoded_school = getSelection(school) 
    encoded_hospital = getSelection(hospital)  
    encoded_state = getState(state) 
    encoded_highway = getSelection(highway) 
    encoded_year = getYear(year)

    features = [bedroom,bathroom,property_size,encoded_tenure,num_floor,encoded_propertyType,num_parkinglot,
                encoded_landTitle,encoded_busStop,encoded_mall,encoded_park,encoded_school,encoded_hospital,
                encoded_state,encoded_highway,encoded_year] 
    
    predicted_price = retrieved_model.predict([features]) 

    return np.exp(predicted_price) 
 

def main():

    st.title("Malaysia Property Prices Forecast") 

    # Form section
    with st.form(key='form1',clear_on_submit=True):
        
        st.subheader("**General Information**")  

        property_type = st.selectbox('Property type',('Apartment','Condominium','Service Residence'), index=None, placeholder="Select a property type",) 

        property_size = st.number_input("Property Size (in range of 400 to 1500)", min_value=400, max_value=1500, value=400, step=1)
        
        num_floor = st.number_input("Number of floors (in range of 15 to 45 )",min_value=15, max_value=45, value=15, step=1)

        bedroom_val = st.number_input("Number of bedrooms (in range of 2 to 5 )",min_value=2, max_value=5, value=2, step=1) 

        bathroom_val = st.number_input("Number of bathrooms (in range of 1 to 4 )",min_value=1, max_value=4, value=1, step=1)  

        num_parkinglot = st.number_input("Number of allocated parking lot (in range of 1 to 3 )",min_value=1, max_value=3, value=1, step=1)  
        
        state = st.selectbox('State',('Johor', 'Kuala Lumpur','Penang','Selangor'), index=None, placeholder="Select a state",) 

        completion_year = st.selectbox("Expected completion year", 
                                    ('Flexible completion date','2026', '2024', '2023', '2022', '2021', '2020', '2019', '2018', '2017', '2016', '2015', '2014', '2013', '2012', '2011', '2010', '2009', '2008', '2007', '2006', '2005', '2004', '2003', '2002', '2001', '2000', '1999', '1998', '1997', '1996', '1995', '1994', '1992', '1989', '1987'),
                                    index=None, placeholder="Select expected completion year",) 


        tenure = st.selectbox('Tenure type',('Freehold','Leasehold'), index=None, placeholder="Select a tenure type",)

        land_title = st.selectbox('Land title',('Bumi Lot','Non Bumi Lot','Malay Reserved'), index=None, placeholder="Select a land title",)

        selection = ["Yes","No"]

        st.subheader("**Nearby Facilities**") 

        col1, col2 = st.columns(2) 
        with col1:
            bus_stop_page = st.radio("Bus stop",selection,index=None)
            mall_page = st.radio("Mall",selection,index=None) 
            park_page = st.radio("Park",selection,index=None)  

        with col2: 
            school_page = st.radio("School",selection,index=None)
            hospital_page = st.radio("Hospital",selection,index=None) 
            highway_page = st.radio("Highway",selection,index=None)  

        predict_btn = st.form_submit_button(label="Predict", type="primary",use_container_width=True)  

    # Prediction section
    if predict_btn: 
        # Check for missing values
        if not (property_type and property_size and num_floor and state and completion_year and bedroom_val and bathroom_val and num_parkinglot and tenure and land_title and bus_stop_page and mall_page 
                and park_page and school_page and hospital_page and highway_page):
            st.warning("Please fill in all the fields before predicting.") 
        else: 
            
            output = round(makePrediction(bedroom_val,bathroom_val,property_size,tenure,num_floor,property_type,
                                          num_parkinglot,land_title,bus_stop_page,mall_page,park_page,school_page,hospital_page,state,highway_page,completion_year)[0],2) 


            st.success("Prediction Successful!") 

            st.subheader("General Information")    
            st.write(f'Property type         : {property_type}')   
            st.write(f'Property size         : {property_size}')
            st.write(f'Number of floors      : {num_floor}')
            st.write(f'Number of bedrooms    : {bedroom_val}')
            st.write(f'Number of bathrooms   : {bathroom_val}')
            st.write(f'Number of parking lot : {num_parkinglot}')
            st.write(f'State                 : {state}')   
            st.write(f'Completion Year       : {completion_year}')   
            st.write(f'Tenure                : {tenure}')   
            st.write(f'Land Title            : {land_title}')   
            st.subheader("Nearby facilities")        
            st.write(f'Bus stop : {bus_stop_page}')  
            st.write(f'Mall     : {mall_page}')  
            st.write(f'Park     : {park_page}')  
            st.write(f'School   : {school_page}')  
            st.write(f'Hospital : {hospital_page}')  
            st.write(f'Highway  : {highway_page}') 
            
            st.success(f'Predicted price : RM {output}') 
    
    
if __name__ == '__main__': 
    main()  

