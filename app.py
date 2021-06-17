from PIL import Image, ImageDraw, ImageFont
import streamlit as st 
import time
import random
import pickle
import requests


hide_streamlit_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                </style>
                """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)


@st.cache(show_spinner=False)
def intro_image():
  font = ImageFont.truetype("NebulousRegular-54aV.ttf", 57)
  im = Image.new("RGB", (890, 100), "white")
  d = ImageDraw.Draw(im) 
  d.text((450, 60), "Identify Your Learning Style", fill="OrangeRed", anchor="ms", font=font)

  font = ImageFont.truetype("NebulousRegular-54aV.ttf", 605)
  im2 = Image.open('style.jpg')
  d = ImageDraw.Draw(im2) 
  d.text((1500, 850), "Learning", fill="LightYellow", anchor="ms", font=font)
  return im,im2

im , im2 = intro_image()

st.image(im, caption=None, use_column_width= True , clamp=False, channels='RGB', output_format='auto')
#st.image(im2, use_column_width= True )

st.subheader('This project is an implementation of Machine Learning Model to identify effective learning style in student centric learning')

st.markdown(""" | Visual      | Aural       | Read/write    | Kinesthetic    |
                | :---                                  |    :----:   |          ---: |          ---: |
                | visual learners like to be provided demonstrations and can learn through descriptions. They like to use lists to maintain pace and organise their thoughts. They remember faces but often forget names. They are distracted by movement or action but noise usually does not bother them. |aural learners learn by listening. They like to be provided with aural instructions. They enjoy aural discussions and  dialogues and prefer to work out problems by talking. They are easily distracted by noise. | read/write learners are note takers. They do best by  taking notes during a lecture or reading difficult material. They  often draw things to remember them. They do well with hands-on projects or tasks.      |learn best by doing. Their  preference is for hands-on experiences. They are often high  energy and like to make use of touching, moving and interacting  with their environment. They prefer not to watch or listen and  generally do not do well in the classroom.|




##### VARK model has four learning style categories : Aural, Kinesthetic, Reader & Visual \n 
A brief description of these learning styles can be found below: \n
 
1) Visual: visual learners like to be provided demonstrations and can \n
learn through descriptions. They like to use lists to maintain pace \n
and organise their thoughts. They remember faces but often forget \n
names. They are distracted by movement or action but noise \n
usually does not bother them. \n
2) Aural: aural learners learn by listening. They like to be provided\ n
with aural instructions. They enjoy aural discussions and \n
dialogues and prefer to work out problems by talking. They are \n
easily distracted by noise. \n
3) Read/write: read/write learners are note takers. They do best by \n
taking notes during a lecture or reading difficult material. They \n
often draw things to remember them. They do well with hands-on \n
projects or tasks. \n
4) Kinesthetic: kinesthetic learners learn best by doing. Their \n
preference is for hands-on experiences. They are often high \n
energy and like to make use of touching, moving and interacting \n
with their environment. They prefer not to watch or listen and \n
generally do not do well in the classroom. \n
Source: (www.geocities.com/-educationplace)      \n
A pre trained Decision Tree Model is running on the backend of this website\n
During evaluation of the model, it gave the following f1 score for the mentioned VARK categories respectively: \n
## [0.70, 0.65, 0.81, 0.81]""")

reader = ['R1.jpg', 'R2.jpg']
visual = ['V1.jpg', 'V2.jpg']
aural = ['A1.jpg', 'A2.jpg','A3.jpg','A4.jpg','A5.jpg']
kinesthetic = ['K1.jpg', 'K2.jpg','K3.jpg']

 
ph = st.empty()

ques = ["I like learning by visualization,  like use of pictures, videos, slides",
        "I like learning by using diagrams, graphs and charts",
        "I follow written directions better than oral directions",
        "I can better understand and follow directions using maps",
        "I like reading lists, bullet points and numbered paragraphs",
        "When learning from Internet, I like videos showing how to do",
        "I can remember more by listening than reading",
        ]
