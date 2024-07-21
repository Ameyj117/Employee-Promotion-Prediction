import pickle
from flask import Flask, render_template, request

# Load the model
model = pickle.load(open('Flask/model.pkl', 'rb'))

app = Flask(__name__)

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/predict')
def predict():
    return render_template('predict.html')

@app.route('/pred', methods=['POST'])
def pred():
    # Extract form data
    department = request.form['department']
    education = request.form['education']
    no_of_trainings = request.form['no_of_trainings']
    age = request.form['age']
    previous_year_rating = request.form['previous_year_rating']
    length_of_service = request.form['length_of_service']
    KPIs = request.form['KPIs']
    awards_won = request.form['awards_won']
    avg_training_score = request.form['avg_training_score']
    
    # Convert categorical variables to numerical
    department_dict = {'Sales': 1, 'Technical': 2, 'Support': 3}
    department = department_dict.get(department, 0)  # Default to 0 if not found
    
    education = int(education)
    KPIs = int(KPIs)
    awards_won = int(awards_won)
    
    # Convert all values to float for prediction
    total = [[department, education, float(no_of_trainings), float(age), 
              float(previous_year_rating), float(length_of_service),
              KPIs, awards_won, float(avg_training_score)]]
    
    # Make prediction
    prediction = model.predict(total)
    
    # Determine result text
    if prediction[0] == 0:
        text = 'Sorry, you are not eligible for promotion'
    else:
        text = 'Great, you are eligible for promotion'
    
    return render_template('submit.html', predictionText=text)

if __name__ == '__main__':
    app.run(debug=True)





