from bs4 import BeautifulSoup
import re
import csv 
import urllib
from urllib.request import urlopen

continentcodes = ['AFR', 'AME', 'ASI', 'AUS', 'EUR'] 
# initialize nested dictionary
allBanknotes = {}

with open('banknotesdata2.csv', 'w', newline='') as csvfile:
    banknotewriter = csv.writer(csvfile, delimiter='|')
    banknotewriter.writerow(['country', 'pick', 'side', 'description'])

        
def extractText(url, country):
    try:
        urllib.request.urlopen(url, timeout=100)
    except:
        print('URL error!')
    else:
        page = urllib.request.urlopen(url, timeout=100)
        html = page.read().decode('cp1252')
        text = []
        soup = BeautifulSoup(html, 'html.parser')
        try:
            # find number: UPDATED July 2021 to be simpler 
            pickno = soup.find(re.compile("font"), {'face': 'Arial', 'size': '6'})
            number = pickno.text.strip()
            print(number)
            allBanknotes[country][number] = {'number' : number, 'date' : '', 'denomination' : '', 'currencyname' : '', 'issuer' : '', 'fronttext' : '', 'backtext' : '' }
            
            # handle misc fields 
            for pickno in soup.find_all(re.compile("td"), {'width': '10%', 'align' : 'left','bgcolor' : '#CECECE'}):
                
                # handle date
                if 'date' in pickno.text.strip().lower():
                    datetag = pickno.find_next_sibling("td")
                    date = re.sub("\s\s+", " ", ''.join(datetag.text.strip().splitlines()))
                    allBanknotes[country][number]['date'] = date
                
                # handle denomination amount and currency name 
                if 'value' in pickno.text.strip().lower():
                    valtag = pickno.find_next_sibling("td")
                    # separate out numerical denomination from currency name 
                    val = ''.join(filter(lambda i: i.isdigit(), valtag.text.strip())) 
                    allBanknotes[country][number]['denomination'] = val
                    currencyname = ''.join(filter(lambda i: i.isalpha(), valtag.text))
                    allBanknotes[country][number]['currencyname'] = currencyname
    
                # handle bank issuer name 
                if 'issued by' in pickno.text.strip().lower():
                    banktag = pickno.find_next_sibling("td")
                    issuer = re.sub("\s\s+", " ", ''.join(banktag.text.strip().splitlines())).strip()
                    allBanknotes[country][number]['issuer'] = issuer 
            count = 0
            for ptag in soup.find_all(re.compile("td"), {'width': '50%'}):
                font = ptag.find('font')
                if font is not None:
                    if (count==0):
                        text.append(font)
                        print(font.text.strip())
                        allBanknotes[country][number]['fronttext'] = re.sub("\s\s+", " ", ''.join(font.text.strip().splitlines()))
                        count = count + 1
                    elif (count==1):
                        #complicated bit to remove extra newlines/spaces 
                        allBanknotes[country][number]['backtext'] = re.sub("\s\s+", " ", ''.join(font.text.strip().splitlines())) 
        except:
            print('Some error occurred')
                
def extractBanknotes(page, noteslist):
    workingLinks = []
    html = page.read().decode('latin-1')
    soup = BeautifulSoup(html, 'html.parser')
    bnotelinks = soup.find_all('font', {'face' : 'Arial', 'size' : '5'})
    count = 0
    for i in range(len(bnotelinks)-1, -1, -1):
        # tr = bnotelinks[i].find_previous('tr').find_previous('tr')
        try:
            # a = tr.find('font')
            # if ('commemorative' not in a.text.lower()):
            # if (count <= 10 and 'commemorative' not in a.text.lower()):
            linktag = bnotelinks[i].find_all("a" , recursive=False, href=True)
            for link in linktag[0:1]:
                if('#' not in link['href'] and 'FX' not in link['href'] and link['href'][3] != 'R' and link['href'][3] != 'M' and link['href'] not in workingLinks):
                    workingLinks.append(link['href'])
                    noteslist.append(link['href'])
                    count = count + 1
        except:
            print('Issue round not found')
            
