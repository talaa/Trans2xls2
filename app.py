from flask import Flask, render_template, request, jsonify
import docx2txt
import pandas as pd

app = Flask(__name__)

filename = None
table_html= None
df=None

def process_lines(lines):
    datetime_list, name_list, text_list = [], [], []

    for i in range(0, len(lines), 4):
        datetime_list.append(lines[i].strip())
        if i + 1 < len(lines):
            name_list.append(lines[i + 1].strip())
        else:
            name_list.append('')
        if i + 2 < len(lines):
            text_list.append(lines[i + 2].strip())
        else:
            text_list.append('')

    result_data = {'Datetime': datetime_list, 'Name': name_list, 'Text': text_list}
    return result_data

@app.route('/', methods=['GET', 'POST'])  # Add support for POST method

def index():
    # Initialize variables to None
    
    global filename, table_html, df 
    
    if request.method == 'POST':
        try:
            file = request.files['file']
            filename=file.filename
            content = docx2txt.process(file)
            lines = content.split('\n')  # Split content into lines
            result_data = process_lines(lines)
            df = pd.DataFrame(result_data)
            # Assuming the DataFrame is named 'df'
            last_entry = df['Datetime'].tail(1).values[0]
            
            table_html = df.to_html(classes='table table-striped', index=False)
            return render_template('index.html', table_html=table_html,filename=filename,last_entry=last_entry)
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)})
    return render_template('index.html')
@app.route('/run_code', methods=['POST'])
def run_code():
    global filename, df
    print("df:" , df)  # This code will now run when the button is clicked
    xlsx_name = f"{filename.rsplit('.', 1)[0]}.xlsx"

    df.to_excel(xlsx_name, index=False)
    return "Code executed successfully!"  # Send a response back to the client

if __name__ == '__main__':
    app.run(debug=True)