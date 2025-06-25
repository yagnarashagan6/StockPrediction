from flask import Flask, jsonify, render_template, request
import pandas as pd
import os
from werkzeug.exceptions import BadRequest

app = Flask(__name__, static_folder='static', template_folder='templates')

EXCEL_PATH = os.path.join(os.path.dirname(__file__), 'Book1.xlsx')

@app.route('/')
def index():
    return render_template('index1.html')

@app.route('/get-excel-data', methods=['GET'])
def get_excel_data():
    try:
        df = pd.read_excel(EXCEL_PATH, sheet_name='Sheet1', engine='openpyxl')
        df.columns = df.columns.str.strip()
        iphone_models = df.columns[1:-1].tolist()  # Skip 'component' and 'stocks'
        return jsonify({'iphone_models': iphone_models})
    except FileNotFoundError:
        return jsonify({'error': f'Error: The file "Book1.xlsx" was not found.'}), 500
    except Exception as e:
        return jsonify({'error': f'Error reading Excel file: {str(e)}'}), 500

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.json
    selected_iphone = data.get('product')

    if not selected_iphone:
        raise BadRequest('No product selected')

    try:
        df = pd.read_excel(EXCEL_PATH, sheet_name='Sheet1', engine='openpyxl')
        df.columns = df.columns.str.strip()

        if selected_iphone not in df.columns:
            return jsonify({'error': f'"{selected_iphone}" not found in Excel columns'}), 400

        product_col = selected_iphone
        stock_col = df.columns[-1]

        component_df = df.iloc[0:11]  # Rows 0–10 for components

        requirements = pd.to_numeric(component_df[product_col].fillna(0), errors='coerce').fillna(0)
        stock = pd.to_numeric(component_df[stock_col].fillna(0), errors='coerce').fillna(0)

        quotients = []
        for r, s in zip(requirements, stock):
            if r > 0:
                quotients.append(s // r)
        possible_units = int(min(quotients)) if quotients else 0

        remaining_stock_list = stock - (requirements * possible_units)
        remaining_stock_list = remaining_stock_list.apply(lambda x: max(x, 0)).astype(int)

        # ✅ Include all components, even unused ones (to match full total stock logic)
        remaining_stock_dict = {
            str(component_df.iloc[i, 0]): int(remaining_stock_list.iloc[i])
            for i in range(len(remaining_stock_list))
        }

        return jsonify({
            'possible_production_units': possible_units,
            'remaining_stock': remaining_stock_dict
        })

    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)
