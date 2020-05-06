import pandas as pd
import numpy as np
from sklearn import tree
import csv
from csv import writer
df= pd.read_csv('test1.csv')
df['Type']= df['Type'].str.lower()

df['Blend']= df['Blend'].str.lower()
x=df.iloc[:,0:4].values
y=df.iloc[:,4:].values

from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()
x[:, 1] = le.fit_transform(x[:, 1])
x[:, 0] = le.fit_transform(x[:, 0])
clf = tree.DecisionTreeRegressor()

clf = clf.fit(x, y)
myf=open('test.csv', 'wb')
myf.close()
from flask import Flask, render_template, request
app = Flask(__name__)
result=[]
@app.route('/')
def student():
   
   return render_template('student.html')

@app.route('/result',methods = ['POST', 'GET'])
def result():
   if request.method == 'POST':
      myfile = open('test.csv','w+')
     
      myfile.write("Type,Blend,Compression ratio,Load\n")
      Type = str(request.form["T"])
      myfile.write("%s"%(Type))
      myfile.write(",")
     
      Blend = str(request.form["B"])
      myfile.write("%s"%(Blend))
      myfile.write(",")
      
      
      Cr=int(request.form["CR"])
      myfile.write("%d"%(Cr))
      myfile.write(",")
    
      Load=int(request.form["L"])
      myfile.write("%d"%(Load))
      
      def append_list_as_row(file_name, list_of_elem):
    # Open file in append mode
         with open(file_name, 'a+') as write_obj:
        # Create a writer object from csv module
            csv_writer = writer(write_obj)
        # Add contents of list as last row in the csv file
            csv_writer.writerow(list_of_elem)
      
      
      myfile.close()
      df= pd.read_csv('test.csv')
      df['Type'] = df['Type'].str.lower()
      df['Blend']= df['Blend'].str.lower()
      print(df)
      x=df.iloc[:,0:4].values
      x[:, 1] = le.fit_transform(x[:, 1])
      x[:, 0] = le.fit_transform(x[:, 0])
      print(x)
      res=clf.predict(x)
      li=[Type,Blend,Cr,Load,res[0,0],res[0,1],res[0,2],res[0,3],res[0,4]]
      append_list_as_row('db.csv', li)
      return render_template("result.html",HC=res[0,0],CO=res[0,1],CO2=res[0,2],O2=res[0,3],Nox=res[0,4])

if __name__ == '__main__':
   app.run(debug = True)