def getBanks(countryurl):
    banklinks = []
    html = urlopen(countryurl, timeout=100).read().decode('latin-1')
    soup = BeautifulSoup(html, 'html.parser')
    tabletag = soup.find('table', {'border' : '3'})
    td = tabletag.find_all('td')
    for tag in td:
        fonttag = tag.find_all('font')
        for tag in fonttag:
            if (len(tag.text.strip()) != 0 and tag.text.strip().lower()[0]=='p'):
                banklink = tag.find_previous('a')['href']
                x = re.sub('#.*', '', banklink)
                # if condition to handle duplicate links, and ../TWN eg in China 
                if (x not in banklinks and re.search('\.+/', x) == None):
                    banklinks.append(x)
    print(banklinks)
    return banklinks 
   
targetURLs = {
    "Afghanistan":"http://banknote.ws/COLLECTION/countries/ASI/AFG/AFG.htm",
    "Albania":"http://banknote.ws/COLLECTION/countries/EUR/ALB/ALB-BES.htm",
    "Algeria":'http://banknote.ws/COLLECTION/countries/AFR/ALG/ALG-BCABAD.htm',
    'Angola':'http://banknote.ws/COLLECTION/countries/AFR/ANG/ANG-BNA.htm',
    'Argentina':'http://banknote.ws/COLLECTION/countries/AME/ARG/ARG3BC.htm',
    'Armenia':'http://banknote.ws/COLLECTION/countries/ASI/ARM/ARM.htm',
    'Australia':'',
    'Austria':'http://banknote.ws/COLLECTION/countries/EUR/AUT/AUT-ONB.htm',
    'Azerbaijan':'http://banknote.ws/COLLECTION/countries/ASI/AZE/AZE.htm',
    'Bahamas':'http://banknote.ws/COLLECTION/countries/AME/BAH/BAH.htm',
    'Bahrain':'http://banknote.ws/COLLECTION/countries/ASI/BHR/BHR.htm',
    'Bangladesh':'http://banknote.ws/COLLECTION/countries/ASI/BDE/BDE.htm',
    'Barbados':'http://banknote.ws/COLLECTION/countries/AME/BBD/BBD.htm',
    'Belarus':'http://banknote.ws/COLLECTION/countries/EUR/BLR/BLR.htm',
    'Belgium':'http://banknote.ws/COLLECTION/countries/EUR/BEL/BEL-BNB.htm',  
    'Belize':'http://banknote.ws/COLLECTION/countries/AME/BLZ/BLZ-BLZ.htm',
    'Bhutan':'http://banknote.ws/COLLECTION/countries/ASI/BHU/BHU.htm',
    'Bolivia':'http://banknote.ws/COLLECTION/countries/AME/BOL/BOL-BCB.htm',
    'Bosnia & Herzegovina':'http://banknote.ws/COLLECTION/countries/EUR/BIH/BIH-CBBH.htm',
    'Botswana':'http://banknote.ws/COLLECTION/countries/AFR/BOT/BOT.htm',
    'Brazil':'',
    'Brunei':'http://banknote.ws/COLLECTION/countries/ASI/BRU/BRU.htm',
    'Bulgaria':'http://banknote.ws/COLLECTION/countries/EUR/BUL/BUL-BNB.htm',
    'Burundi':'http://banknote.ws/COLLECTION/countries/AFR/BUR/BUR.htm',
    'Cambodia':'http://banknote.ws/COLLECTION/countries/ASI/CMB/CMB.htm',
    'Canada':'http://banknote.ws/COLLECTION/countries/AME/CAN/CAN-BOC.htm',
    'Cape Verde':'http://banknote.ws/COLLECTION/countries/AFR/CVE/CVE.htm',
    'Chile':'http://banknote.ws/COLLECTION/countries/AME/CIL/CIL-BCC.htm',
    'China':'',
    'Colombia':'http://banknote.ws/COLLECTION/countries/AME/COL/COL-BDR.htm',
    'Comoros':'http://banknote.ws/COLLECTION/countries/AFR/COM/COM.htm',
    'Costa Rica':'http://banknote.ws/COLLECTION/countries/AME/CRI/CRI-BCC.htm',
    'Croatia':'http://banknote.ws/COLLECTION/countries/EUR/CRO/CRO-REP.htm',
    'Cuba':'http://banknote.ws/COLLECTION/countries/AME/CUB/CUB-BCC.htm',
    'Cyprus':'http://banknote.ws/COLLECTION/countries/EUR/CYP/CYP.htm',
    'Czech Republic':'http://banknote.ws/COLLECTION/countries/EUR/CZR/CZR.htm',
    'Democratic Republic of the Congo':'',
    'Denmark':'http://banknote.ws/COLLECTION/countries/EUR/DEN/DEN-NAT.htm',
    'Djibouti':'',
    'Dominican Republic':'',
    'Ecuador':'http://banknote.ws/COLLECTION/countries/AME/ECU/ECU-BCE.htm',
    'Egypt':'http://banknote.ws/COLLECTION/countries/AFR/EGY/EGY-NCB.htm',
    'El Salvador':'',
    'Eritrea':'http://banknote.ws/COLLECTION/countries/AFR/ERI/ERI.htm',
    'Estonia':'',
    'Ethiopia':'http://banknote.ws/COLLECTION/countries/AFR/ETH/ETH.htm',
    'Fiji':'',
    'Finland':'http://banknote.ws/COLLECTION/countries/EUR/FIN/FIN-FIB.htm',
    'France':'',
    'Gambia':'http://banknote.ws/COLLECTION/countries/AFR/GAM/GAM.htm',
    'Georgia':'http://banknote.ws/COLLECTION/countries/ASI/GEO/GEO.htm',
    'Germany':'http://banknote.ws/COLLECTION/countries/EUR/GFR/GFR.htm',
    'Ghana':'http://banknote.ws/COLLECTION/countries/AFR/GHA/GHA.htm',
    'Greece':'',
    'Guatemala':'',
    'Guinea':'http://banknote.ws/COLLECTION/countries/AFR/GUI/GUI.htm',
    'Guinea-Bissau':'http://banknote.ws/COLLECTION/countries/AFR/GUB/GUB-GUB.htm',
    'Guyana':'',
    'Haiti':'',
    'Honduras':'',
    'Hungary':'',
    'Iceland':'http://banknote.ws/COLLECTION/countries/EUR/ICE/ICE.htm',
    'India':'',
    'Indonesia':'',
    'Iran':'',
    'Iraq':'http://banknote.ws/COLLECTION/countries/ASI/IRQ/IRQ.htm',
    'Ireland':'',
    'Israel':'http://banknote.ws/COLLECTION/countries/ASI/ISR/ISR.htm',
    'Italy':'',
    'Jamaica':'',
    'Japan':'',
    'Jordan':'http://banknote.ws/COLLECTION/countries/ASI/JOR/JOR.htm',
    'Kazakhstan':'http://banknote.ws/COLLECTION/countries/ASI/KAZ/KAZ.htm',
    'Kenya':'http://banknote.ws/COLLECTION/countries/AFR/KEN/KEN.htm',
    'Kuwait':'http://banknote.ws/COLLECTION/countries/ASI/KUW/KUW.htm',
    'Kyrgyzstan':'http://banknote.ws/COLLECTION/countries/ASI/KYR/KYR.htm',
    'Lao PDR':'http://banknote.ws/COLLECTION/countries/ASI/LAO/LAO.htm',
    'Latvia':'',
    'Lebanon':'',
    'Lesotho':'http://banknote.ws/COLLECTION/countries/AFR/LES/LES.htm',
    'Liberia':'http://banknote.ws/COLLECTION/countries/AFR/LIB/LIB.htm',
    'Libya':'',
    'Lithuania':'',
    'Macedonia':'http://banknote.ws/COLLECTION/countries/EUR/MCD/MCD.htm',
    'Madagascar':'',
    'Malawi':'http://banknote.ws/COLLECTION/countries/AFR/MLW/MLW.htm',
    'Malaysia':'http://banknote.ws/COLLECTION/countries/ASI/MLY/MLY.htm',
    'Maldives':'http://banknote.ws/COLLECTION/countries/ASI/MLV/MLV.htm',
    'Malta':'http://banknote.ws/COLLECTION/countries/EUR/MLT/MLT.htm',
    'Mauritania':'http://banknote.ws/COLLECTION/countries/AFR/MAU/MAU.htm',
    'Mauritius':'',
    'Mexico':'',
    'Moldova':'http://banknote.ws/COLLECTION/countries/EUR/MOL/MOL.htm',
    'Mongolia':'http://banknote.ws/COLLECTION/countries/ASI/MON/MON.htm',
    'Morocco':'',
    'Mozambique':'',
    'Myanmar':'',
    'Namibia':'http://banknote.ws/COLLECTION/countries/AFR/NAM/NAM-NAM.htm',
    'Nepal':'http://banknote.ws/COLLECTION/countries/ASI/NEP/NEP.htm',
    'Netherlands':'',
    'New Zealand':'',
    'Nicaragua':'',
    'Nigeria':'http://banknote.ws/COLLECTION/countries/AFR/NIA/NIA.htm',
    'North Korea':'http://banknote.ws/COLLECTION/countries/ASI/KON/KON.htm',
    'Norway':'http://banknote.ws/COLLECTION/countries/EUR/NOR/NOR-NOB.htm',
    'Oman':'http://banknote.ws/COLLECTION/countries/ASI/OMA/OMA.htm',
    'Pakistan':'',
    'Papua New Guinea':'http://banknote.ws/COLLECTION/countries/AUS/PNG/PNG.htm',
    'Paraguay':'',
    'Peru':'',
    'Philippines':'',
    'Poland':'',
    'Portugal':'',
    'Qatar':'http://banknote.ws/COLLECTION/countries/ASI/QAT/QAT.htm',
    'Romania':'',
    'Russia':'http://banknote.ws/COLLECTION/countries/EUR/RUS/RUS-GENERAL/RUS-FED.htm',
    'Rwanda':'http://banknote.ws/COLLECTION/countries/AFR/RWA/RWA.htm',
    'South Sudan':'http://banknote.ws/COLLECTION/countries/AFR/SSD/SSD.htm',
    'Samoa':'http://banknote.ws/COLLECTION/countries/AUS/SAM/SAM.htm',
    'Sao Tome E Principe':'http://banknote.ws/COLLECTION/countries/AFR/STP/STP.htm',
    'Saudi Arabia':'http://banknote.ws/COLLECTION/countries/ASI/SAR/SAR.htm',
    'Serbia':'http://banknote.ws/COLLECTION/countries/EUR/SER/SER.htm',
    'Seychelles':'http://banknote.ws/COLLECTION/countries/AFR/SEY/SEY.htm',
    'Sierra Leone':'http://banknote.ws/COLLECTION/countries/AFR/SLE/SLE.htm',
    'Singapore':'http://banknote.ws/COLLECTION/countries/ASI/SIN/SIN.htm',
    'Slovakia':'http://banknote.ws/COLLECTION/countries/EUR/SVK/SVK.htm',
    'Slovenia':'http://banknote.ws/COLLECTION/countries/EUR/SLV/SLV.htm',
    'Solomon Islands':'http://banknote.ws/COLLECTION/countries/AUS/SOL/SOL.htm',
    'Somaliland':'http://banknote.ws/COLLECTION/countries/AFR/SOD/SOD.htm',
    'Somalia':'http://banknote.ws/COLLECTION/countries/AFR/SOM/SOM.htm',
    'South Africa':'',
    'South Korea':'http://banknote.ws/COLLECTION/countries/ASI/KOS/KOS.htm',
    'Spain':'',
    'Sri Lanka':'',
    'Sudan':'',
    'Suriname':'',
    'Swaziland':'http://banknote.ws/COLLECTION/countries/AFR/SWZ/SWZ.htm',
    'Sweden':'http://banknote.ws/COLLECTION/countries/EUR/SWE/SWE-SRB.htm',
    'Switzerland':'',
    'Syria':'',
    'Taiwan':'http://banknote.ws/COLLECTION/countries/ASI/TWN/TWN.htm',
    'Tajikistan':'http://banknote.ws/COLLECTION/countries/ASI/TAJ/TAJ.htm',
    'Tanzania':'http://banknote.ws/COLLECTION/countries/AFR/TAN/TAN.htm',
    'Thailand':'',
    'Tonga':'http://banknote.ws/COLLECTION/countries/AUS/TON/TON.htm',
    'Trinidad and Tobago':'http://banknote.ws/COLLECTION/countries/AME/TRT/TRT.htm',
    'Tunisia':'',
    'Turkey':'',
    'Turkmenistan':'http://banknote.ws/COLLECTION/countries/ASI/TKM/TKM.htm',
    'Uganda':'http://banknote.ws/COLLECTION/countries/AFR/UGA/UGA.htm',
    'Ukraine':'',
    'United Arab Emirates':'http://banknote.ws/COLLECTION/countries/ASI/UAE/UAE.htm',
    'United Kingdom':'',
    'United States':'http://banknote.ws/COLLECTION/countries/AME/USA/USA-FEDRES/USA-FEDRES.htm',
    'Uruguay':'',
    'Uzbekistan':'',
    'Vanuatu':'http://banknote.ws/COLLECTION/countries/AUS/VTU/VTU-VTU.htm',
    'Venezuela':'',
    'Vietnam':'',
    'Yemen':'http://banknote.ws/COLLECTION/countries/ASI/YEM/YEM.htm',
    'Zambia':'http://banknote.ws/COLLECTION/countries/AFR/ZAM/ZAM.htm',
    'Zimbabwe':'http://banknote.ws/COLLECTION/countries/AFR/ZIM/ZIM-ZIM.htm'
    }

