# Heart Stroke Prediction Streamlit App

Place the trained model, scaler and columns pickle files in this folder before running.

Expected files (examples):
- `knn_heart_model.pkl` (or any .pkl containing 'knn'/'heart'/'model')
- `scaler.pkl` (or any .pkl containing 'scaler')
- `columns.pkl` (or any .pkl containing 'column'/'columns')

Install dependencies and run:

```powershell
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

The app will be available at `http://localhost:8501`.
