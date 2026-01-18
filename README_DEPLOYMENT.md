# Deployment Instructions (Render.com)

1.  **GitHub Repository**
    *   Create a new repository on GitHub.
    *   Push all files in this directory to the repository.
    *   Ensure the structure looks like this:
        ```
        /
        ├── app.py
        ├── requirements.txt
        ├── Procfile
        ├── model/
        │   ├── model_development.py
        │   └── house_price_model.pkl
        ├── static/
        │   └── style.css
        ├── templates/
        │   └── index.html
        └── ...
        ```

2.  **Render.com**
    *   Sign up/Login to [Render.com](https://render.com).
    *   Click "New +" -> "Web Service".
    *   Connect your GitHub repository.
    *   Give it a name (e.g., `house-price-prediction`).
    *   **Runtime**: Python 3
    *   **Build Command**: `pip install -r requirements.txt`
    *   **Start Command**: `gunicorn app:app`
    *   Click "Create Web Service".

3.  **Finalization**
    *   Wait for the deployment to finish.
    *   Copy the URL (e.g., `https://house-price-prediction.onrender.com`).
    *   Fill in the `HousePrice_hosted_webGUI_link.txt` file with your details and this URL.

## Local Test
To test locally:
```bash
pip install -r requirements.txt
python app.py
```
Open http://127.0.0.1:5000 in your browser.
