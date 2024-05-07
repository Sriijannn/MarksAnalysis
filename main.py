from flask import Flask, render_template, request, jsonify
import pandas as pd

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    if file:
        data = pd.read_csv(file)
        
        
        data.dropna(axis=0, how='all', inplace=True)
        data.dropna(axis=1, how='all', inplace=True)
        
        
        grouped_data = data.groupby(['Name', 'Subject']).agg({'Marks': 'mean', 'Total Marks': 'first'}).reset_index()
        
     
        grouped_data = grouped_data.groupby('Name').agg({'Subject': lambda x: list(x), 'Marks': lambda x: list(x), 'Total Marks': 'mean'}).reset_index()
        
        charts_data = []
        
        for index, row in grouped_data.iterrows():
            chart_data = {
                'name': row['Name'],
                'subjects': row['Subject'],
                'marks': row['Marks'],
                'average_total_marks': row['Total Marks']
            }
            
            charts_data.append(chart_data)
        
        return jsonify({'data': charts_data})

if __name__ == '__main__':
    app.run(debug=True)
