import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from plotly import graph_objs as go
from datetime import date
import streamlit as st

cursos = ['agricola'] #,"civil","eletrica","mecanica","petroleo","producao","quimica","rec_hidricos","telecom"]

dados = pd.read_excel('agricola.xlsx')

l_colunas = [ 'Horário Seg', 'Horário Ter', 'Horário Qua', 'Horário Qui', 'Horário Sex','Horário Sáb']



for i in l_colunas:
    horario1 = []
    horario2 = []
    for n in range(len(dados)):

        try:
            horario1.append(int(dados[i][n].split("-")[0].split(":")[0]))
            horario2.append(int(dados[i][n].split("-")[1].split(":")[0]))
        except:
            horario1.append("-")
            horario2.append("-")
        h1 = i +" "+ "inicial"
        h2 = i + " " + "final"
    dados[h1] = horario1
    dados[h2] = horario2


selec = ['Código Disciplina', 'Nome Disciplina', 'Código Turma',
        'CH Teóricas', 'CH Práticas', 'CH Estágio',
        'Horário Seg inicial', 'Horário Seg final',
       'Horário Ter inicial', 'Horário Ter final', 'Horário Qua inicial',
       'Horário Qua final', 'Horário Qui inicial', 'Horário Qui final',
       'Horário Sex inicial', 'Horário Sex final', 'Horário Sáb inicial',
       'Horário Sáb final']

colunas = dados.columns
b = colunas.isin(selec)
filtro = colunas[b]
dados_filtrado = dados[filtro]

col = ['Horário Seg inicial','Horário Ter inicial','Horário Qua inicial','Horário Qui inicial','Horário Sex inicial']
classificacao = [0 for a in  range(len(dados_filtrado))]
for i in col:
    for j in range(len(dados)):
        try:
            if int(dados_filtrado[i][j]) < 12:
                turno = "Manhã"
            if int(dados_filtrado[i][j]) >= 12 and int(dados_filtrado[i][j]) < 18:
                turno = "Tarde"
            if int(dados_filtrado[i][j]) >=18:
                turno = "Noite"

            classificacao[j] = turno
        except:
            pass


dados_filtrado['classificacao'] = classificacao


# Grafico 1

d_graf2 = dados_filtrado[['classificacao','Código Disciplina']].groupby(dados_filtrado['classificacao']).count()/len(dados_filtrado)
w = 0.25
x = np.arange(len(d_graf2))
layout = go.Layout(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)'
)
fig = go.Figure(data=[
    go.Bar(name="teste",x=['tarde'],y=[d_graf2['classificacao'][0]]),go.Bar(name="teste1",x=['manha'],y=[d_graf2['classificacao'][1]]),go.Bar(name="teste2",x=['noite'],y=[d_graf2['classificacao'][2]])
],layout=layout)
fig.update_xaxes(visible=False)
fig.update_yaxes(visible=False)
fig.update_layout_images(visible=False)

# Define o título do Dashboard

st.title("Projeto- Matérias")



empresa_selecionada = st.selectbox('Cursos',cursos)

st.plotly_chart(fig)
