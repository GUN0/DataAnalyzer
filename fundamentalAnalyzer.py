import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
from pandasgui import show

url = 'https://www.isyatirim.com.tr/tr-tr/analiz/hisse/Sayfalar/default.aspx'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
rows = soup.select('.dataTable tbody tr')

output_directory = 'home/gun/Documents/ProperReports/'
directory = '/home/gun/Documents/ReportCollector/FinancialReports/'
sorted_directory = sorted(os.listdir(directory))

yf_STOCK = []
yf_stock_price = {}
stock_and_close_price = {}
stock_data = {}
stock_ratios = {}

STOCKS = ["ACSEL","ADEL","AFYON","AKCNS","ATEKS","AKSA","ALCAR","ALKIM","ALKA","ALMAD","AEFES","ASUZU","ANGEN","ARCLK","ARSAN","ASTOR","AVOD",
          "AYGAZ","BAGFS","BAKAB","BNTAS","BANVT","BARMA","BTCIM","BSOKE","BAYRK","BRKSN","BLCYT","BMSTL","BMSCH","BOBET","BRSAN","BFREN","BOSSA",
          "BRISA","BURCE","BURVA","BUCIM","BVSAN","CCOLA","CELHA","CEMAS","CEMTS","CMBTN","CIMSA","CUSAN","DAGI","DARDL","DMSAS","DERIM","DESA","DEVA",
          "DNISI","DITAS","DGNMO","DOGUB","DOKTA","DURDO","DYOBY","EGEEN","EGGUB","EGPRO","EGSER","EPLAS","ELITE","EMKEL",
          "ENSRI","ERBOS","ERCB","EREGL","ERSU","TEZOL","EUREN","FADE","FMIZP","FROTO","FORMT","FRIGO","GEDZA","GENTS","GEREL","GOODY",
          "GOLTS","GUBRF","HATEK","HEKTS","HKTM","ISKPL","IHEVA","IMASM","IPEKE","ISDMR","ISSEN","IZINV","IZMDC","IZFAS","JANTS","KLKIM",
          "KAPLM","KRDMA","KRDMB","KRDMD","KARSN","KRTEK","KARTN","KATMR","KERVT","KRVGD","KMPUR","KLMSN","KCAER","KLSYN","KNFRT","KONYA",
          "KONKA","KORDS","KRPLS","KOZAL","KOZAA","KRSTL","KUTPO","KTSKR","LUKSK","MAKIM","MAKTK","MRSHL","MEDTR","MEGAP",
          "MNDRS","MERCN","MERKO","MNDTR","NIBAS","NUHCM","ONCSM","ORCAY","OTKAR","OYAKC","OYLUM","OZRDN","OZSUB","PNLSN","PRKME","PARSN","PENGD",
          "PETKM","PETUN","PINSU","PNSUT","POLTK","PRZMA","QUAGR","RNPOL","RODRG","RTALB","RUBNS","SAFKR","SNICA","SANFM","SAMAT","SARKY","SASA","SAYAS",
          "SEKUR","SELGD","SELVA","SEYKM","SILVR","SOKE","SKTAS","SUNTK","TATGD","TMPOL","TETMT","TOASO","TUCLK","TUKAS","TRILC","TMSN",
          "TUPRS","PRKAB","TTRAK","ULUSE","ULUUN","USAK","ULKER","VANGD","VESBE","VESTL","VKING","YAPRK","YATAS","YYLGD","YKSLN","YUNSA"]


for i in (sorted_directory):
    i = os.path.splitext(i)[0]
    file = pd.read_excel(f'/home/gun/Documents/ReportCollector/FinancialReports/{i}.xlsx')
    donen_varliklar = file[file['Bilanço'] == 'Dönen Varlıklar']
    diger_donen_varliklar = file[file['Bilanço'] == '  Diğer Dönen Varlıklar']
    net_donem_kari = file[file['Bilanço'] == '  Dönem Net Kar/Zararı']
    odenmis_sermaye = file[file['Bilanço'] == '  Ödenmiş Sermaye']
    toplam_kaynaklar = file[file['Bilanço'] == 'TOPLAM KAYNAKLAR']
    kisa_vadeli = file[file['Bilanço'] == 'Kısa Vadeli Yükümlülükler']
    uzun_vadeli = file[file['Bilanço'] == 'Uzun Vadeli Yükümlülükler']
    nakit_ve_nakit_benzeri = file[file['Bilanço'] == '  Nakit ve Nakit Benzerleri']
    brut_kar = file[file['Bilanço'] == 'BRÜT KAR (ZARAR)']
    satis_gelirleri = file[file['Bilanço'] == 'Satış Gelirleri']
    ozkaynaklar = file[file['Bilanço'] == 'Özkaynaklar']
    financials = pd.concat([donen_varliklar, diger_donen_varliklar,net_donem_kari, odenmis_sermaye, toplam_kaynaklar, 
                     kisa_vadeli, uzun_vadeli, nakit_ve_nakit_benzeri, 
                     brut_kar, satis_gelirleri, ozkaynaklar])
    for numeric in financials.columns[1:]:
        financials[numeric] = financials[numeric].astype(int)
    stock_data[i] = financials

