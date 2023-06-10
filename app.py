from flask import Flask,jsonify,request
import json
from bs4 import BeautifulSoup
from flask_cors import CORS
from time import sleep
import requests
import datetime
import numpy as np 
import pandas as pd 
from statsmodels.tsa.arima.model import ARIMA
app = Flask(__name__)
CORS(app)
from markupsafe import escape
@app.route("/rec")
def recomendation(): 
    stocks=['RACC',
 'SCTS',
 'TRTO',
 'OIH',
 'HELI',
 'ORWE',
 'RUBX',
 'TRST',
 'AJWA',
 'COSG',
 'DOMT',
 'DSCW',
 'EAST',
 'EDFM',
 'EFID',
 'INFI',
 'JUFO',
 'KABO',
 'OLFI',
 'CIRA',
 'EGSA',
 'ELWA',
 'GOCO',
 'MHOT',
 'MMAT',
 'MPRC',
 'PHTV',
 'SDTI',
 'SPHT',
 'TALM',
 'GBCO',
 'GMCI',
 'IBCT',
 'ICMI',
 'ISPH',
 'MBEN',
 'MKIT',
 'MTIE',
 'SMFR',
 'ACAMD',
 'ADIB',
 'ADRI',
 'AFDI',
 'AMER',
 'AMIA',
 'ANFI',
 'ARAB',
 'AREH',
 'ASPI',
 'ATLC',
 'BINV',
 'BTFH',
 'CANA',
 'CCAP',
 'CCRS',
 'CICH',
 'CIEB',
 'CNFN',
 'COMI',
 'COPR',
 'DAPH',
 'DCRC',
 'DEIN',
 'EALR',
 'EASB',
 'EBSC',
 'EGBE',
 'EHDR',
 'EIUD',
 'EKHO',
 'EKHOA',
 'ELKA',
 'ELSH',
 'EMFD',
 'EOSB',
 'EXPA',
 'FAIT',
 'FAITA',
 'FIRE',
 'GPPL',
 'GRCA',
 'HDBK',
 'HRHO',
 'ICID',
 'ICLE',
 'IDRE',
 'KRDI',
 'KWIN',
 'MAAL',
 'MENA',
 'MNHD',
 'MOIN',
 'NAHO',
 'NHPS',
 'OBRI',
 'OCDI',
 'ODIN',
 'OFH',
 'ORHD',
 'PHDC',
 'PRDC',
 'PRMH',
 'QNBA',
 'REAC',
 'ROTO',
 'RREI',
 'RTVC',
 'SAIB',
 'SAUD',
 'SEIG',
 'TANM',
 'TMGH',
 'UNIT',
 'UTOP',
 'ZMID',
 'CLHO',
 'IDHC',
 'NINH',
 'SPMD',
 'UPMS',
 'AXPH',
 'BIOC',
 'CPCI',
 'MCRO',
 'MIPH',
 'MPCI',
 'NIPH',
 'OCPH',
 'PHAR',
 'RMDA',
 'SIPC',
 'EDBM',
 'FNAR',
 'GGCC',
 'IEEC',
 'MOIL',
 'NCCW',
 'NDRL',
 'ORAS',
 'UEGC',
 'WKOL',
 'ARCC',
 'ASCM',
 'ATQA',
 'EGAL',
 'ESRS',
 'IRAX',
 'IRON',
 'ISMQ',
 'MBSC',
 'MCQE',
 'MISR',
 'PRCL',
 'SCEM',
 'SVCE',
 'ACGC',
 'AIFI',
 'APSW',
 'BIDI',
 'CEFM',
 'DTPP',
 'EFIC',
 'EGCH',
 'ELNA',
 'EPCO',
 'EPPK',
 'FERC',
 'GTWL',
 'ICFC',
 'IFAP',
 'ISMA',
 'KZPC',
 'MEGM',
 'MEPA',
 'MFPC',
 'MICH',
 'MILS',
 'MOSC',
 'MPCO',
 'NEDA',
 'PACH',
 'POUL',
 'RAKT',
 'RKAZ',
 'SCFM',
 'SKPC',
 'SNFC',
 'SPIN',
 'SUGR',
 'UEFM',
 'UNIP',
 'WCDF',
 'ZEOT',
 'ARVA',
 'CERA',
 'ECAP',
 'ELEC',
 'ENGC',
 'GDWA',
 'INEG',
 'LCSW',
 'PTCC',
 'SWDY',
 'AIVC',
 'GSSC',
 'MFSC',
 'EFIH',
 'FWRY',
 'RAYA',
 'VERT',
 'CSAG',
 'ETRS',
 'UASG',
 'EGTS']
    recom=[]
    for i in stocks[:5] :
            ss=requests.get(f"https://scrap-29ek.onrender.com/stock/{i}/{1095}")
            ss=ss.json()
            datetime=[]
            open=[]
            high=[]
            low=[]
            close=[]
            volume=[]
            for i in ss['data']:
                list=[]
                for j in i : 
                    list.append(j)
                datetime.append(list[0])
                open.append(list[2])
                high.append(list[3])
                low.append(list[4])
                close.append(list[5])
                volume.append(list[6])
            dic={'datetime':datetime,'Open':open,'High':high,'Low':low,'Close':close,'Volume':volume}
            data=pd.DataFrame(dic)
            data['datetime'] = pd.to_datetime(data['datetime'])
            data = data.set_index('datetime')
            X = data['Close'].values
            history = [x for x in X]
            predictions = []
            # walk-forward validation
            import statsmodels.api as sm
            model = ARIMA(history, order=((1,1,2)))
            model_fit = model.fit()
            output = model_fit.forecast(steps=180)
            res=[]
            maxx=0
            for i in output:
                     res.append(i)
                     maxx=max(maxx,i)
            recom.append([((maxx-close[-1])/10),d,res[-1],close[-1]])
    recom.sort(reverse=True)
    results=[]
    for m in recom[:10] :
        results.append(m[1])
    return results
@app.route("/")
def home():
    data = {'page':'home page','message':'ok'}
    return jsonify(data)
###########################
app.run(debug=False,host='0.0.0.0')
