from flask import Flask, render_template, request, url_for
from keras.models import load_model
from keras.preprocessing import image
from flask import send_file
import numpy as np
app = Flask(__name__)
dic={0:'Dorje', 1:'Rosary', 2:'Mikky offering bowl', 3:'Incense burner', 4:'Butter lamp', 5:'Bumpa',6:'Unknown'}

model=load_model('finalmodeldor.h5')
model.make_predict_function()

def predict_label(img_path):
   i=image.load_img(img_path, target_size=(224,224))
   i=image.img_to_array(i)
   i=np.expand_dims(i, axis=0)
   i=i.reshape(1, 224, 224, 3)
   p=model.predict(i)
   
   list_index=[0,1,2,3,4,5,6]
   x=p

   for i in range(7):
      for j in range(7):
         if x[0][list_index[i]] > x[0][list_index[j]]: 
            temp = list_index[i] 
            list_index[i]= list_index[j]
            list_index[j]=temp
   
   for i in range(1):
      # return(dic[list_index[i]], ':', round(p[0][list_index[i]]*100,2), '%')
      return(dic[list_index[i]])


   #print(p)
   #return dic[p[0]]

@app.route('/', methods=['GET', 'POST'])
def main():
   return render_template('Website.html')


@app.route("/submit", methods=['GET','POST'])
def get_output():
   if request.method=='POST':
      img = request.files['my_image']

      img_path="./static/images/" + img.filename
      img.save(img_path)

      p=predict_label(img_path)

   return render_template("Website.html",prediction = p, img_path = img_path)

@app.route('/details', methods=['GET'])
def details():
   return render_template('cardview.html')

@app.route('/about', methods=['GET'])
def about():
   return render_template('profile.html')

@app.route('/explanationbumpa', methods=['GET'])
def explanationbumpa():
   return render_template('BumpaExplanation.html')

@app.route('/explanationincense', methods=['GET'])
def explanationincense():
   return render_template('incenseexplanation.html')

@app.route('/explanationvajra', methods=['GET'])
def explanationvajra():
   return render_template('vajraexplanation.html')

@app.route('/explanationbutterlamp', methods=['GET'])
def explanationbutterlamp():
   return render_template('butterlampexplanation.html')

@app.route('/explanationmikkyoffering', methods=['GET'])
def explanationmikkyoffering():
   return render_template('mikkyexplanation.html')

@app.route('/explanationrosary', methods=['GET'])
def explanationrosary():
   return render_template('rosaryexplanation.html')

@app.route("/remove", methods=['GET','POST'])
def remove():
  return render_template("Website.html")

if __name__ == '__main__':
   app.run(debug=True)