# TODO create a dict, key = stock name, value = data frame of calculated ratios 

for key, df in stock_data.items():
    bilanco_adjusted = pd.DataFrame()
    net_kar_yillik_df = pd.DataFrame()
    satis_gelirleri_yillik_df = pd.DataFrame()
    brut_kar_yillik_df = pd.DataFrame()
    ozkaynak_ortalama_df = pd.DataFrame()
    donen_varliklar_proper_df = pd.DataFrame()
    toplam_donen_varliklar_df = pd.DataFrame()

    for index, row in stock_data[key].iterrows():
        if index == 0:
            title0 = pd.concat([row[:1]], axis=1).T
            date_value0 = pd.concat([row[1:]], axis=1).T
            row0 = pd.concat([title0, date_value0], axis=1)

            donen_varliklar_proper = row0.drop('Bilanço', axis=1)
            donen_varliklar_proper.insert(0, 'Değerler','Dönen Varlıklar')
            donen_varliklar_proper_df = donen_varliklar_proper_df._append(donen_varliklar_proper)
            bilanco_adjusted = bilanco_adjusted._append(donen_varliklar_proper)

        elif index == 9:
            title01 = pd.concat([row[:1]], axis=1).T
            date_value01 = pd.concat([row[1:]], axis=1).T
            row01 = pd.concat([title01, date_value01], axis=1)

            diger_donen_varliklar_proper = row01.drop('Bilanço', axis=1)
            diger_donen_varliklar_proper.insert(0, 'Değerler','Diğer Dönen Varlıklar')

            toplam_donen_varliklar = diger_donen_varliklar_proper.drop('Değerler', axis=1)
            toplam_donen_varliklar.insert(0, 'Değerler','Toplam Dönen Varlıklar')
            toplam_donen_varliklar = toplam_donen_varliklar.reset_index(drop=True)

            for i in range(1, len(toplam_donen_varliklar.columns)):
                current_column = toplam_donen_varliklar.columns[i]
                donen_col = donen_varliklar_proper_df.columns[i]
                diger_col = diger_donen_varliklar_proper.columns[i]
                
                donen = donen_varliklar_proper_df[donen_col].reset_index(drop=True) 
                diger = diger_donen_varliklar_proper[diger_col].reset_index(drop=True)

                toplam_donen_varliklar[current_column] = donen + diger

            toplam_donen_varliklar_df = toplam_donen_varliklar_df._append(toplam_donen_varliklar)
            toplam_donen_varliklar_df.set_index(pd.Index([10]), inplace=True)

            bilanco_adjusted = bilanco_adjusted._append([diger_donen_varliklar_proper, toplam_donen_varliklar_df])

        if index == 52:
            title1 = pd.concat([row[:1]], axis=1).T
            date_value1 = pd.concat([row[1:]], axis=1).T
            row1 = pd.concat([title1, date_value1], axis=1)

            net_kar_ceyrek = row1.drop('Bilanço', axis=1)
            net_kar_ceyrek.insert(0, 'Değerler','Net Kar/Zarar Çeyreklik')

            for i in range(1, len(net_kar_ceyrek.columns) -1):
                current_col = net_kar_ceyrek.columns[i]
                prev_col = net_kar_ceyrek.columns[i+1]

                if not current_col.endswith('/3'):
                    net_kar_ceyrek[current_col] = net_kar_ceyrek[current_col] - net_kar_ceyrek[prev_col]

            net_kar_yillik = net_kar_ceyrek.drop('Değerler', axis=1)
            net_kar_yillik.insert(0, 'Değerler','Net Kar/Zarar Yıllık')

            for i in range(1, len(net_kar_yillik.columns) -3):
                col1 = net_kar_yillik.columns[i+1]
                col2 = net_kar_yillik.columns[i+2]
                col3 = net_kar_yillik.columns[i+3]
                current_col = net_kar_yillik.columns[i]

                net_kar_yillik[current_col] = net_kar_yillik[current_col] + net_kar_yillik[col1] + net_kar_yillik[col2] + net_kar_yillik[col3]
            net_kar_yillik.iloc[0, -3:] = 0

            net_kar_yillik_df = net_kar_yillik_df._append(net_kar_yillik)
            net_kar_yillik_df.set_index(pd.Index([53]), inplace=True)
            bilanco_adjusted = bilanco_adjusted._append([net_kar_ceyrek, net_kar_yillik_df])

        elif index == 45:
            title2 = pd.concat([row[:1]], axis=1).T
            date_value2 = pd.concat([row[1:]], axis=1).T
            row2 = pd.concat([title2, date_value2], axis=1)

            odenmis_sermaye_proper = row2.drop('Bilanço', axis=1) 
            odenmis_sermaye_proper.insert(0,'Değerler', 'Ödenmiş Sermaye') 
            
            bilanco_adjusted = bilanco_adjusted._append(odenmis_sermaye_proper)

        elif index == 55:
            title3 = pd.concat([row[:1]], axis=1).T
            date_value3 = pd.concat([row[1:]], axis=1).T
            row3 = pd.concat([title3, date_value3], axis=1)

            toplam_kaynaklar_proper = row3.drop('Bilanço', axis=1) 
            toplam_kaynaklar_proper.insert(0,'Değerler', 'Toplam Kaynaklar') 
            
            bilanco_adjusted = bilanco_adjusted._append(toplam_kaynaklar_proper)

        elif index == 23:
            title4 = pd.concat([row[:1]], axis=1).T
            date_value4 = pd.concat([row[1:]], axis=1).T
            row4 = pd.concat([title4, date_value4], axis=1)

            uzun_vadeli_borc = row4.drop('Bilanço', axis=1) 
            uzun_vadeli_borc.insert(0,'Değerler', 'Uzun Vadeli Borçlar') 
            
            bilanco_adjusted = bilanco_adjusted._append(uzun_vadeli_borc)

        elif index == 36:
            title5 = pd.concat([row[:1]], axis=1).T
            date_value5 = pd.concat([row[1:]], axis=1).T
            row5 = pd.concat([title5, date_value5], axis=1)

            kisa_vadeli_borc = row5.drop('Bilanço', axis=1) 
            kisa_vadeli_borc.insert(0,'Değerler', 'Kısa Vadeli Borçlar') 
            
            bilanco_adjusted = bilanco_adjusted._append(kisa_vadeli_borc)

        elif index == 1:
            title6 = pd.concat([row[:1]], axis=1).T
            date_value6 = pd.concat([row[1:]], axis=1).T
            row6 = pd.concat([title6, date_value6], axis=1)

            nakit_ve_nakit_benzeri_proper = row6.drop('Bilanço', axis=1) 
            nakit_ve_nakit_benzeri_proper.insert(0,'Değerler', 'Nakit ve Nakit Benzerleri') 
            
            bilanco_adjusted = bilanco_adjusted._append(nakit_ve_nakit_benzeri_proper)
        
        elif index == 66:
            title7 = pd.concat([row[:1]], axis=1).T
            date_value7 = pd.concat([row[1:]], axis=1).T
            row7 = pd.concat([title7, date_value7], axis=1)

            brut_kar_ceyrek = row7.drop('Bilanço', axis=1) 
            brut_kar_ceyrek.insert(0,'Değerler', 'Brüt Kar/Zarar Çeyreklik')

            for i in range(1, len(brut_kar_ceyrek.columns) -1):
                current_col = brut_kar_ceyrek.columns[i]
                prev_col = brut_kar_ceyrek.columns[i+1]

                if not current_col.endswith('/3'):
                    brut_kar_ceyrek[current_col] = brut_kar_ceyrek[current_col] - brut_kar_ceyrek[prev_col]

            brut_kar_yillik = brut_kar_ceyrek.drop('Değerler', axis=1)
            brut_kar_yillik.insert(0, 'Değerler','Brüt Kar/Zarar Yıllık')

            for i in range(1, len(brut_kar_yillik.columns) -3):
                col1 = brut_kar_yillik.columns[i+1]
                col2 = brut_kar_yillik.columns[i+2]
                col3 = brut_kar_yillik.columns[i+3]
                current_col = brut_kar_yillik.columns[i]

                brut_kar_yillik[current_col] = brut_kar_yillik[current_col] + brut_kar_yillik[col1] + brut_kar_yillik[col2] + brut_kar_yillik[col3]
            brut_kar_yillik.iloc[0, -3:] = 0

            brut_kar_yillik_df = brut_kar_yillik_df._append(brut_kar_yillik)
            brut_kar_yillik_df.set_index(pd.Index([67]), inplace=True)
            bilanco_adjusted = bilanco_adjusted._append([brut_kar_ceyrek, brut_kar_yillik_df])

        elif index == 57:
            title8 = pd.concat([row[:1]], axis=1).T
            date_value8 = pd.concat([row[1:]], axis=1).T
            row8 = pd.concat([title8, date_value8], axis=1)

            satis_gelirleri_ceyrek = row8.drop('Bilanço', axis=1) 
            satis_gelirleri_ceyrek.insert(0,'Değerler', 'Satış Gelirleri Çeyreklik') 

            for i in range(1, len(satis_gelirleri_ceyrek.columns) -1):
                current_col = satis_gelirleri_ceyrek.columns[i]
                prev_col = satis_gelirleri_ceyrek.columns[i+1]

                if not current_col.endswith('/3'):
                    satis_gelirleri_ceyrek[current_col] = satis_gelirleri_ceyrek[current_col] - satis_gelirleri_ceyrek[prev_col]

            satis_gelirleri_yillik = satis_gelirleri_ceyrek.drop('Değerler', axis=1)
            satis_gelirleri_yillik.insert(0, 'Değerler','Satış Gelirleri Yıllık')

            for i in range(1, len(satis_gelirleri_yillik.columns) -3):
                col1 = satis_gelirleri_yillik.columns[i+1]
                col2 = satis_gelirleri_yillik.columns[i+2]
                col3 = satis_gelirleri_yillik.columns[i+3]
                current_col = satis_gelirleri_yillik.columns[i]

                satis_gelirleri_yillik[current_col] = satis_gelirleri_yillik[current_col] + satis_gelirleri_yillik[col1] + satis_gelirleri_yillik[col2] + satis_gelirleri_yillik[col3]
            satis_gelirleri_yillik.iloc[0, -3:] = 0

            satis_gelirleri_yillik_df = satis_gelirleri_yillik_df._append(satis_gelirleri_yillik)
            satis_gelirleri_yillik_df.set_index(pd.Index([58]), inplace=True)
            bilanco_adjusted = bilanco_adjusted._append([satis_gelirleri_ceyrek, satis_gelirleri_yillik_df])

        elif index == 43:
            title9 = pd.concat([row[:1]], axis=1).T
            date_value9 = pd.concat([row[1:]], axis=1).T
            row9 = pd.concat([title9, date_value9], axis=1)

            ozkaynak_proper = row9.drop('Bilanço', axis=1) 
            ozkaynak_proper.insert(0,'Değerler', 'Özkaynaklar')

            ozkaynak_ortalama = ozkaynak_proper.drop('Değerler', axis=1) 
            ozkaynak_ortalama.insert(0,'Değerler', 'Özkaynaklar (ORTALAMA)') 

            for i in range(1, len(ozkaynak_ortalama.columns) -4):
                current_col = ozkaynak_ortalama.columns[i]
                col_4 = ozkaynak_ortalama.columns[i+4]

                ozkaynak_ortalama[current_col] = (ozkaynak_ortalama[current_col] + ozkaynak_ortalama[col_4]) / 2
            ozkaynak_ortalama.iloc[0, -4:] = 0
            ozkaynak_ortalama_df = ozkaynak_ortalama_df._append(ozkaynak_ortalama)
            ozkaynak_ortalama_df.set_index(pd.Index([44]), inplace=True)

            bilanco_adjusted = bilanco_adjusted._append([ozkaynak_proper, ozkaynak_ortalama_df])

    bilanco_adjusted.to_excel('/home/gun/Documents/ProperReports/{}.xlsx'.format(key), index=False)


    # show(bilanco_adjusted)

