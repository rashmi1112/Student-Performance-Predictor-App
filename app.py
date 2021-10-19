from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import streamlit as st 
import pickle

pickle_in = open("logisticRegression.pkl","rb")
lg_model = pickle.load(pickle_in)

pickle_in1 = open("randomForest.pkl","rb")
randomForest = pickle.load(pickle_in1)

pickle_in2 = open("scaler.pkl","rb")
scaler = pickle.load(pickle_in2)


def welcome():
    return "Student Performance Predictor"

def convertPercentageToInt(string): 
    var_int = string[0:-1]
    return float(var_int)

def convertCGPA(cgpa, country):
    cgpa_str = cgpa
    if type(cgpa_str) == float: 
        cgpa = cgpa_str
    elif type(cgpa_str) == str:
        cgpa = convertPercentageToInt(cgpa_str)
    
    if country == 'India':
        uniform_cgpa = (cgpa / 10) * 4
        return uniform_cgpa
        
    if country == 'USA':
        return cgpa
      
    if country == 'UK': 
        if cgpa >= 70:
            return 4.0
        if cgpa > 65 and cgpa <= 69:
            return 3.7
        if cgpa > 60 and cgpa <= 65:
            return 3.3
        if cgpa > 55 and cgpa <= 60:
            return 3.0
        if cgpa > 50 and cgpa <= 55:
            return 2.7
        if cgpa > 45 and cgpa <= 50: 
            return 2.3
        if cgpa > 40 and cgpa <= 45: 
            return 2.0
        if cgpa >= 35 and cgpa <= 40: 
            return 1.0
        if cgpa < 35: 
            return 0 
    
    if country == 'Germany': 
        if cgpa >= 1 and cgpa < 1.3:
            return 4.0
        if cgpa >= 1.3 and cgpa < 1.7: 
            return 3.7
        if cgpa >= 1.7 and cgpa < 2.0: 
            return 3.3
        if cgpa >= 2 and cgpa < 2.3: 
            return 3.0
        if cgpa >= 2.3 and cgpa < 2.7: 
            return 2.7
        if cgpa >= 2.7 and cgpa < 3.0: 
            return 2.3
        if cgpa >= 3.0 and cgpa < 3.3: 
            return 2.0
        if cgpa >= 3.3 and cgpa < 3.7: 
            return 1.7
        if cgpa >= 3.7 and cgpa < 4.0: 
            return 1.3
        if cgpa >= 4.0 and cgpa < 5.0: 
            return 1.0
        if cgpa == 5: 
            return 0
    
    if country == 'Canada': 
        if cgpa >= 9 and cgpa <= 10:
            return 4.0
        if cgpa >= 8 and cgpa < 9: 
            return 3.67
        if cgpa >= 7 and cgpa < 8: 
            return 3.33
        if cgpa >= 6 and cgpa < 7: 
            return 3.0
        if cgpa >= 5 and cgpa < 6: 
            return 2.67
        if cgpa >= 4 and cgpa < 5: 
            return 2.33
        if cgpa >= 3 and cgpa < 4: 
            return 2.0
        if cgpa >= 2 and cgpa < 3: 
            return 1.67
        if cgpa >= 1 and cgpa < 2: 
            return 1.3
        if cgpa < 1: 
            return 0
        
    if country == 'Australia': 
        if cgpa >= 6 and cgpa <= 7:
            return 4.0
        if cgpa >= 5.5 and cgpa < 6: 
            return 3.70
        if cgpa >= 5 and cgpa < 5.5: 
            return 3.3
        if cgpa >= 4.5 and cgpa < 5: 
            return 3.0
        if cgpa >= 4 and cgpa < 4.5: 
            return 2.67
        if cgpa >= 3.5 and cgpa < 4: 
            return 2.33
        if cgpa >= 3 and cgpa < 3.5: 
            return 2.0
        if cgpa >= 2.5 and cgpa < 3: 
            return 1.67
        if cgpa >= 2 and cgpa < 2.5: 
            return 1.3
        if cgpa >= 1 and cgpa < 2:
            return 1.0
        if cgpa < 1: 
            return 0
       
    
    if country == 'Spain': 
        uniform_cgpa = (cgpa / 10) * 4
        return uniform_cgpa
        
    
    

