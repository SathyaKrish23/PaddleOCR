# FastAPI OCR Service

This repository contains a **FastAPI-based OCR (Optical Character Recognition) service** built using **PaddleOCR**. The application exposes APIs to upload files (images/PDFs) and extract text efficiently.

---

## 📌 Features

* Fast and accurate OCR using **PaddleOCR**
* REST APIs built with **FastAPI**
* Supports file uploads via `multipart/form-data`
* Easy to deploy and extend
* Optimized for Python **3.10**

---

## 🧰 Tech Stack

* **Python** 3.10
* **FastAPI** – API framework
* **PaddleOCR** – Text detection & recognition
* **PaddlePaddle** – Deep learning backend
* **Uvicorn** – ASGI server

---

## ✅ Requirements

### Python Version

```text
Python 3.10
```

### Python Modules

```text
fastapi
paddleocr
paddlepaddle==3.2.1
uvicorn
python-multipart
```

---

## 📦 Installation

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd <your-repo-folder>
```

### 2. Create Virtual Environment (Recommended)

```bash
python -m venv venv
```

Activate the environment:

**Windows**

```bash
venv\Scripts\activate
```

**Linux / macOS**

```bash
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install --upgrade pip
pip install fastapi paddleocr paddlepaddle==3.2.1 uvicorn python-multipart
```

---

## ▶️ Running the Application

Make sure `main.py` exists in the root directory.

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

---

## 🌐 API Documentation

Once the server is running, open:

* **Swagger UI:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
* **ReDoc:** [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## 📤 Example Usage

Upload an image or document using the API endpoint defined in `main.py`.

Example (via Swagger UI):

1. Open `/docs`
2. Select the OCR endpoint
3. Upload file
4. Get extracted text as JSON

---

## 📁 Project Structure

```text
.
├── main.py          # FastAPI application entry point
├── README.md        # Project documentation
├── venv/            # Virtual environment (optional)
```

---

## ⚠️ Notes

* Ensure compatible PaddlePaddle version (`3.2.1`) is used to avoid runtime issues.
* For GPU support, install the appropriate PaddlePaddle GPU package.
* First OCR request may take longer due to model loading.

---

## 🤝 Contribution

Feel free to fork the repository and submit pull requests for improvements or bug fixes.

---

## 📜 License

This project is open-source and available for educational and commercial use.

---

**Happy Coding 🚀**
