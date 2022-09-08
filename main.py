import pandas as pd
import numpy as np
import data as dt
import math as mt

#Capital Inicial
cap_i=1000000

#Primera fecha
FirstDF = dt.df
passive_m1= df[0].reset_index(drop=True)

#Peso ponderado
peso_pond= passive_m1["Peso (%)"]/100

#Capital Invertido en T=0
peso_din= cap_i * peso_pond

acciones=prices_M.iloc[0, :]
#Cantidad de títulos por activo
titulos = [peso_din[i] / acciones[i] for i in range(0, len(acciones))]
n_titulos=[mt.trunc(titulos[i]) for i in range (0, len(titulos))]

#comisión para el portafolio
fee= [sum((n_titulos[i] * acciones) *0.00125) for i in range(0,len(acciones))]

#Precio mensual por la cantidad de titulos
value_i= sum(n_titulos*acciones)
#cantidad de efectivo  
cash= cap_i - value_i - sum(fee)

#Valor del portafolio al primer mes
pvalue_m1= value_i + cash 

#Valor del portafolio en el resto de los meses de inversión
pvalue_mr=[sum(dt.prices_M.iloc[i, :] * titulos) for i in range (len(dt.prices_M[0:]))]

df_pasiva=pd.DataFrame({'Timestamp': dt.prices_M.index[0:], 'capital':pvalue_mr[0:]})
rend=[(pvalue_mr[i+1]/pvalue_mr[i])-1  for i in range(0,len (pvalue_mr)-1)]
rend.insert(0,0)
rend_acum= [(pvalue_mr[i]/pvalue_m1) for i in range(0, len(pvalue_mr))]
df_pasiva["Rend"] = rend
df_pasiva["Rend_acum"] = rend_acum[0:]
df_pasiva.head()

#Inversión Activa
prices2= dt.prices_A.iloc[0,:]

DFA = df
active_m1= DFA[0].reset_index(drop=True)
#Peso ponderado
peso_pondact= active_m1["Peso (%)"]/100
#Capital Invertido en T=0
peso_dinact= cap_i * peso_pondact

#Número de titulos 
acciones_act=dt.prices_A.iloc[0, :]
titulos_act= [peso_dinact[i] / acciones_act[i] for i in range(0, len(acciones_act))]
n_titulos_act=[mt.trunc(titulos_act[i]) for i in range (0, len(titulos_act))]

fee_act= [sum((n_titulos_act[i] * acciones_act) *0.00125) for i in range(0,len(acciones_act))]

#Precio mensual por la cantidad de titulos
value_i_act= sum(n_titulos_act*acciones_act)

cash_act= cap_i - value_i_act - sum(fee_act)

#Valor del portafolio al primer mes
pvalue_actm1= value_i_act + cash_act

pvalue_actmr=[sum(dt.prices_A.iloc[i, :] * titulos_act) for i in range (len(dt.prices_A[0:]))]

#Mover los titulos cada mes
move=pd.DataFrame({'Close': acciones_act.iloc[0:], 'Rendimientos': prices2, 'Titulos': n_titulos_act[0:],})
move.head(5)

pd.options.mode.chained_assignment = None  # default='warn'
for i in range(1,len(move)):
    if move['Rendimientos'][i]<= -0.05:
        move['Titulos'][i]= move['Titulos'][i-1] +(move['Titulos'][i]*.05) // (move['Close'][i-1]*(1+0.00125))
    else:
        move['Titulos'][i]= move['Titulos'][i-1] - (move['Titulos'][i]*.05)
        
numtit_act= pvalue_actm1// acciones_act.iloc[0:]
pvalue_act= acciones_act.iloc[0:]*numtit_act
pvalue_act= move['Titulos']* move['Close']

df_activo= pd.DataFrame({"Timestamp": dt.prices_A.index[0],"Capital":pvalue_act,"Rendimientos":pvalue_act.pct_change(),
                          "Rendimientos_Acumulados":pvalue_act/pvalue_act[0]})
df_activo.head(5)

#Históricos de las operaciones
df_operaciones= pd.DataFrame({'Timestamp': dt.prices_A.index[0],'titulos_totales':move['Titulos'], 
                              'titulos_compra':move['Titulos'].diff(),'precios': move['Close']})
df_operaciones['Comisión']= move['Titulos'].diff()*move['Close']* 0.00125
df_operaciones['Comision_acum'] = df_operaciones['Comisión'].cumsum()
df_operaciones.head(5)

rf = 0.0429/12
#Medidas de Atribución al Desempeño
df_medidas = pd.DataFrame({"medida":["rend_m","rend_c","sharpe"],
                           "descripción":['Rendimiento Promedio Mensual', 'Rendimiento Mensual Acumulado','Sharpe Ratio']})
df_medidas = df_medidas.set_index("medida")
df_medidas["inv_pasiva"] = (np.array(rend).mean(),np.array(rend_acum).mean(),(np.array(rend).mean()-rf)/np.array(rend_acum).std())
df_medidas["inv_activa"] = (prices2.mean(),prices2.mean(),(prices2.mean()-rf)/prices2.std())
df_medidas
