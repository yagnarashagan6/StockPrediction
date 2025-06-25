# 📦 Production Optimizer Web Application

A dynamic web application built with **Flask** to optimize product manufacturing based on available stock, using real-time data from an online Excel sheet.

## 🚀 Live Demo - https://production-optimizer-sy4k.onrender.com/

## 👨‍💻 Developed By
**Yagnarashagan C**  
[LinkedIn Profile](https://www.linkedin.com/in/yagna-rashagan-4a0431256)

---

## 🔍 Overview

This Flask-based tool streamlines production planning by calculating the maximum number of products that can be manufactured using current component stocks. It fetches data from a cloud-hosted Excel file and provides real-time updates, helping inventory managers and engineers make quick, informed decisions.

---

## ✨ Features

- 🔧 **Flask Backend** for seamless API management.
- 📊 **Excel Integration** via `pandas` & `openpyxl` for real-time data.
- 📈 **Dynamic Production Calculation** based on stock levels.
- 🧮 **Remaining Stock Analysis** after each production estimate.
- 🎛️ **User-Friendly UI** with clean dropdown-based interaction.
- ⚠️ **Error Handling** for invalid/missing inputs.
- 🧩 **Modular Architecture** with support for future upgrades (multi-product, gap analysis).

---

## 🛠️ Tech Stack

- **Frontend**: HTML, CSS, JavaScript  
- **Backend**: Python (Flask)  
- **Data Source**: Online Excel Sheet  
- **Libraries**: `pandas`, `openpyxl`, `flask`

---

## 🧠 Production Calculation Logic

1.Fetch Data: Load component stock and product requirements from the Excel file.

2.Component Limits: For each component, divide available stock by units required per product.

3.Find Bottleneck: Identify the lowest result — this limits total producible units.

4.Calculate Remaining Stock: Subtract used quantities from each component's stock.

5.Display Results: Show maximum production units and updated stock on the frontend.

![image](https://github.com/user-attachments/assets/bfcf63a5-205a-42c0-9d00-c2aceff6606a)
![image](https://github.com/user-attachments/assets/b47938b3-63b6-44ac-bcfd-0954abca1758)


---

## 📁 Project Structure
├── templates

├── index1.html # Frontend UI

    ├── python.py # Flask backend with logic
    ├── Book1.xlsx # Online Excel sheet (data source)

---

## 🔗 API Endpoints

- `GET /get-excel-data` — fetch product list  
- `POST /calculate` — compute production capacity + remaining stock

---

## 🔄 Future Enhancements

- ✅ independent calculation  
- 🔜 User-defined quantity input support  
- 🔜 Smart combined production mode  
 

---

## 📌 Conclusion

This project bridges inventory data with automated logic, reducing manual errors and helping organizations optimize production seamlessly. It’s ideal for small-scale manufacturers, inventory planners, and anyone looking to automate production decisions.

---

## 📎 GitHub Repository

[🔗 StockPrediction on GitHub](https://github.com/yagnarashagan6/StockPrediction)
