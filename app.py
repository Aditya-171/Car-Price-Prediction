from flask import Flask, render_template, request
import pickle
import numpy as np

clf = pickle.load(open('car_prediction_model.pkl','rb'))


app= Flask(__name__)

@app.route('/')
def home():
	return render_template('index_car.html')


@app.route('/predict', methods=['POST'])
def predict():
    if (request.method == 'POST'):
        km_driven=int(request.form['km_driven'])
        no_year = int(request.form['no_year'])
        Year=2020-no_year
        present_Price=float(request.form['present_price'])
        no_owner=request.form['no_owner']
        if(no_owner==0):
            no_owner=0
        if(no_owner==1):
            no_owner=1
        if(no_owner==3):
            no_owner=3
        
        fuel_type=request.form['fuel_type']
        if (fuel_type=="petrol"):
        	Fuel_Type_Petrol=1
        	Fuel_Type_Diesel=0
        elif(fuel_type=="diesel"):
        	Fuel_Type_Petrol=0
        	Fuel_Type_Diesel=1	
        else:
        	Fuel_Type_Petrol=0
        	Fuel_Type_Diesel=0 


        seller_type=request.form['seller_type']
        if (seller_type=="Individual"):
        	seller_type=1
        else:
        	seller_type=0
        Transmission_Mannual=request.form['Transmission_Mannual']
        if(Transmission_Mannual=='Mannual'):
        	Transmission_Mannual=1
        else:
        	Transmission_Mannual=0
      
        prediction=clf.predict([[present_Price,km_driven,no_owner,Year,Fuel_Type_Diesel,Fuel_Type_Petrol,seller_type,Transmission_Mannual]])
        output=round(prediction[0],2)

        if output<0:
        	return render_template('result_car.html',prediction_text='Sorry you cannot sell this car')
        else:
        	return render_template('result_car.html',prediction_text="You can sell this car at {} Lakhs".format(output))
    else:
    	return render_template('index_car.html')    


if __name__=="__main__":
	app.run()	