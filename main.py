from ppi_client.ppi import PPI
import pandas as pd
import datetime as dt
import plotly.graph_objects as go
from funcionesAux import getFuturesDate, convert_datetime_to_date, days_to_maturity
import json

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)

ACCIONES_CON_OPCIONES = ["ALUA", "COME", "GGAL", "YPFD", "PGR", "TXAR",
                         "PAMP", "CRES", "BHIP", "TRAN", "SUPV", "CECO2",
                         "BOLT", "BMA", "TECO2", "EDN", "CEPU", "BYMA",
                         "TGNO4", "HARG"]

ACCIONES_CON_FUTUROS = ["GGAL", "PAMP", "YPFD"]

END_DATE = dt.date.today()

START_DATE = END_DATE - dt.timedelta(days = 120)

VENCIMIENTO = 'PASADO'

MATURITY_DATE = getFuturesDate(END_DATE)['FECHA ' + VENCIMIENTO]


with open("C:/Users/User/Desktop/Proyectos 3.9/FINANZAS/c.json") as json_file:
    archivo = json.load(json_file)
client_id = archivo["ppi"]["client_id"]
client_secret = archivo["ppi"]["client_secret"]

ppi = PPI(sandbox=False)
ppi.account.login(client_id, client_secret)

tasas = pd.DataFrame()
marketdata = pd.DataFrame()

for ticker in ACCIONES_CON_FUTUROS:
    try:
        accion_raw = ppi.marketdata.search(ticker, "Acciones", "A-48HS", START_DATE, END_DATE)
        aux_accion = pd.DataFrame.from_dict(accion_raw, orient='columns')
        aux_accion.set_index("date",inplace=True)
        aux_accion = aux_accion['price']
        # print(aux_accion)
        aux_accion.name = ticker
        marketdata = pd.concat([marketdata, aux_accion], axis=1)
    except:
        print(f"No se pudo traer precio histórico de: {ticker}")
    ticker_futuro = ticker + "/" + getFuturesDate(END_DATE)[VENCIMIENTO]
    try:
        futuro_raw = ppi.marketdata.search(ticker_futuro, "FUTUROS", "A-24HS", START_DATE, END_DATE)
        aux_futuro = pd.DataFrame.from_dict(futuro_raw, orient='columns')
        aux_futuro.set_index("date", inplace=True)
        aux_futuro = aux_futuro['price']
        aux_futuro.name = ticker_futuro

        marketdata = pd.concat([marketdata, aux_futuro], axis=1)
    except:
        print(f"No se pudo traer precio histórico de: {ticker_futuro}")

    #Calculo la tasa de interés ganada con el futuro
    tasas[ticker] = ((marketdata[ticker_futuro] / marketdata[ticker]) - 1) * 100


# Acá ya tengo marketdata y tasas, acomodo los índices
tasas.sort_index(inplace=True)
marketdata.sort_index(inplace=True)

tasas['fecha'] = pd.to_datetime(tasas.index)
tasas['días al vencimiento'] = tasas['fecha'].apply(days_to_maturity, maturity_date=MATURITY_DATE)

for column in ACCIONES_CON_FUTUROS:
    tasas[column + ' TNA'] = tasas[column]*365/tasas['días al vencimiento']


tasas.drop(['fecha', 'días al vencimiento'], axis=1, inplace=True)
tasas.dropna(inplace=True)

print(tasas.head())

fig = go.Figure()
for column in tasas.columns:
    fig.add_trace(go.Scatter(x=tasas.index, y=tasas[column], mode='lines', name=column))


fig.update_layout(title_text=f"Tasa Implícita de Futuros ROFEX - {getFuturesDate(END_DATE)[VENCIMIENTO]}", title_x=0.5)

fig.update_yaxes(
        title_text = "Tasa %",
        title_standoff = 25)

fig.update_xaxes(
    # rangeslider_visible=True
    # nticks=20,
    tickangle = 90,
    title_text = "Fecha",
    title_standoff = 25,
    rangeselector=dict(
        buttons=list([
            dict(count=2, label="2m", step="month", stepmode="backward"),
            dict(count=4, label="4m", step="month", stepmode="backward"),
            # dict(count=1, label="YTD", step="year", stepmode="todate"),
            dict(step="all")])),
    rangebreaks=[
        dict(bounds=["sat", "mon"]),  # hide weekends
        # dict(values=["2015-12-25", "2016-01-01"])  # hide Christmas and New Year's
        ])
fig.show()