# to avoid calling urlopen too many times 
targetURLs2 = {
    'Saudi Arabia':'http://banknote.ws/COLLECTION/countries/ASI/SAR/SAR.htm',
    'Serbia':'http://banknote.ws/COLLECTION/countries/EUR/SER/SER.htm',
    'Seychelles':'http://banknote.ws/COLLECTION/countries/AFR/SEY/SEY.htm',
    'Sierra Leone':'http://banknote.ws/COLLECTION/countries/AFR/SLE/SLE.htm',
    'Singapore':'http://banknote.ws/COLLECTION/countries/ASI/SIN/SIN.htm',
    'Slovakia':'http://banknote.ws/COLLECTION/countries/EUR/SVK/SVK.htm',
    'Slovenia':'http://banknote.ws/COLLECTION/countries/EUR/SLV/SLV.htm',
    'Solomon Islands':'http://banknote.ws/COLLECTION/countries/AUS/SOL/SOL.htm',
    'Somaliland':'http://banknote.ws/COLLECTION/countries/AFR/SOD/SOD.htm',
    'Somalia':'http://banknote.ws/COLLECTION/countries/AFR/SOM/SOM.htm',
    'South Africa':'',
    'South Korea':'http://banknote.ws/COLLECTION/countries/ASI/KOS/KOS.htm',
    'Spain':'',
    'Sri Lanka':'',
    'Sudan':'',
    'Suriname':'',
    'Swaziland':'http://banknote.ws/COLLECTION/countries/AFR/SWZ/SWZ.htm',
    'Sweden':'http://banknote.ws/COLLECTION/countries/EUR/SWE/SWE-SRB.htm',
    'Switzerland':'',
    'Syria':'',
    'Taiwan':'http://banknote.ws/COLLECTION/countries/ASI/TWN/TWN.htm',
    'Tajikistan':'http://banknote.ws/COLLECTION/countries/ASI/TAJ/TAJ.htm',
    'Tanzania':'http://banknote.ws/COLLECTION/countries/AFR/TAN/TAN.htm',
    'Thailand':'',
    'Tonga':'http://banknote.ws/COLLECTION/countries/AUS/TON/TON.htm',
    'Trinidad and Tobago':'http://banknote.ws/COLLECTION/countries/AME/TRT/TRT.htm',
    'Tunisia':'',
    'Turkey':'',
    'Turkmenistan':'http://banknote.ws/COLLECTION/countries/ASI/TKM/TKM.htm',
    'Uganda':'http://banknote.ws/COLLECTION/countries/AFR/UGA/UGA.htm',
    'Ukraine':'',
    'United Arab Emirates':'http://banknote.ws/COLLECTION/countries/ASI/UAE/UAE.htm',
    'United Kingdom':'',
    'United States':'',
    'Uruguay':'',
    'Uzbekistan':'',
    'Vanuatu':'http://banknote.ws/COLLECTION/countries/AUS/VTU/VTU-VTU.htm',
    'Venezuela':'',
    'Vietnam':'',
    'Yemen':'http://banknote.ws/COLLECTION/countries/ASI/YEM/YEM.htm',
    'Zambia':'http://banknote.ws/COLLECTION/countries/AFR/ZAM/ZAM.htm',
    'Zimbabwe':'http://banknote.ws/COLLECTION/countries/AFR/ZIM/ZIM-ZIM.htm'
    }


