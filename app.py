from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

def predict_breast_cancer(data):
    risk_factors = {
        'age': {'safe': [0, 50], 'weight': 1},
        'tumor_size': {'safe': [0, 2], 'weight': 2},
        'lymph_nodes': {'safe': [0, 0], 'weight': 3},
        'histological_grade': {'safe': [1, 1], 'weight': 2},
        'er_status': {'safe': [1, 1], 'weight': 1},
        'pr_status': {'safe': [1, 1], 'weight': 1},
        'her2_status': {'safe': [0, 0], 'weight': 2},
        'ki67_index': {'safe': [0, 10], 'weight': 2},
        'p53_status': {'safe': [0, 0], 'weight': 2}
    }
    
    risk_score = 0
    total_weight = 0

    for factor, info in risk_factors.items():
        total_weight += info['weight']
        if not (info['safe'][0] <= data[factor] <= info['safe'][1]):
            risk_score += info['weight']

    risk_percentage = (risk_score / total_weight) * 100
    return round(risk_percentage, 2)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.form.to_dict()
    data = {key: float(value) for key, value in data.items()}
    prediction = predict_breast_cancer(data)
    return jsonify({'prediction': prediction})

if __name__ == '__main__':
    app.run(debug=True)
