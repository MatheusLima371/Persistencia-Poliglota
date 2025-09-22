# Projeto de Persistência Poliglota com MongoDB + SQLite + Streamlit
# Autor: Matheus Cândido Carneiro Lima – RGM: 35593229

import sqlite3
from pymongo import MongoClient
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Persistência Poliglota", layout="wide")
st.title("Projeto de Persistência Poliglota com MongoDB + SQLite")

conn = sqlite3.connect('dados.db')
cursor = conn.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS cidades (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT,
    estado TEXT,
    pais TEXT
)
''')
conn.commit()

st.subheader("Cadastrar cidades no SQLite")
with st.form("form_sqlite"):
    nome_cidade = st.text_input("Nome da cidade")
    estado = st.text_input("Estado")
    pais = st.text_input("País")
    submit_sqlite = st.form_submit_button("Salvar cidade")

if submit_sqlite and nome_cidade and estado and pais:
    cursor.execute("INSERT INTO cidades (nome, estado, pais) VALUES (?, ?, ?)",
                   (nome_cidade, estado, pais))
    conn.commit()
    st.success(f"Cidade '{nome_cidade}' cadastrada com sucesso!")

cursor.execute("SELECT * FROM cidades")
dados_sqlite = cursor.fetchall()
if dados_sqlite:
    st.write("📋 Cidades cadastradas (SQLite):")
    df_sqlite = pd.DataFrame(dados_sqlite, columns=["ID", "Nome", "Estado", "País"])
    st.dataframe(df_sqlite)

st.subheader("Cadastrar coordenadas no MongoDB")
mongo_uri = "mongodb://localhost:27017/"
client = MongoClient(mongo_uri)
db = client['geodados']
colecao = db['coordenadas']

with st.form("form_mongo"):
    nome_local = st.text_input("Nome do local")
    latitude = st.number_input("Latitude", format="%.6f")
    longitude = st.number_input("Longitude", format="%.6f")
    descricao = st.text_area("Descrição")
    submit_mongo = st.form_submit_button("Salvar coordenadas")

if submit_mongo and nome_local and descricao:
    doc = {
        "nome": nome_local,
        "coordenadas": {
            "latitude": latitude,
            "longitude": longitude
        },
        "descricao": descricao
    }
    colecao.insert_one(doc)
    st.success(f"Coordenadas de '{nome_local}' salvas no MongoDB!")

dados_mongo = list(colecao.find())

if dados_mongo:
    st.write("📋 Locais cadastrados (MongoDB):")
    df_mongo = pd.DataFrame([
        {
            "Nome": d.get("nome"),
            "Latitude": d["coordenadas"]["latitude"],
            "Longitude": d["coordenadas"]["longitude"],
            "Descrição": d.get("descricao", "")
        } for d in dados_mongo
    ])
    st.dataframe(df_mongo)

    st.subheader("🗺️ Visualização no mapa")
    coords = pd.DataFrame([
        {
            "lat": d["coordenadas"]["latitude"],
            "lon": d["coordenadas"]["longitude"]
        } for d in dados_mongo
    ])
    st.map(coords)

conn.close()
st.info("💡 Dica: preencha algumas cidades e coordenadas para ver o mapa funcionando.")