three_let_code = {
    'AFG':'Afghanistan',
    'ALB':'Albania',
    'ALG':'Algeria',
    'ANG':'Angola',
    'ARG':'Argentina',
    'ARM':'Armenia',
    'AUS':'Australia',
    'AUT':'Austria',
    'AZE':'Azerbaijan',
    'BAH':'Bahamas',
    'BHR':'Bahrain',
    'BDE':'Bangladesh',
    'BBD':'Barbados',
    'BLR':'Belarus',
    'BEL':'Belgium',
    'BLZ':'Belize',
    'BHU':'Bhutan',
    'BOL':'Bolivia',
    'BIH':'Bosnia & Herzegovina',
    'BOT':'Botswana',
    'BRA':'Brazil',
    'BRU':'Brunei',
    'BUL':'Bulgaria',
    'BUR':'Burundi',
    'CMB':'Cambodia',
    'CAN':'Canada',
    'CVE':'Cape Verde',
    'CIL':'Chile',
    'CIN':'China',
    'COL':'Colombia',
    'COM':'Comoros',
    'CRI':'Costa Rica',
    'CRO':'Croatia',
    'CUB':'Cuba',
    'CYP':'Cyprus',
    'CZR':'Czech Republic',
    'CDR':'Democratic Republic of the Congo',
    'DEN':'Denmark',
    'DJI':'Djibouti',
    'DOR':'Dominican Republic',
    'ECU':'Ecuador',
    'EGY':'Egypt',
    'ESV':'El Salvador',
    'ERI':'Eritrea',
    'EST':'Estonia',
    'ETH':'Ethiopia',
    'FIJ':'Fiji',
    'FIN':'Finland',
    'FRA':'France',
    'GAM':'Gambia',
    'GEO':'Georgia',
    'GFR':'Germany',
    'GHA':'Ghana',
    'GRC':'Greece',
    'GTM':'Guatemala',
    'GUI':'Guinea',
    'GUB':'Guinea-Bissau',
    'GUY':'Guyana',
    'HAI':'Haiti',
    'HON':'Honduras',
    'HUN':'Hungary',
    'ICE':'Iceland',
    'IND':'India',
    'INO':'Indonesia',
    'IRN':'Iran',
    'IRQ':'Iraq',
    'IRL':'Ireland',
    'ISR':'Israel',
    'ITA':'Italy',
    'JAM':'Jamaica',
    'JAP':'Japan',
    'JOR':'Jordan',
    'KAZ':'Kazakhstan',
    'KEN':'Kenya',
    'KUW':'Kuwait',
    'KYR':'Kyrgyzstan',
    'LAO':'Lao PDR',
    'LAT':'Latvia',
    'LEB':'Lebanon',
    'LES':'Lesotho',
    'LIB':'Liberia',
    'LIY':'Libya',
    'LIT':'Lithuania',
    'MCD':'Macedonia',
    'MAD':'Madagascar',
    'MLW':'Malawi',
    'MLY':'Malaysia',
    'MLV':'Maldives',
    'MLT':'Malta',
    'MAU':'Mauritania',
    'MRS':'Mauritius',
    'MEX':'Mexico',
    'MOL':'Moldova',
    'MON':'Mongolia',
    'MRQ':'Morocco',
    'MOZ':'Mozambique',
    'MYA':'Myanmar',
    'NAM':'Namibia',
    'NEP':'Nepal',
    'NDL':'Netherlands',
    'NZL':'New Zealand',
    'NIC':'Nicaragua',
    'NIA':'Nigeria',
    'KON':'North Korea',
    'NOR':'Norway',
    'OMA':'Oman',
    'PAK':'Pakistan',
    'PNG':'Papua New Guinea',
    'PGY':'Paraguay',
    'PER':'Peru',
    'PIL':'Philippines',
    'POL':'Poland',
    'POR':'Portugal',
    'QAT':'Qatar',
    'ROM':'Romania',
    'RUS':'Russia',
    'RWA':'Rwanda',
    'SSD':'South Sudan',
    'SAM':'Samoa',
    'STP':'Sao Tome E Principe',
    'SAR':'Saudi Arabia',
    'SER':'Serbia',
    'SEY':'Seychelles',
    'SLE':'Sierra Leone',
    'SIN':'Singapore',
    'SVK':'Slovakia',
    'SLV':'Slovenia',
    'SOL':'Solomon Islands',
    'SOD':'Somaliland',
    'SOM':'Somalia',
    'SAF':'South Africa',
    'KOS':'South Korea',
    'SPA':'Spain',
    'SLK':'Sri Lanka',
    'SUD':'Sudan',
    'SUR':'Suriname',
    'SWZ':'Swaziland',
    'SWE':'Sweden',
    'SUI':'Switzerland',
    'SYR':'Syria',
    'TWN':'Taiwan',
    'TAJ':'Tajikistan',
    'TAN':'Tanzania',
    'THL':'Thailand',
    'TON':'Tonga',
    'TRT':'Trinidad and Tobago',
    'TUN':'Tunisia',
    'TUR':'Turkey',
    'TKM':'Turkmenistan',
    'UGA':'Uganda',
    'UKR':'Ukraine',
    'UAE':'United Arab Emirates',
    'GBR':'United Kingdom',
    'USA':'United States',
    'URU':'Uruguay',
    'UZB':'Uzbekistan',
    'VTU':'Vanuatu',
    'VEN':'Venezuela',
    'VIE':'Vietnam',
    'YEM':'Yemen',
    'ZAM':'Zambia',
    'ZIM':'Zimbabwe'
    }

