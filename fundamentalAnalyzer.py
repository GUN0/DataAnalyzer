import os
import pandas as pd
import requests
from bs4 import BeautifulSoup

url = 'https://www.isyatirim.com.tr/tr-tr/analiz/hisse/Sayfalar/default.aspx'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
rows = soup.select('.dataTable tbody tr')

directory = '/home/gun/Documents/ReportCollector/FinancialReports/'
sorted_directory = sorted(os.listdir(directory))

stock_and_close_price = {}
stock_data = {}

STOCKS = ["ACSEL","ADEL","AFYON","AGROT","AKCNS","ATEKS","AKSA","ALCAR","ALKIM","ALKA","ALMAD","AEFES","ASUZU","ANGEN","ARCLK","ARSAN","ASTOR","ATAKP","AVOD",
          "AYGAZ","BAGFS","BAKAB","BNTAS","BANVT","BARMA","BTCIM","BSOKE","BAYRK","BRKSN","BIENY","BLCYT","BMSTL","BMSCH","BOBET","BRSAN","BFREN","BOSSA",
          "BRISA","BURCE","BURVA","BUCIM","BVSAN","CCOLA","CVKMD","CELHA","CEMSA","CEMTS","CMBTN","CIMSA","CUSAN","DAGI","DARDL","DMSAS","DERIM","DESA","DEVA",
          "DNISI","DITAS","DMRGD","DOFER","DGNMO","DOGUB","DOKTA","DURDO","DYOBY","EGEEN","EGGUB","EGPRO","EGSER","EPLAS","EKOS","EKSUN","ELITE","EMKEL",
          "ENSRI","ERBOS","ERCB","EREGL","ERSU","TEZOL","EUREN","EUPWR","FADE","FMIZP","FROTO","FORMT","FRIGO","GEDZA","GENTS","GEREL","GIPTA","GOODY",
          "GOKNR","GOLTS","GUBRF","HATEK","HATSN","HEKTS","HKTM","ISKLP","IHEVA","IMASM","IPEKE","ISDMR","ISSEN","IZINV","IZMDC","IZFAS","JANTS","KLKIM",
          "KLSER","KAPLM","KRDMA","KRMDB","KRDMD","KARSN","KRTEK","KARTN","KATMR","KAYSE","KERVT","KRVGD","KMPUR","KLMSN","KCAER","KLSYN","KNFRT","KONYA",
          "KONKA","KORDS","KRPLS","KOZAL","KOZAA","KOPOL","KRSTL","KBORU","KUTPO","KTSKR","LUKSK","MAKIM","MAKTK","MRSHL","MEDTR","MEGMT","MEGAP","MEKAG",
          "MNDRS","MERCN","MERKO","MNDTR","NIBAS","NUHCM","OFSYM","ONCSM","ORCAY","OTKAR","OYAKC","OYLUM","OZRDN","OZSUB","PNLSN","PRKME","PARSN","PENGD",
          "PETKM","PETUN","PINSU","PNSUT","POLTK","PRZMA","QUAGR","RNPOL","RODRG","RTALB","RUBNS","SAFKR","SNICA","SANFM","SAMAT","SARKY","SASA","SAYAS",
          "SEKUR","SELGD","SELVA","SEYKM","SILVR","SOKE","SKTAS","SUNTK","TARKM","TATGD","TMPOL","TETMT","TOASO","TUCLK","TUKAS","MARBL","TRILC","TMSN",
          "TUPRS","PRKAB","TTRAK","ULUSE","ULUUN","USAK","ULKER","VANGD","VESBE","VESTL","VKING","YAPRK","YATAS","YYLGD","YKLSN","YUNSA"]

def convert_to_float(value):
    value = value.replace(',', '').replace('.', '', value.count('.') - 1)

    result = float(value)
    return result

for row in rows:
    stock = row.find('td', title=True).a.text.strip()
    close_price = row.select_one('td.text-right').text.strip().replace(',', '.')
    close_price_float = convert_to_float(close_price)

    if stock in STOCKS:
        stock_and_close_price[stock] = close_price_float

sorted_list = sorted(stock_and_close_price.items())
sorted_stock_and_close_price = dict(sorted_list)


for i in (sorted_directory):
    i = os.path.splitext(i)[0]
    file = pd.read_excel(f'/home/gun/Documents/ReportCollector/FinancialReports/{i}.xlsx')
    net_donem_kari = file[file['Bilanço'] == '  Dönem Net Kar/Zararı']
    odenis_sermaye = file[file['Bilanço'] == '  Ödenmiş Sermaye']
    toplam_kaynaklar = file[file['Bilanço'] == 'TOPLAM KAYNAKLAR']
    kisa_vadeli = file[file['Bilanço'] == 'Kısa Vadeli Yükümlülükler']
    uzun_vadeli = file[file['Bilanço'] == 'Uzun Vadeli Yükümlülükler']
    nakit_ve_nakit_benzeri = file[file['Bilanço'] == '  Nakit ve Nakit Benzerleri']
    brut_kar = file[file['Bilanço'] == 'BRÜT KAR (ZARAR)']
    satis_gelirleri = file[file['Bilanço'] == 'Satış Gelirleri']
    ozkaynaklar = file[file['Bilanço'] == 'Özkaynaklar']
    financials = pd.concat([net_donem_kari, odenis_sermaye, toplam_kaynaklar, 
                     kisa_vadeli, uzun_vadeli, nakit_ve_nakit_benzeri, 
                     brut_kar, satis_gelirleri, ozkaynaklar])
    for numeric in financials.columns[1:]:
        financials[numeric] = financials[numeric].astype(int)
    stock_data[i] = financials

# TODO create a dict, keys = stock name, value = data frame of calculated ratios 
a = stock_data['ACSEL'].iloc[[0]]
a = a.iloc[:, 1:]
for i in range(len(a.columns) -1):
    result = a.iloc[:, i] - a.iloc[:, i + 1]
    print(result)