def predict_student_performance(gre, toefl, cgpa, country, gpa):
    
    unif_gpa = convertCGPA(cgpa, country)
    entry = [[gre, toefl, unif_gpa, gpa]]
    scaled_entry = scaler.transform(entry)
    prediction_arr = randomForest.predict(scaled_entry)
    predicted_value = list(prediction_arr)[0]
    
    if predicted_value == 0:
        return 'Below Average'
    elif predicted_value == 1:
        return 'Above Average'
    elif predicted_value == 2:
        return 'Excellent'
    else:
        return 'Average'


def main():
    st.markdown(
    '<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.5.3/dist/css/bootstrap.min.css" integrity="sha384-TX8t27EcRE3e/ihU7zmQxVncDAy5uIKz4rEkgIXeMed4M0jlfIDPvg6uqKI2xXr2" crossorigin="anonymous">',unsafe_allow_html=True,)    
    
    query_params = st.experimental_get_query_params()
    tabs = ["Home", "About", "Contact"]
    
    if "tab" in query_params:
        active_tab = query_params["tab"][0]
    else:
        active_tab = "Home"

    if active_tab not in tabs:
        st.experimental_set_query_params(tab="Home")
        active_tab = "Home"

    li_items = "".join(
        f"""
        <li class="nav-item">
            <a class="nav-link{' active' if t==active_tab else ''}" href="/?tab={t}">{t}</a>
        </li>
        """
        for t in tabs
    )
    tabs_html = f"""
        <ul class= "nav justify-content-center"> 
        {li_items}
        </ul>
    """

    st.markdown(tabs_html, unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    if active_tab == "Home":
#         st.title()
        html_temp = """
        <div style="background-color:tomato;padding:10px">
        <h2 style="color:white;text-align:center;"> Student Perfromance Predictor App </h2>
        </div>
        """
        st.markdown(html_temp,unsafe_allow_html=True)
        gre = st.text_input("GRE Score (260-340)")
#         toefl = st.text_input("TOEFL Score (0-120)")
        toefl = st.slider("TOEFL Score", min_value=0, max_value=120, value=50,)
        country = st.selectbox('Country', ('India', 'USA', 'UK', 'Germany', 'Canada', 'Australia', 'Spain'))
        highest_degree = st.selectbox('Highest Degree Completed',('Bachelors','Masters','PHD'))
        cgpa = st.text_input("CGPA")
        gpa = st.text_input("GPA")
        result=""
        if st.button("Predict"):
            result=predict_student_performance(gre, toefl, cgpa, country, gpa)
            st.success('This student is {}'.format(result))   
                   
    elif active_tab == "About":
        st.title("This application was created as a part of Binghamton University Student Predictor Project. This application allows to predict the future performance of a student provided his/her eduction records. The final result lets a student to be categorized into one of the four groups mentioned below: ")
        one = """<h2 style="color:orange;text-align:center;"> 1. Excellent </h2>"""
        st.markdown(one, unsafe_allow_html=True)
        two = """<h2 style="color:orange;text-align:center;"> 2. Above Average </h2>"""
        st.markdown(two, unsafe_allow_html=True)
        three = """<h2 style="color:orange;text-align:center;"> 3. Average </h2>"""
        st.markdown(three, unsafe_allow_html=True)
        four = """<h2 style="color:orange;text-align:center;"> 4. Below Average </h2>"""
        st.markdown(four, unsafe_allow_html=True)
        
    elif active_tab == "Contact":
        st.write("Name:  Rashmi Badadale")
        email = """
        <a href = "mailto: rbadada1@binghamton.edu">Send Feedback</a>"""
        st.markdown(email, unsafe_allow_html=True)
        
                        
    else:
        st.error("Something has gone terribly wrong.")
                       
if __name__=='__main__':
    main()