# trick to flip above dict, need it for countries w/ multiple banks 
three_let_inverse = {v: k for k, v in three_let_code.items()}

continentCode = {
    'AFG':'ASI',
    'ALB':'EUR',
    'ALG':'AFR',
    "ANG":"AFR",
    "ARG":"AME",
    "ARM":"ASI",
    "AUS":"AUS",
    "AUT":"EUR",
    "AZE":"ASI",
    "BAH":"AME",
    "BHR":"ASI",
    "BDE":"ASI",
    "BBD":"AME",
    "BLR":"EUR",
    "BEL":"EUR",
    'BLZ':'AME',
    'BHU':'ASI',
    'BOL':'AME',
    'BIH':'EUR',
    'BOT':'AFR',
    'BRA':'AME',
    'BRU':'ASI',
    'BUL':'EUR',
    'BUR':'AFR',
    'CMB':'ASI',
    'CAN':'AME',
    'CVE':'AFR',
    'CIL':'AME',
    'CIN':'ASI',
    'COL':'AME',
    'COM':'AFR',
    'CRI':'AME',
    'CRO':'EUR',
    'CUB':'AME',
    'CYP':'EUR',
    'CZR':'EUR',
    'CDR':'AFR',
    'DEN':'EUR',
    'DJI':'AFR',
    'DOR':'AME',
    'ECU':'AME',
    'EGY':'AFR',
    'ESV':'AME',
    'ERI':'AFR',
    'EST':'EUR',
    'ETH':'AFR',
    'FIN':'EUR',
    'FIJ':'AUS',
    'FRA':'EUR',
    'GAM':'AFR',
    'GEO':'ASI',
    'GFR':'EUR',
    'GHA':'AFR',
    'GRC':'EUR',
    'GTM':'AME',
    'GUI':'AFR',
    'GUB':'AFR',
    'GUY':'AME',
    'HAI':'AME',
    'HON':'AME',
    'HUN':'EUR',
    'ICE':'EUR',
    'IND':'ASI',
    'INO':'ASI',
    'IRN':'ASI',
    'IRQ':'ASI',
    'IRL':'EUR',
    'ISR':'ASI',
    'ITA':'EUR',
    'JAM':'AME',
    'JAP':'ASI',
    'JOR':'ASI',
    'KAZ':'ASI',
    'KEN':'AFR',
    'KUW':'ASI',
    'KYR':'ASI',
    'LAO':'ASI',
    'LAT':'EUR',
    'LEB':'ASI',
    'LES':'AFR',
    'LIB':'AFR',
    'LIY':'AFR',
    'LIT':'EUR',
    'MCD':'EUR',
    'MAD':'AFR',
    'MLW':'AFR',
    'MLY':'ASI',
    'MLV':'ASI',
    'MLT':'EUR',
    'MAU':'AFR',
    'PER':'AME',
    'MRS':'AFR',
    'MEX':'AME',
    'MOL':'EUR',
    'MON':'ASI',
    'MRQ':'AFR',
    'MOZ':'AFR',
    'MYA':'ASI',
    'NAM':'AFR',
    'NEP':'ASI',
    'NDL':'EUR',
    'NZL':'AUS',
    'NIC':'AME',
    'NIA':'AFR',
    'KON':'ASI',
    'NOR':'EUR',
    'OMA':'ASI',
    'PAK':'ASI',
    'PNG':'AUS',
    'PGY':'AME',
    'PIL':'ASI',
    'POL':'EUR',
    'POR':'EUR',
    'QAT':'ASI',
    'ROM':'EUR',
    'RUS':'EUR',
    'RWA':'AFR',
    'SSD':'AFR',
    'SAM':'AUS',
    'STP':'AFR',
    'SAR':'ASI',
    'SER':'EUR',
    'SEY':'AFR',
    'SLE':'AFR',
    'SIN':'ASI',
    'SVK':'EUR',
    'SLV':'EUR',
    'SOL':'AUS',
    'SOD':'AFR',
    'SOM':'AFR',
    'SAF':'AFR',
    'KOS':'ASI',
    'SPA':'EUR',
    'SLK':'ASI',
    'SUD':'AFR',
    'SUR':'AME',
    'SWZ':'AFR',
    'SWE':'EUR',
    'SUI':'EUR',
    'SYR':'ASI',
    'TWN':'ASI',
    'TAJ':'ASI',
    'TAN':'AFR',
    'THL':'ASI',
    'TON':'AUS',
    'TRT':'AME',
    'TUN':'AFR',
    'TUR':'ASI',
    'TKM':'ASI',
    'UGA':'AFR',
    'UKR':'EUR',
    'UAE':'ASI',
    'GBR':'EUR',
    'USA':'AME',
    'URU':'AME',
    'UZB':'ASI',
    'VTU':'AUS',
    'VEN':'AME',
    'VIE':'ASI',
    'YEM':'ASI',
    'ZAM':'AFR',
    'ZIM':'AFR'
    }