ques_id = {}
with ph.beta_container():
  genre = st.radio("From your understanding which of these is your most dominant learning style?",
                 options=['Visual', 'Aural', 'Reader','Kinesthetic'])   
  user_id = st.text_input("Provide email to recieve detail interpretation of our system", value="example@gmail.com", max_chars=20)
  for i in range(0, 7):
      st.subheader(ques[i])
      ques_id["ques{0}".format(i)]= st.radio(' ',('Strongly Disagree', 'Disagree', 'Neutral', 'Agree', 'Strongly Agree'),key='q'f'{i}')

 
#================================================
def one_pos():
  starting_list = []
  position_list = []
  for k in range(-1, 30, 5):
    starting_list.append(k)
  for u in range(0,7):
    if ques_id["ques{0}".format(u)] == 'Agree' :
      position_list.append((starting_list[u]+1))
    elif ques_id["ques{0}".format(u)] == 'Disagree' :
      position_list.append((starting_list[u]+2))  
    elif ques_id["ques{0}".format(u)] == 'Neutral' :
      position_list.append((starting_list[u]+3))
    elif ques_id["ques{0}".format(u)] == 'Strongly Agree' :
      position_list.append((starting_list[u]+4))
    elif ques_id["ques{0}".format(u)] == 'Strongly Disagree' :
      position_list.append((starting_list[u]+5))  
  
  rows, cols = (1, 35) 
  arr = [[0 for i in range(cols)] for j in range(rows)]
  for r in range(0,len(position_list)):
    arr[0][position_list[r]] = 1
  return arr
#================================================
placeholder = st.empty()  

if placeholder.button('Find Out'):
    
   placeholder.empty()
   pickle_in = open('learningpreference.pkl', 'rb') 
   classifier = pickle.load(pickle_in)
   X_test = one_pos()
   prediction = classifier.predict(X_test)
   res = ' '.join([str(elem) for elem in X_test[0]]) 
   my_bar = st.progress(0)
  
   for percent_complete in range(100):
        if percent_complete<55:
          time.sleep(0.5*(1.5/(1+percent_complete)))
        else:
          time.sleep(0.0002*(percent_complete))
        
        placeholder.write(f"Analyzing your learning style.. {percent_complete} % ⏳")
        my_bar.progress(percent_complete + 1)
        time.sleep(0.02)
        placeholder.empty()
   ph.empty()
   st.markdown("<h1 style='text-align: center; color: Tomato;'>✔️ Report is Ready</h1>", unsafe_allow_html=True)
   if prediction[0]== 0 :
      predic = 'Aural'
      st.markdown("<h1 style='text-align: center; color: Tomato;'>Aural method is your effective learning style 👂</h1>", unsafe_allow_html=True) 
      imagew = Image.open(random.choice(aural))
   elif prediction[0]== 1 :
      predic = 'Kinesthetic'
      st.markdown("<h1 style='text-align: center; color: Tomato;'>Kinesthetic method is your effective learning style 🛠️</h1>", unsafe_allow_html=True) 
      imagew = Image.open(random.choice(kinesthetic))
   elif prediction[0]== 2 :
      predic = 'Reading'
      st.markdown("<h1 style='text-align: center; color: Tomato;'>Reading method is your effective learning style 📖</h1>", unsafe_allow_html=True) 
      imagew = Image.open(random.choice(reader))
   elif prediction[0]== 3 :
      predic = 'Visual'
      st.markdown("<h1 style='text-align: center; color: Tomato;'>Visual method is your effective learning style 🗺️</h1>", unsafe_allow_html=True) 
      imagew = Image.open(random.choice(visual))
   st.image(imagew, use_column_width= True )
   requests.get('https://script.google.com/macros/s/AKfycbxQv4rcAD57LLBvjvZn4rLn03rjpauVLMvLdxaIB_eVsjRXyKKHw4QVK7XR6wFbJBJnOg/exec?tem='+genre+'&humid='+predic+'&res='+res+'&contid='+user_id+'&room=1')
   st.markdown("<h1 style='text-align: center; color: Tomato;'>Happy Learning ✒️</h1>", unsafe_allow_html=True) 
   st.button("Refresh")
