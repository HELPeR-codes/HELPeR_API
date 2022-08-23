import pandas as pd
import datetime as dt2
from datetime import datetime
from blueprints.annotation_endpoints.anno_config import aconfig
import json
import pathlib
import copy

annotation_folder = aconfig.annotation_folder

def updates(from_date):
    dt=None
    try:
        dt = datetime.strptime(from_date,"%m-%d-%Y")
    except Exception:
        print("cannot parse date ")
        return json.dumps({"error":"not able to parse date"})

    print(dt,datetime.now())

    if dt > datetime.now():
        return json.dumps({"error":"future date"})

    if dt is None:
        return json.dumps({"error":"none date"})
    df_latest=None
    df = None
    startdate=dt
    enddate = datetime.now()
    print(startdate,enddate)
    while startdate < enddate:
        print(annotation_folder,datetime.strftime(startdate,"%y_%-m_%-d"))
        for file in list(pathlib.Path(annotation_folder).glob('*_daily_'+datetime.strftime(startdate,"%y_%m_%d")+'*')):
            print(file)
            dftemp = pd.read_json(file)
            dftemp['date']=startdate
            if df is None:
                df=copy.copy(dftemp)
            else:
                df = pd.concat([df,copy.copy(dftemp)])
        startdate = startdate + dt2.timedelta(days=1)
    if df is not None:
        df_latest = df.sort_values('date').drop_duplicates('id', keep='last')
        print("No of json objects sent", len(df_latest))
        return df_latest.to_json(orient="records")
    return {}


if __name__ == '__main__':
    # a = updates(from_date="04-18-2022")
    # print(a)

    a= updates(from_date="01-01-2020")
    print(a)





