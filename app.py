from PIL import Image, ImageDraw, ImageFont
import streamlit as st 
import time
import random
import pickle

hide_streamlit_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                </style>
                """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)


@st.cache(show_spinner=False)
def intro_image():
  font = ImageFont.truetype("NebulousRegular-54aV.ttf", 65)
  im = Image.new("RGB", (890, 100), "white")
  d = ImageDraw.Draw(im) 
  d.text((450, 60), "Identify Your", fill="OrangeRed", anchor="ms", font=font)

  font = ImageFont.truetype("NebulousRegular-54aV.ttf", 605)
  im2 = Image.open('style.jpg')
  d = ImageDraw.Draw(im2) 
  d.text((1500, 850), "Learning", fill="LightYellow", anchor="ms", font=font)
  return im,im2

im , im2 = intro_image()

st.image(im, caption=None, use_column_width= True , clamp=False, channels='RGB', output_format='auto')
st.image(im2, use_column_width= True )
with st.beta_expander("Take the quiz to find out | Expand to know more"):
      st.write("""
          This project is an implementation of Machine Learning Model to identify effective learning style in student centric learning
      """)
      st.markdown(""" ### VARK model has four learning style categories : Aural, Kinesthetic, Reader & Visual \n 
A pre trained Decision Tree Model is running on the backend of this website\n
During evaluation of the model, it gave the following f1 score for the mentioned VARK categories respectively: \n
## [0.70, 0.65, 0.81, 0.81]""")
      st.markdown(""" ## Authors : \n [Dr. Md. Rakibul Hoque](https://scholar.google.com/citations?user=3AwQ-8kAAAAJ&hl=en) \n 
[Dr. M. Helal Uddin Ahmed](https://www.du.ac.bd/faculty/faculty_details/MIS/743)""" )

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
        "I do better at academic subjects by listening to lectures",
        "I like listen to a good lecture than read about the same material",
        "I prefer listening a news on radio than reading it in a newspaper",
        "I like attending labs and practical session",
        "I like to make visuals (concept maps, charts, graphs and models)",
        "I like to participate in games for learning",
        ]
ques_id = {}
with ph.beta_container():
  for i in range(0, 13):
      st.subheader(ques[i])
      ques_id["ques{0}".format(i)]= st.radio(' ',('Strongly Disagree', 'Disagree', 'Neutral', 'Agree', 'Strongly Agree'),key='q'f'{i}')

 
#================================================
def one_pos():
  starting_list = []
  position_list = []
  for k in range(-1, 60, 5):
    starting_list.append(k)
  for u in range(0,13):
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
  
  rows, cols = (1, 65) 
  arr = [[0 for i in range(cols)] for j in range(rows)]
  for r in range(0,len(position_list)):
    arr[0][position_list[r]] = 1
  return arr
#================================================
placeholder = st.empty()  

if placeholder.button('Find Out'):
    
   placeholder.empty()
   pickle_in = open('classifier.pkl', 'rb') 
   classifier = pickle.load(pickle_in)
   X_test = one_pos()
   prediction = classifier.predict(X_test)
  
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
      st.markdown("<h1 style='text-align: center; color: Tomato;'>Aural method is your effective learning style 👂</h1>", unsafe_allow_html=True) 
      imagew = Image.open(random.choice(aural))
   elif prediction[0]== 1 :
      st.markdown("<h1 style='text-align: center; color: Tomato;'>Kinesthetic method is your effective learning style 🛠️</h1>", unsafe_allow_html=True) 
      imagew = Image.open(random.choice(kinesthetic))
   elif prediction[0]== 2 :
      st.markdown("<h1 style='text-align: center; color: Tomato;'>Reading method is your effective learning style 📖</h1>", unsafe_allow_html=True) 
      imagew = Image.open(random.choice(reader))
   elif prediction[0]== 3 :
      st.markdown("<h1 style='text-align: center; color: Tomato;'>Visual method is your effective learning style 🗺️</h1>", unsafe_allow_html=True) 
      imagew = Image.open(random.choice(visual))
   st.image(imagew, use_column_width= True )
   st.markdown("<h1 style='text-align: center; color: Tomato;'>Happy Learning ✒️</h1>", unsafe_allow_html=True) 
   st.button("Refresh")