# testing purposes, replace targetURLs in the main body with this when testing
testURLs = {
    'Cambodia':'http://banknote.ws/COLLECTION/countries/ASI/CMB/CMB.htm',
    'China':'http://banknote.ws/COLLECTION/countries/ASI/CIN/CIN-PR/CIN-PR.htm',
    }

# add country names to allBanknotes dictionary
for key in targetURLs:
    allBanknotes[key] = {}

recentnotes = []
for country in targetURLs:
    print(country + ' as normal')
    if targetURLs[country] != '':
        page = urlopen(targetURLs[country], timeout=100)
        extractBanknotes(page, recentnotes)
    else:
        print(country + ' >1 page')
        code = three_let_inverse[country]
        continent = continentCode[code]
        coverURL = 'http://banknote.ws/COLLECTION/countries/' + continent + '/' + code + '/' + code + '.htm'
       # handle Italy exception 
        if(code=='ITA'):
            coverURL = 'http://banknote.ws/COLLECTION/countries/EUR/ITA/ITAoverview.htm'
        for banklink in getBanks(coverURL):
            target = 'http://banknote.ws/COLLECTION/countries/' + continent + '/' + code + '/' + banklink
            print(target)
            page = urlopen(target, timeout=100)
            extractBanknotes(page, recentnotes)

            
                    
