from flask import Flask, request, jsonify
import ydata_profiling
import pandas as pd

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    if file.filename.endswith('.csv') or file.filename.endswith('.parquet') or file.filename.endswith('.excel') or file.filename.endswith('.txt'):
        df = pd.read_csv(file)
        profile = df.profile_report()
        return jsonify(profile.to_html())
    else:
        return 'File type not supported.'

if __name__ == '__main__':
    app.run(debug=True)
