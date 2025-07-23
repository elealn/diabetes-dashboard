# -*- coding: utf-8 -*-
from flask import Flask, render_template, request
import pandas as pd
import joblib
import plotly.express as px
import plotly
import json

app = Flask(__name__)

# Cargar modelo
model = joblib.load("model/model.pkl")

@app.route("/", methods=["GET", "POST"])
def index():
    resultado = None
    fig_json = None

    if request.method == "POST":
        features = [float(request.form[col]) for col in ['age', 'bmi', 'bp']]
        df_pred = pd.DataFrame([features], columns=['age', 'bmi', 'bp'])
        pred = model.predict(df_pred)[0]
        resultado = f"Riesgo estimado de diabetes: {pred:.2f}"

    # Mostrar grafico dummy (para ejemplo)
    df_demo = pd.DataFrame({
        "Variable": ["Age", "BMI", "BP"],
        "Valor Promedio": [0.03, 0.04, 0.05]
    })
    fig = px.bar(df_demo, x="Variable", y="Valor Promedio", title="Variables promedio")
    fig_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template("index.html", resultado=resultado, fig=fig_json)

if __name__ == "__main__":
    #app.run(debug=True)
    import os
    port = int(os.environ.get("PORT", 5000))  # Render asigna un puerto automáticamente
    app.run(debug=False, host="0.0.0.0", port=port)
