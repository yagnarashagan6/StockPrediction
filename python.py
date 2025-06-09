from flask import Flask, jsonify, render_template, request
import pandas as pd
import os
from werkzeug.exceptions import BadRequest

app = Flask(__name__, static_folder='static', template_folder='templates')

# --- Configuration ---
# The path to your Excel file.
# This makes sure the script can find "Book1.xlsx" in the same folder.
EXCEL_PATH = os.path.join(os.path.dirname(__file__), 'Book1.xlsx')
IPHONE_MODELS_COLUMN_RANGE = slice(1, 17)  # Columns B to Q for iPhone models
POSSIBLE_PRODUCTION_ROW = 11  # Row 12 in Excel (index 11)
REMAINING_STOCK_ROW = 13      # Row 14 in Excel (index 13)

# --- Routes ---

@app.route('/')
def index():
    """Render the main HTML page."""
    return render_template('index.html')

@app.route('/get-excel-data', methods=['GET'])
def get_excel_data():
    """Read the Excel file and return the list of iPhone models."""
    try:
        # Read the Excel file every time this is called
        df = pd.read_excel(EXCEL_PATH, sheet_name='Sheet1', engine='openpyxl')
        df.columns = df.columns.str.strip()

        # Extract iPhone model names from the header row (columns B to Q)
        iphone_models = df.columns[IPHONE_MODELS_COLUMN_RANGE].tolist()
        return jsonify({'iphone_models': iphone_models})

    except FileNotFoundError:
        return jsonify({'error': f'Error: The file "Book1.xlsx" was not found.'}), 500
    except Exception as e:
        return jsonify({'error': f'Error reading Excel file: {str(e)}'}), 500

@app.route('/calculate', methods=['POST'])
def calculate():
    """Calculate production and stock for a selected iPhone."""
    data = request.json
    selected_iphone = data.get('product')

    if not selected_iphone:
        raise BadRequest('No product selected')

    try:
        # Re-reads the Excel file on every calculation to get the latest data.
        df = pd.read_excel(EXCEL_PATH, sheet_name='Sheet1', engine='openpyxl', header=0)
        df.columns = df.columns.str.strip()

        if selected_iphone not in df.columns:
            return jsonify({'error': f'"{selected_iphone}" not found in Excel columns'}), 400

        # Get the column index for the selected iPhone
        col_idx = df.columns.get_loc(selected_iphone)

        # Get possible production units from Row 12 (index 11)
        # .iloc uses 0-based indexing, so row 12 is at index 11.
        prod_value = df.iloc[POSSIBLE_PRODUCTION_ROW, col_idx] if len(df) > POSSIBLE_PRODUCTION_ROW else 0
        possible_production_units = int(prod_value) if pd.notna(prod_value) else 0

        # Get remaining stock from Row 14 (index 13)
        # .iloc uses 0-based indexing, so row 14 is at index 13. This is the corrected part.
        stock_value = df.iloc[REMAINING_STOCK_ROW, col_idx] if len(df) > REMAINING_STOCK_ROW else 0
        remaining_stock = int(stock_value) if pd.notna(stock_value) else 0

        return jsonify({
            'possible_production_units': possible_production_units,
            'remaining_stock': remaining_stock
        })

    except FileNotFoundError:
        return jsonify({'error': 'Error: "Book1.xlsx" not found. Make sure the file is in the same directory.'}), 500
    except Exception as e:
        return jsonify({'error': f'An error occurred during calculation: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)