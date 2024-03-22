#!/usr/bin/env python3

import os
import requests
from bs4 import BeautifulSoup
import pandas as pd

# from pandasgui import show

url = "https://www.isyatirim.com.tr/tr-tr/analiz/hisse/Sayfalar/default.aspx"
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")
rows = soup.select(".dataTable tbody tr")

output_directory = "home/gun/Documents/ProperReports/"
directory = "/home/gun/Documents/ReportCollector/FinancialReports/"
sorted_directory = sorted(os.listdir(directory))

yf_STOCK = []
yf_stock_price = {}
stock_and_close_price = {}
stock_data = {}
stock_ratios = {}

STOCKS = [
    "ACSEL",
    "ADEL",
    "AFYON",
    "AKCNS",
    "ATEKS",
    "AKSA",
    "ALCAR",
    "ALKIM",
    "ALKA",
    "ALMAD",
    "AEFES",
    "ASUZU",
    "ANGEN",
    "ARCLK",
    "ARSAN",
    "AVOD",
    "AYGAZ",
    "BAGFS",
    "BAKAB",
    "BNTAS",
    "BANVT",
    "BTCIM",
    "BSOKE",
    "BAYRK",
    "BRKSN",
    "BLCYT",
    "BMSCH",
    "BRSAN",
    "BFREN",
    "BOSSA",
    "BRISA",
    "BURCE",
    "BURVA",
    "BUCIM",
    "BVSAN",
    "CCOLA",
    "CELHA",
    "CEMAS",
    "CEMTS",
    "CMBTN",
    "CIMSA",
    "CUSAN",
    "DAGI",
    "DARDL",
    "DMSAS",
    "DERIM",
    "DESA",
    "DEVA",
    "DITAS",
    "DGNMO",
    "DOGUB",
    "DOKTA",
    "DURDO",
    "DYOBY",
    "EGEEN",
    "EGGUB",
    "EGPRO",
    "EGSER",
    "EPLAS",
    "EMKEL",
    "ERBOS",
    "ERCB",
    "EREGL",
    "ERSU",
    "TEZOL",
    "FADE",
    "FMIZP",
    "FROTO",
    "FORMT",
    "FRIGO",
    "GEDZA",
    "GENTS",
    "GEREL",
    "GOODY",
    "GOLTS",
    "GUBRF",
    "HATEK",
    "HEKTS",
    "IHEVA",
    "IPEKE",
    "ISDMR",
    "IZINV",
    "IZMDC",
    "IZFAS",
    "JANTS",
    "KLKIM",
    "KAPLM",
    "KRDMA",
    "KRDMB",
    "KRDMD",
    "KARSN",
    "KRTEK",
    "KARTN",
    "KATMR",
    "KERVT",
    "KRVGD",
    "KMPUR",
    "KLMSN",
    "KNFRT",
    "KONYA",
    "KONKA",
    "KORDS",
    "KOZAL",
    "KOZAA",
    "KRSTL",
    "KUTPO",
    "LUKSK",
    "MAKTK",
    "MRSHL",
    "MEDTR",
    "MEGAP",
    "MNDRS",
    "MERKO",
    "MNDTR",
    "NIBAS",
    "NUHCM",
    "ORCAY",
    "OTKAR",
    "OYAKC",
    "OYLUM",
    "OZRDN",
    "PNLSN",
    "PRKME",
    "PARSN",
    "PENGD",
    "PETKM",
    "PETUN",
    "PINSU",
    "PNSUT",
    "POLTK",
    "PRZMA",
    "QUAGR",
    "RODRG",
    "RTALB",
    "RUBNS",
    "SAFKR",
    "SANFM",
    "SAMAT",
    "SARKY",
    "SASA",
    "SAYAS",
    "SEKUR",
    "SELGD",
    "SEYKM",
    "SILVR",
    "SKTAS",
    "SUNTK",
    "TATGD",
    "TMPOL",
    "TETMT",
    "TOASO",
    "TUCLK",
    "TUKAS",
    "TMSN",
    "TUPRS",
    "PRKAB",
    "TTRAK",
    "ULUSE",
    "ULUUN",
    "USAK",
    "ULKER",
    "VANGD",
    "VESBE",
    "VESTL",
    "VKING",
    "YAPRK",
    "YATAS",
    "YYLGD",
    "YKSLN",
    "YUNSA",
]


