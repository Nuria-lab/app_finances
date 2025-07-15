from flask import Flask, render_template, request, redirect
import pandas as pd
import os
from datetime import datetime

app = Flask(__name__)
ARCHIVO = "finanzas.csv"

def cargar_datos():
    if os.path.exists(ARCHIVO):
        try:
            df = pd.read_csv(ARCHIVO)
            if df.empty:
                print("Archivo CSV vacío, creando DataFrame vacío con columnas.")
                df = pd.DataFrame(columns=["Fecha", "Tipo", "Categoria", "Descripcion", "Monto"])
        except pd.errors.EmptyDataError:
            print("Archivo CSV vacío, creando DataFrame vacío con columnas.")
            df = pd.DataFrame(columns=["Fecha", "Tipo", "Categoria", "Descripcion", "Monto"])
    else:
        print("No se encontró archivo, creando DataFrame vacío con columnas.")
        df = pd.DataFrame(columns=["Fecha", "Tipo", "Categoria", "Descripcion", "Monto"])
    return df


def guardar_datos(df):
    df.to_csv(ARCHIVO, index=False)

@app.route("/", methods=["GET", "POST"])
def index():
    df = cargar_datos()
    
    if request.method == "POST":
        tipo = request.form["tipo"]
        categoria = request.form["categoria"]
        descripcion = request.form["descripcion"]
        try:
            monto = float(request.form["monto"])
            if monto <= 0:
                raise ValueError
        except:
            return "Error: el monto debe ser un número positivo."
        
        nuevo = {
            "Fecha": datetime.today().strftime("%d-%m-%Y"),
            "Tipo": tipo,
            "Categoria": categoria,
            "Descripcion": descripcion,
            "Monto": monto
        }
        df = pd.concat([df, pd.DataFrame([nuevo])], ignore_index=True)
        guardar_datos(df)
        return redirect("/")

    ingresos = df[df["Tipo"] == "ingreso"]["Monto"].sum()
    gastos = df[df["Tipo"] == "gasto"]["Monto"].sum()
    saldo = ingresos - gastos

    return render_template("index.html", movimientos=df, saldo=saldo)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)