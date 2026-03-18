from flask import Flask, render_template, request
import pickle
import numpy as np

app = Flask(__name__)

model = pickle.load(open('model.pkl', 'rb'))

# Home page
@app.route('/')
def home():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():

    try:
        Administrative = float(request.form.get('Administrative',0))
        Administrative_Duration = float(request.form.get('Administrative_Duration',0))
        Informational = float(request.form.get('Informational',0))
        Informational_Duration = float(request.form.get('Informational_Duration',0))
        ProductRelated = float(request.form.get('ProductRelated',0))
        ProductRelated_Duration = float(request.form.get('ProductRelated_Duration',0))
        BounceRates = float(request.form.get('BounceRates',0))
        ExitRates = float(request.form.get('ExitRates',0))
        PageValues = float(request.form.get('PageValues',0))
        SpecialDay = float(request.form.get('SpecialDay',0))

        Month = request.form.get('Month')
        VisitorType = request.form.get('VisitorType')
        Weekend = request.form.get('Weekend')

        month_map = {'Feb':2,'Mar':3,'May':5,'June':6,'Jul':7,'Aug':8,'Sep':9,'Oct':10,'Nov':11,'Dec':12}
        visitor_map = {'Returning_Visitor':1,'New_Visitor':0,'Other':2}
        weekend_map = {'True':1,'False':0}

        Month = month_map.get(Month,0)
        VisitorType = visitor_map.get(VisitorType,0)
        Weekend = weekend_map.get(Weekend,0)

        features = np.array([[Administrative,Administrative_Duration,
                              Informational,Informational_Duration,
                              ProductRelated,ProductRelated_Duration,
                              BounceRates,ExitRates,PageValues,SpecialDay,
                              Month,VisitorType,Weekend]])

        prediction = model.predict(features)

        if prediction[0] == 1:
            output = "Customer WILL Purchase"
        else:
            output = "Customer will NOT Purchase"

        return render_template('index.html', prediction_text=output)

    except Exception as e:
        return str(e)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