for i in sorted_directory:
    i = os.path.splitext(i)[0]
    file = pd.read_excel(
        f"/home/gun/Documents/ReportCollector/FinancialReports/{i}.xlsx"
    )
    donen_varliklar = file[file["Bilanço"] == "Dönen Varlıklar"]
    diger_donen_varliklar = file[file["Bilanço"] == "  Diğer Dönen Varlıklar"]
    net_donem_kari = file[file["Bilanço"] == "  Dönem Net Kar/Zararı"]
    odenmis_sermaye = file[file["Bilanço"] == "  Ödenmiş Sermaye"]
    toplam_kaynaklar = file[file["Bilanço"] == "TOPLAM KAYNAKLAR"]
    kisa_vadeli = file[file["Bilanço"] == "Kısa Vadeli Yükümlülükler"]
    uzun_vadeli = file[file["Bilanço"] == "Uzun Vadeli Yükümlülükler"]
    nakit_ve_nakit_benzeri = file[file["Bilanço"] == "  Nakit ve Nakit Benzerleri"]
    brut_kar = file[file["Bilanço"] == "BRÜT KAR (ZARAR)"]
    satis_gelirleri = file[file["Bilanço"] == "Satış Gelirleri"]
    ozkaynaklar = file[file["Bilanço"] == "Özkaynaklar"]
    toplam_varliklar = file[file["Bilanço"] == "TOPLAM VARLIKLAR"]
    arge = file[file["Bilanço"] == "Araştırma ve Geliştirme Giderleri (-)"]
    pazar_satis_dagitim = file[
        file["Bilanço"] == "Pazarlama, Satış ve Dağıtım Giderleri (-)"
    ]
    genel_yonetim = file[file["Bilanço"] == "Genel Yönetim Giderleri (-)"]
    diger_faliyet_giderleri = file[file["Bilanço"] == "Diğer Faaliyet Giderleri (-)"]
    diger_faliyet_gelirleri = file[file["Bilanço"] == "Diğer Faaliyet Gelirleri"]

    financials = pd.concat(
        [
            donen_varliklar,
            diger_donen_varliklar,
            net_donem_kari,
            odenmis_sermaye,
            toplam_kaynaklar,
            kisa_vadeli,
            uzun_vadeli,
            nakit_ve_nakit_benzeri,
            brut_kar,
            satis_gelirleri,
            ozkaynaklar,
            toplam_varliklar,
            arge,
            pazar_satis_dagitim,
            genel_yonetim,
            diger_faliyet_giderleri,
            diger_faliyet_gelirleri,
        ]
    )
    for numeric in financials.columns[1:]:
        financials[numeric] = financials[numeric].astype(int)
    stock_data[i] = financials

