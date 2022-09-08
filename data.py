import pandas as pd
import pandas_datareader.data as web

historicos = pd.read_csv('Lab_1/NAFTRAC_20220729.csv', skiprows=2)
historicos.head(5)

filenames= ['NAFTRAC_20200131.csv','NAFTRAC_20200228.csv','NAFTRAC_20200331.csv','NAFTRAC_20200430.csv','NAFTRAC_20200529.csv','NAFTRAC_20200630.csv','NAFTRAC_20200731.csv','NAFTRAC_20200831.csv'
        ,'NAFTRAC_20200930.csv','NAFTRAC_20201030.csv','NAFTRAC_20201130.csv','NAFTRAC_20201231.csv','NAFTRAC_20210129.csv','NAFTRAC_20210226.csv','NAFTRAC_20210331.csv','NAFTRAC_20210331.csv'
        ,'NAFTRAC_20210430.csv','NAFTRAC_20210531.csv','NAFTRAC_20210630.csv','NAFTRAC_20210730.csv','NAFTRAC_20210831.csv','NAFTRAC_20210930.csv','NAFTRAC_20211026.csv','NAFTRAC_20211130.csv'
        ,'NAFTRAC_20211231.csv','NAFTRAC_20220126.csv','NAFTRAC_20220228.csv','NAFTRAC_20220331.csv','NAFTRAC_20220429.csv','NAFTRAC_20220531.csv','NAFTRAC_20220630.csv','NAFTRAC_20220729.csv']

loc = r'Lab_1/'
fullloc = [loc + filenames[i] for i in range(0, len(filenames))]

df= [pd.read_csv(i,skiprows=2) for i in fullloc]
df=[df[i].dropna() for i in range(0,len(df))]
ticker=df[0]["Ticker"].reset_index(drop=True)
ticker=[ticker[i]+".MX" for i in range(0,len(ticker))]
ticker=[ticker[i].replace("*","")for i in range(0,len(ticker))]
ticker=[ticker[i].replace("GFREGIOO","RA") for i in range (0,len(ticker))]
ticker[34]="LIVEPOLC-1.MX"
ticker.remove("LIVEPOLC.1.MX")
ticker.remove("BSMXB.MX")
ticker.remove("KOFUBL.MX")
  
  # Inversión Pasiva
prices_M = pd.DataFrame(get_adj_closes(tickers=ticker, start_date="2020-01-31", end_date="2022-07-29")).dropna()
prices_M = prices_M.groupby(pd.Grouper(freq="M")).last()

#Inversion Activa
prices_A = pd.DataFrame(get_adj_closes(tickers=ticker, start_date="2020-01-31", end_date="2022-07-29")).dropna()
prices_A = prices_A.groupby(pd.Grouper(freq="M")).last()
