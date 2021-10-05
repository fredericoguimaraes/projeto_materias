import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from plotly import graph_objs as go
from datetime import date
import streamlit as st

st.sidebar.title("Projeto- Engenharia UFF")
st.sidebar.header("2021.2")
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            Criado por: Frederico Guimarães
            """
st.sidebar.markdown(hide_streamlit_style, unsafe_allow_html=True) 
                  


def ler_dados(curso):
    curso = curso + '.xlsx'
    base = pd.read_excel(curso)
    return base



cursos = ['agricola' ,"civil","eletrica","mecanica","petroleo","producao","quimica","rec_hidricos","telecom"]
st.subheader('Matérias por turno para cada curso')
curso_selecionado = st.selectbox('Cursos',cursos)


dados = ler_dados(curso_selecionado)

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
dados_filtrado = dados_filtrado.loc[dados_filtrado['classificacao'] !=0]
d_graf2 = dados_filtrado[['Código Disciplina']].groupby(dados_filtrado['classificacao']).count()/len(dados_filtrado)
d_graf2 = d_graf2.reset_index().rename(columns={'Código Disciplina': 'Valor'})
layout = go.Layout(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)')
fig = go.Figure(data=[
    go.Bar(name="Manhã",y=[d_graf2['Valor'][0]],text="{0:.2f}%".format(d_graf2['Valor'][0]*100),textposition="auto"),go.Bar(name="Tarde",y=[d_graf2['Valor'][2]],text="{0:.2f}%".format(d_graf2['Valor'][2]*100),textposition="auto"),go.Bar(name="Noite",y=[d_graf2['Valor'][1]],text="{0:.2f}%".format(d_graf2['Valor'][1]*100),textposition="auto")],layout=layout)
fig.update_traces(hoverinfo = 'name+text ',  
                  textfont_size = 16)
fig.update_xaxes(visible=False)
fig.update_yaxes(visible=False)
fig.update_layout(barmode='group',title="Distribuição de matérias por turno")
fig.update_layout_images(visible=False)


st.plotly_chart(fig)


def Tratabase(base):
    l_colunas = ['Horário Seg', 'Horário Ter', 'Horário Qua', 'Horário Qui', 'Horário Sex', 'Horário Sáb']

    for i in l_colunas:
        horario1 = []
        horario2 = []
        for n in range(len(base)):

            try:
                horario1.append(int(base[i][n].split("-")[0].split(":")[0]))
                horario2.append(int(base[i][n].split("-")[1].split(":")[0]))
            except:
                horario1.append("-")
                horario2.append("-")
            h1 = i + " " + "inicial"
            h2 = i + " " + "final"
        base[h1] = horario1
        base[h2] = horario2

    selec = ['Código Disciplina', 'Nome Disciplina', 'Código Turma',
             'CH Teóricas', 'CH Práticas', 'CH Estágio',
             'Horário Seg inicial', 'Horário Seg final',
             'Horário Ter inicial', 'Horário Ter final', 'Horário Qua inicial',
             'Horário Qua final', 'Horário Qui inicial', 'Horário Qui final',
             'Horário Sex inicial', 'Horário Sex final', 'Horário Sáb inicial',
             'Horário Sáb final']
    colunas = base.columns
    b = colunas.isin(selec)
    filtro = colunas[b]
    dados_filtrado = base[filtro]

    col = ['Horário Seg inicial', 'Horário Ter inicial', 'Horário Qua inicial', 'Horário Qui inicial',
           'Horário Sex inicial']
    classificacao = [0 for a in range(len(dados_filtrado))]
    for i in col:
        for j in range(len(base)):
            try:
                if int(dados_filtrado[i][j]) < 12:
                    turno = "Manhã"
                if int(dados_filtrado[i][j]) >= 12 and int(dados_filtrado[i][j]) < 18:
                    turno = "Tarde"
                if int(dados_filtrado[i][j]) >= 18:
                    turno = "Noite"

                classificacao[j] = turno
            except:
                pass

    dados_filtrado['classificacao'] = classificacao

    return dados_filtrado

    return dados_filtrado
def dados_barh(turno):
    cursos = ['agricola', "civil", "eletrica", "mecanica", "petroleo", "producao", "quimica", "rec_hidricos", "telecom"]
    df_barh = pd.DataFrame()
    for l in cursos:
        linha = {}
        b = ler_dados(l)
        dados = Tratabase(b)
        total= dados.loc[dados['classificacao']!=0].value_counts().sum()
        dados = dados.loc[dados['classificacao'] == turno]
        resultado = dados['classificacao'].count()/total
        linha = {'curso': l, 'valor': resultado}
        df_barh = df_barh.append(linha,ignore_index=True)
    return df_barh


# grafico 2
st.subheader("Ranking de cursos por turno")
turnos = ['Manhã','Tarde','Noite']
selec_turno = st.selectbox("Turno",turnos)

base_g2 = dados_barh(selec_turno).sort_values(by='valor',ascending=True)
layout = go.Layout(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)')
base_g2['valor2'] = ["{0:.2f}%".format(i*100) for i in base_g2["valor"]]
fig2 = go.Figure(go.Bar(x=base_g2['valor'],y=base_g2['curso'],orientation='h',text=base_g2['valor2'],textposition="auto"))
fig2.update_traces(hoverinfo = 'y+text ',  
                  textfont_size = 16)
fig2.update_xaxes(visible=False)
fig2.update_yaxes(visible=True)
fig2.update_layout(title="Ranking de Cursos por Turno")
fig2.update_layout_images(visible=False)
st.plotly_chart(fig2)


    