for key, df in stock_data.items():
    bilanco_adjusted = pd.DataFrame()
    net_kar_yillik_df = pd.DataFrame()
    satis_gelirleri_yillik_df = pd.DataFrame()
    brut_kar_yillik_df = pd.DataFrame()
    ozkaynak_ortalama_df = pd.DataFrame()
    ortalama_kaynaklar_df = pd.DataFrame()
    ar_ge_yillik_df = pd.DataFrame()
    pazar_satis_dagitim_yillik_df = pd.DataFrame()
    genel_yonetim_giderleri_yillik_df = pd.DataFrame()
    diger_faliyet_giderleri_yillik_df = pd.DataFrame()
    diger_faliyet_gelirleri_yillik_df = pd.DataFrame()

    for index, row in stock_data[key].iterrows():
        if index == 0:
            title0 = pd.concat([row[:1]], axis=1).T
            date_value0 = pd.concat([row[1:]], axis=1).T
            row0 = pd.concat([title0, date_value0], axis=1)

            donen_varliklar_proper = row0.drop("Bilanço", axis=1)
            donen_varliklar_proper.insert(0, "Değerler", "Dönen Varlıklar")
            bilanco_adjusted = bilanco_adjusted._append(donen_varliklar_proper)

        elif index == 9:
            title01 = pd.concat([row[:1]], axis=1).T
            date_value01 = pd.concat([row[1:]], axis=1).T
            row01 = pd.concat([title01, date_value01], axis=1)

            diger_donen_varliklar_proper = row01.drop("Bilanço", axis=1)
            diger_donen_varliklar_proper.insert(0, "Değerler", "Diğer Dönen Varlıklar")
            bilanco_adjusted = bilanco_adjusted._append(diger_donen_varliklar_proper)

        if index == 52:
            title1 = pd.concat([row[:1]], axis=1).T
            date_value1 = pd.concat([row[1:]], axis=1).T
            row1 = pd.concat([title1, date_value1], axis=1)

            net_kar_ceyrek = row1.drop("Bilanço", axis=1)
            net_kar_ceyrek.insert(0, "Değerler", "Net Kar/Zarar Çeyreklik")

            for i in range(1, len(net_kar_ceyrek.columns) - 1):
                current_col = net_kar_ceyrek.columns[i]
                prev_col = net_kar_ceyrek.columns[i + 1]

                if not current_col.endswith("/3"):
                    net_kar_ceyrek[current_col] = (
                        net_kar_ceyrek[current_col] - net_kar_ceyrek[prev_col]
                    )

            net_kar_yillik = net_kar_ceyrek.drop("Değerler", axis=1)
            net_kar_yillik.insert(0, "Değerler", "Net Kar/Zarar Yıllık")

            for i in range(1, len(net_kar_yillik.columns) - 3):
                col1 = net_kar_yillik.columns[i + 1]
                col2 = net_kar_yillik.columns[i + 2]
                col3 = net_kar_yillik.columns[i + 3]
                current_col = net_kar_yillik.columns[i]

                net_kar_yillik[current_col] = (
                    net_kar_yillik[current_col]
                    + net_kar_yillik[col1]
                    + net_kar_yillik[col2]
                    + net_kar_yillik[col3]
                )
            net_kar_yillik.iloc[0, -3:] = 0

            net_kar_yillik_df = net_kar_yillik_df._append(net_kar_yillik)
            net_kar_yillik_df.set_index(pd.Index([53]), inplace=True)
            bilanco_adjusted = bilanco_adjusted._append(
                [net_kar_ceyrek, net_kar_yillik_df]
            )

        elif index == 45:
            title2 = pd.concat([row[:1]], axis=1).T
            date_value2 = pd.concat([row[1:]], axis=1).T
            row2 = pd.concat([title2, date_value2], axis=1)

            odenmis_sermaye_proper = row2.drop("Bilanço", axis=1)
            odenmis_sermaye_proper.insert(0, "Değerler", "Ödenmiş Sermaye")

            bilanco_adjusted = bilanco_adjusted._append(odenmis_sermaye_proper)

        elif index == 55:
            title3 = pd.concat([row[:1]], axis=1).T
            date_value3 = pd.concat([row[1:]], axis=1).T
            row3 = pd.concat([title3, date_value3], axis=1)

            toplam_kaynaklar_proper = row3.drop("Bilanço", axis=1)
            toplam_kaynaklar_proper.insert(0, "Değerler", "Toplam Kaynaklar")

            ortalama_kaynaklar = toplam_kaynaklar_proper.drop("Değerler", axis=1)
            ortalama_kaynaklar.insert(0, "Değerler", "Ortalama Kaynaklar")

            for i in range(1, len(ortalama_kaynaklar.columns) - 4):
                current_col = ortalama_kaynaklar.columns[i]
                col_4 = ortalama_kaynaklar.columns[i + 4]

                ortalama_kaynaklar[current_col] = (
                    ortalama_kaynaklar[current_col] + ortalama_kaynaklar[col_4]
                ) / 2
            ortalama_kaynaklar.iloc[0, -4:] = 0

            ortalama_kaynaklar_df = ortalama_kaynaklar_df._append(ortalama_kaynaklar)
            ortalama_kaynaklar_df.set_index(pd.Index([56]), inplace=True)
            bilanco_adjusted = bilanco_adjusted._append(
                [toplam_kaynaklar_proper, ortalama_kaynaklar_df]
            )

        elif index == 23:
            title4 = pd.concat([row[:1]], axis=1).T
            date_value4 = pd.concat([row[1:]], axis=1).T
            row4 = pd.concat([title4, date_value4], axis=1)

            kisa_vadeli_borc = row4.drop("Bilanço", axis=1)
            kisa_vadeli_borc.insert(0, "Değerler", "Kısa Vadeli Borçlar")

            bilanco_adjusted = bilanco_adjusted._append(kisa_vadeli_borc)

        elif index == 36:
            title5 = pd.concat([row[:1]], axis=1).T
            date_value5 = pd.concat([row[1:]], axis=1).T
            row5 = pd.concat([title5, date_value5], axis=1)

            uzun_vadeli_borc = row5.drop("Bilanço", axis=1)
            uzun_vadeli_borc.insert(0, "Değerler", "Uzun Vadeli Borçlar")

            bilanco_adjusted = bilanco_adjusted._append(uzun_vadeli_borc)

        elif index == 1:
            title6 = pd.concat([row[:1]], axis=1).T
            date_value6 = pd.concat([row[1:]], axis=1).T
            row6 = pd.concat([title6, date_value6], axis=1)

            nakit_ve_nakit_benzeri_proper = row6.drop("Bilanço", axis=1)
            nakit_ve_nakit_benzeri_proper.insert(
                0, "Değerler", "Nakit ve Nakit Benzerleri"
            )

            bilanco_adjusted = bilanco_adjusted._append(nakit_ve_nakit_benzeri_proper)

        elif index == 66:
            title7 = pd.concat([row[:1]], axis=1).T
            date_value7 = pd.concat([row[1:]], axis=1).T
            row7 = pd.concat([title7, date_value7], axis=1)

            brut_kar_ceyrek = row7.drop("Bilanço", axis=1)
            brut_kar_ceyrek.insert(0, "Değerler", "Brüt Kar/Zarar Çeyreklik")

            for i in range(1, len(brut_kar_ceyrek.columns) - 1):
                current_col = brut_kar_ceyrek.columns[i]
                prev_col = brut_kar_ceyrek.columns[i + 1]

                if not current_col.endswith("/3"):
                    brut_kar_ceyrek[current_col] = (
                        brut_kar_ceyrek[current_col] - brut_kar_ceyrek[prev_col]
                    )

            brut_kar_yillik = brut_kar_ceyrek.drop("Değerler", axis=1)
            brut_kar_yillik.insert(0, "Değerler", "Brüt Kar/Zarar Yıllık")

            for i in range(1, len(brut_kar_yillik.columns) - 3):
                col1 = brut_kar_yillik.columns[i + 1]
                col2 = brut_kar_yillik.columns[i + 2]
                col3 = brut_kar_yillik.columns[i + 3]
                current_col = brut_kar_yillik.columns[i]

                brut_kar_yillik[current_col] = (
                    brut_kar_yillik[current_col]
                    + brut_kar_yillik[col1]
                    + brut_kar_yillik[col2]
                    + brut_kar_yillik[col3]
                )
            brut_kar_yillik.iloc[0, -3:] = 0

            brut_kar_yillik_df = brut_kar_yillik_df._append(brut_kar_yillik)
            brut_kar_yillik_df.set_index(pd.Index([65]), inplace=True)
            bilanco_adjusted = bilanco_adjusted._append(
                [brut_kar_ceyrek, brut_kar_yillik_df]
            )

        elif index == 57:
            title8 = pd.concat([row[:1]], axis=1).T
            date_value8 = pd.concat([row[1:]], axis=1).T
            row8 = pd.concat([title8, date_value8], axis=1)

            satis_gelirleri_ceyrek = row8.drop("Bilanço", axis=1)
            satis_gelirleri_ceyrek.insert(0, "Değerler", "Satış Gelirleri Çeyreklik")

            for i in range(1, len(satis_gelirleri_ceyrek.columns) - 1):
                current_col = satis_gelirleri_ceyrek.columns[i]
                prev_col = satis_gelirleri_ceyrek.columns[i + 1]

                if not current_col.endswith("/3"):
                    satis_gelirleri_ceyrek[current_col] = (
                        satis_gelirleri_ceyrek[current_col]
                        - satis_gelirleri_ceyrek[prev_col]
                    )

            satis_gelirleri_yillik = satis_gelirleri_ceyrek.drop("Değerler", axis=1)
            satis_gelirleri_yillik.insert(0, "Değerler", "Satış Gelirleri Yıllık")

            for i in range(1, len(satis_gelirleri_yillik.columns) - 3):
                col1 = satis_gelirleri_yillik.columns[i + 1]
                col2 = satis_gelirleri_yillik.columns[i + 2]
                col3 = satis_gelirleri_yillik.columns[i + 3]
                current_col = satis_gelirleri_yillik.columns[i]

                satis_gelirleri_yillik[current_col] = (
                    satis_gelirleri_yillik[current_col]
                    + satis_gelirleri_yillik[col1]
                    + satis_gelirleri_yillik[col2]
                    + satis_gelirleri_yillik[col3]
                )
            satis_gelirleri_yillik.iloc[0, -3:] = 0

            satis_gelirleri_yillik_df = satis_gelirleri_yillik_df._append(
                satis_gelirleri_yillik
            )
            satis_gelirleri_yillik_df.set_index(pd.Index([58]), inplace=True)
            bilanco_adjusted = bilanco_adjusted._append(
                [satis_gelirleri_ceyrek, satis_gelirleri_yillik_df]
            )

        elif index == 43:
            title9 = pd.concat([row[:1]], axis=1).T
            date_value9 = pd.concat([row[1:]], axis=1).T
            row9 = pd.concat([title9, date_value9], axis=1)

            ozkaynak_proper = row9.drop("Bilanço", axis=1)
            ozkaynak_proper.insert(0, "Değerler", "Özkaynaklar")

            ozkaynak_ortalama = ozkaynak_proper.drop("Değerler", axis=1)
            ozkaynak_ortalama.insert(0, "Değerler", "Özkaynaklar (ORTALAMA)")

            for i in range(1, len(ozkaynak_ortalama.columns) - 4):
                current_col = ozkaynak_ortalama.columns[i]
                col_4 = ozkaynak_ortalama.columns[i + 4]

                ozkaynak_ortalama[current_col] = (
                    ozkaynak_ortalama[current_col] + ozkaynak_ortalama[col_4]
                ) / 2
            ozkaynak_ortalama.iloc[0, -4:] = 0
            ozkaynak_ortalama_df = ozkaynak_ortalama_df._append(ozkaynak_ortalama)
            ozkaynak_ortalama_df.set_index(pd.Index([44]), inplace=True)

            bilanco_adjusted = bilanco_adjusted._append(
                [ozkaynak_proper, ozkaynak_ortalama_df]
            )

        elif index == 21:
            title10 = pd.concat([row[:1]], axis=1).T
            date_value10 = pd.concat([row[1:]], axis=1).T
            row10 = pd.concat([title10, date_value10], axis=1)

            toplam_varliklar_proper = row10.drop("Bilanço", axis=1)
            toplam_varliklar_proper.insert(0, "Değerler", "Toplam Varlıklar")

            bilanco_adjusted = bilanco_adjusted._append(toplam_varliklar_proper)

        elif index == 69:
            title11 = pd.concat([row[:1]], axis=1).T
            date_value11 = pd.concat([row[1:]], axis=1).T
            row11 = pd.concat([title11, date_value11], axis=1)

            ar_ge_ceyrek = row11.drop("Bilanço", axis=1)
            ar_ge_ceyrek.insert(
                0, "Değerler", "Araştırma ve Geliştirme Giderleri Çeyreklik"
            )

            for i in range(1, len(ar_ge_ceyrek.columns) - 1):
                current_col = ar_ge_ceyrek.columns[i]
                prev_col = ar_ge_ceyrek.columns[i + 1]

                if not current_col.endswith("/3"):
                    ar_ge_ceyrek[current_col] = (
                        ar_ge_ceyrek[current_col] - ar_ge_ceyrek[prev_col]
                    )

            ar_ge_yillik = ar_ge_ceyrek.drop("Değerler", axis=1)
            ar_ge_yillik.insert(
                0, "Değerler", "Araştırma ve Geliştirme Giderleri Yıllık"
            )

            for i in range(1, len(ar_ge_yillik.columns) - 3):
                col1 = ar_ge_yillik.columns[i + 1]
                col2 = ar_ge_yillik.columns[i + 2]
                col3 = ar_ge_yillik.columns[i + 3]
                current_col = ar_ge_yillik.columns[i]

                ar_ge_yillik[current_col] = (
                    ar_ge_yillik[current_col]
                    + ar_ge_yillik[col1]
                    + ar_ge_yillik[col2]
                    + ar_ge_yillik[col3]
                )
            ar_ge_yillik.iloc[0, -3:] = 0

            ar_ge_yillik_df = ar_ge_yillik_df._append(ar_ge_yillik)
            ar_ge_yillik_df.set_index(pd.Index([699]), inplace=True)

            bilanco_adjusted = bilanco_adjusted._append([ar_ge_ceyrek, ar_ge_yillik_df])

        elif index == 67:
            title12 = pd.concat([row[:1]], axis=1).T
            date_value12 = pd.concat([row[1:]], axis=1).T
            row12 = pd.concat([title12, date_value12], axis=1)

            pazar_satis_dagitim_ceyrek = row12.drop("Bilanço", axis=1)
            pazar_satis_dagitim_ceyrek.insert(
                0, "Değerler", "Pazarlama, Satış ve Dağıtım Giderleri Çeyreklik"
            )
            for i in range(1, len(pazar_satis_dagitim_ceyrek.columns) - 1):
                current_col = pazar_satis_dagitim_ceyrek.columns[i]
                prev_col = pazar_satis_dagitim_ceyrek.columns[i + 1]

                if not current_col.endswith("/3"):
                    pazar_satis_dagitim_ceyrek[current_col] = (
                        pazar_satis_dagitim_ceyrek[current_col]
                        - pazar_satis_dagitim_ceyrek[prev_col]
                    )

            pazar_satis_dagitim_yillik = pazar_satis_dagitim_ceyrek.drop(
                "Değerler", axis=1
            )
            pazar_satis_dagitim_yillik.insert(
                0, "Değerler", "Pazarlama, Satış ve Dağıtım Giderleri Yıllık"
            )

            for i in range(1, len(pazar_satis_dagitim_yillik.columns) - 3):
                col1 = pazar_satis_dagitim_yillik.columns[i + 1]
                col2 = pazar_satis_dagitim_yillik.columns[i + 2]
                col3 = pazar_satis_dagitim_yillik.columns[i + 3]
                current_col = pazar_satis_dagitim_yillik.columns[i]

                pazar_satis_dagitim_yillik[current_col] = (
                    pazar_satis_dagitim_yillik[current_col]
                    + pazar_satis_dagitim_yillik[col1]
                    + pazar_satis_dagitim_yillik[col2]
                    + pazar_satis_dagitim_yillik[col3]
                )
            pazar_satis_dagitim_yillik.iloc[0, -3:] = 0

            pazar_satis_dagitim_yillik_df = pazar_satis_dagitim_yillik_df._append(
                pazar_satis_dagitim_yillik
            )
            pazar_satis_dagitim_yillik_df.set_index(pd.Index([677]), inplace=True)

            bilanco_adjusted = bilanco_adjusted._append(
                [pazar_satis_dagitim_ceyrek, pazar_satis_dagitim_yillik_df]
            )

        elif index == 68:
            title13 = pd.concat([row[:1]], axis=1).T
            date_value13 = pd.concat([row[1:]], axis=1).T
            row13 = pd.concat([title13, date_value13], axis=1)

            genel_yonetim_giderleri_ceyrek = row13.drop("Bilanço", axis=1)
            genel_yonetim_giderleri_ceyrek.insert(
                0, "Değerler", "Genel Yönetim Giderleri Çeyreklik"
            )

            for i in range(1, len(genel_yonetim_giderleri_ceyrek.columns) - 1):
                current_col = genel_yonetim_giderleri_ceyrek.columns[i]
                prev_col = genel_yonetim_giderleri_ceyrek.columns[i + 1]

                if not current_col.endswith("/3"):
                    genel_yonetim_giderleri_ceyrek[current_col] = (
                        genel_yonetim_giderleri_ceyrek[current_col]
                        - genel_yonetim_giderleri_ceyrek[prev_col]
                    )

            genel_yonetim_giderleri_yillik = genel_yonetim_giderleri_ceyrek.drop(
                "Değerler", axis=1
            )
            genel_yonetim_giderleri_yillik.insert(
                0, "Değerler", "Genel Yönetim Giderleri Yıllık"
            )

            for i in range(1, len(genel_yonetim_giderleri_yillik.columns) - 3):
                col1 = genel_yonetim_giderleri_yillik.columns[i + 1]
                col2 = genel_yonetim_giderleri_yillik.columns[i + 2]
                col3 = genel_yonetim_giderleri_yillik.columns[i + 3]
                current_col = genel_yonetim_giderleri_yillik.columns[i]

                genel_yonetim_giderleri_yillik[current_col] = (
                    genel_yonetim_giderleri_yillik[current_col]
                    + genel_yonetim_giderleri_yillik[col1]
                    + genel_yonetim_giderleri_yillik[col2]
                    + genel_yonetim_giderleri_yillik[col3]
                )
            genel_yonetim_giderleri_yillik.iloc[0, -3:] = 0

            genel_yonetim_giderleri_yillik_df = (
                genel_yonetim_giderleri_yillik_df._append(
                    genel_yonetim_giderleri_yillik
                )
            )
            genel_yonetim_giderleri_yillik_df.set_index(pd.Index([688]), inplace=True)

            bilanco_adjusted = bilanco_adjusted._append(
                [genel_yonetim_giderleri_ceyrek, genel_yonetim_giderleri_yillik_df]
            )

        elif index == 71:
            title14 = pd.concat([row[:1]], axis=1).T
            date_value14 = pd.concat([row[1:]], axis=1).T
            row14 = pd.concat([title14, date_value14], axis=1)

            diger_faliyet_giderleri_ceyrek = row14.drop("Bilanço", axis=1)
            diger_faliyet_giderleri_ceyrek.insert(
                0, "Değerler", "Diğer Faaliyet Giderleri Çeyreklik"
            )

            for i in range(1, len(diger_faliyet_giderleri_ceyrek.columns) - 1):
                current_col = diger_faliyet_giderleri_ceyrek.columns[i]
                prev_col = diger_faliyet_giderleri_ceyrek.columns[i + 1]

                if not current_col.endswith("/3"):
                    diger_faliyet_giderleri_ceyrek[current_col] = (
                        diger_faliyet_giderleri_ceyrek[current_col]
                        - diger_faliyet_giderleri_ceyrek[prev_col]
                    )

            diger_faliyet_giderleri_yillik = diger_faliyet_giderleri_ceyrek.drop(
                "Değerler", axis=1
            )
            diger_faliyet_giderleri_yillik.insert(
                0, "Değerler", "Diğer Faaliyet Giderleri Yıllık"
            )

            for i in range(1, len(diger_faliyet_giderleri_yillik.columns) - 3):
                col1 = diger_faliyet_giderleri_yillik.columns[i + 1]
                col2 = diger_faliyet_giderleri_yillik.columns[i + 2]
                col3 = diger_faliyet_giderleri_yillik.columns[i + 3]
                current_col = diger_faliyet_giderleri_yillik.columns[i]

                diger_faliyet_giderleri_yillik[current_col] = (
                    diger_faliyet_giderleri_yillik[current_col]
                    + diger_faliyet_giderleri_yillik[col1]
                    + diger_faliyet_giderleri_yillik[col2]
                    + diger_faliyet_giderleri_yillik[col3]
                )
            diger_faliyet_giderleri_yillik.iloc[0, -3:] = 0

            diger_faliyet_giderleri_yillik_df = (
                diger_faliyet_giderleri_yillik_df._append(
                    diger_faliyet_giderleri_yillik
                )
            )
            diger_faliyet_giderleri_yillik_df.set_index(pd.Index([710]), inplace=True)

            bilanco_adjusted = bilanco_adjusted._append(
                [diger_faliyet_giderleri_ceyrek, diger_faliyet_giderleri_yillik_df]
            )

        elif index == 70:
            title15 = pd.concat([row[:1]], axis=1).T
            date_value15 = pd.concat([row[1:]], axis=1).T
            row15 = pd.concat([title15, date_value15], axis=1)

            diger_faliyet_gelirleri_ceyrek = row15.drop("Bilanço", axis=1)
            diger_faliyet_gelirleri_ceyrek.insert(
                0, "Değerler", "Diğer Faaliyet Gelirleri Çeyreklik"
            )

            for i in range(1, len(diger_faliyet_gelirleri_ceyrek.columns) - 1):
                current_col = diger_faliyet_gelirleri_ceyrek.columns[i]
                prev_col = diger_faliyet_gelirleri_ceyrek.columns[i + 1]

                if not current_col.endswith("/3"):
                    diger_faliyet_gelirleri_ceyrek[current_col] = (
                        diger_faliyet_gelirleri_ceyrek[current_col]
                        - diger_faliyet_gelirleri_ceyrek[prev_col]
                    )

            diger_faliyet_gelirleri_yillik = diger_faliyet_gelirleri_ceyrek.drop(
                "Değerler", axis=1
            )
            diger_faliyet_gelirleri_yillik.insert(
                0, "Değerler", "Diğer Faaliyet Gelirleri Yıllık"
            )

            for i in range(1, len(diger_faliyet_gelirleri_yillik.columns) - 3):
                col1 = diger_faliyet_gelirleri_yillik.columns[i + 1]
                col2 = diger_faliyet_gelirleri_yillik.columns[i + 2]
                col3 = diger_faliyet_gelirleri_yillik.columns[i + 3]
                current_col = diger_faliyet_gelirleri_yillik.columns[i]

                diger_faliyet_gelirleri_yillik[current_col] = (
                    diger_faliyet_gelirleri_yillik[current_col]
                    + diger_faliyet_gelirleri_yillik[col1]
                    + diger_faliyet_gelirleri_yillik[col2]
                    + diger_faliyet_gelirleri_yillik[col3]
                )
            diger_faliyet_gelirleri_yillik.iloc[0, -3:] = 0

            diger_faliyet_gelirleri_yillik_df = (
                diger_faliyet_gelirleri_yillik_df._append(
                    diger_faliyet_gelirleri_yillik
                )
            )
            diger_faliyet_gelirleri_yillik_df.set_index(pd.Index([700]), inplace=True)

            bilanco_adjusted = bilanco_adjusted._append(
                [diger_faliyet_gelirleri_ceyrek, diger_faliyet_gelirleri_yillik_df]
            )

    bilanco_adjusted.to_excel(
        "/home/gun/Documents/ProperReports/{}.xlsx".format(key), index=False
    )

    # show(bilanco_adjusted)