#build banknote.ws link
for note in recentnotes:
    countrycode = note[0:3]
    try:
        country = three_let_code[countrycode]
        continent = continentCode[countrycode]
        code2 = ''
        # special exceptions for large countries 
        if countrycode=='CIN':
            code2 = '/CIN-PR'
        elif countrycode=='RUS':
            code2 = '/RUS-GENERAL'
        elif countrycode=='MEX':
            code2 = '/MEX-GENERAL'
        elif countrycode=='USA':
            code2 = '/USA-FEDRES'
        url = 'http://banknote.ws/COLLECTION/countries/' + continent + '/' + countrycode + code2 + '/' + note 
        print(url)
        extractText(url, country)
    except:
        print('Did not find country!')
   
    
# write to CSV     
with open('missing-banknotes-data.csv', 'w', newline='', encoding="utf-8-sig") as csvfile:
    banknotewriter = csv.writer(csvfile, delimiter=',')
    banknotewriter.writerow(['country', 'pick', 'denomination', 'currency_name', 'date', 'issuer', 'front_text', 'back_text'])
    for country in targetURLs:
        for number in allBanknotes[country].keys():
                banknotewriter.writerow([country, allBanknotes[country][number]['number'], 
                                         allBanknotes[country][number]['denomination'],
                                         allBanknotes[country][number]['currencyname'],
                                         allBanknotes[country][number]['date'],
                                         allBanknotes[country][number]['issuer'],
                                         allBanknotes[country][number]['fronttext'],
                                         allBanknotes[country][number]['backtext']])



