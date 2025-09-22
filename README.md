# Projeto Persistência Poliglota com MongoDB + SQLite + Streamlit

## Autor
Matheus Cândido Carneiro Lima 

## Descrição
Este projeto demonstra persistência poliglota usando:
- SQLite para dados estruturados (cidades)
- MongoDB para dados geoespaciais
- Streamlit para interface web

## Como rodar

1. Instale as bibliotecas necessárias:
   ```bash
   pip install streamlit pymongo pandas
   ```

2. Configure o MongoDB (local ou Atlas). O link padrão no `app.py` é `mongodb://localhost:27017/`.

3. Rode o app:
   ```bash
   streamlit run app.py
   ```

4. Abra no navegador o link que o Streamlit mostrar (normalmente `http://localhost:8501`).

## Arquivos incluídos
- app.py — código principal
- dados.db — banco SQLite inicial
- README.md — instruções de uso
