import pandas as pd
from datetime import datetime
import numpy as np

def bnh (
    _df,
    _start = '2010-01-01',
    _end = datetime.now(),
    _col = 'Adj Close'
) : 
    # 데이터프레임의 복사본 생성
    df = _df.copy()
    # Date가 컬럼에 존재하면 Date를 인덱스로 변경
    if 'Date' in df.columns : 
        df.set_index('Date',inplace = True)
    # 인덱스를 시계열 데이터로 변경
    df.index = pd.to_datetime(df.index)
    # 결측치와 무한대 값 제거
    flag = df.isin([np.nan,np.inf,-np.inf]).any(axis = 1)
    df = df.loc[~flag,]

    try : 
        df = df.loc[_start:_end,[_col]]
    except Exception as e : 
        print(e)
        print('인자값이 잘못입력되었습니다.')
        return ""
    # 일별 수익율 계산하여 rtn 컬럼에 대입
    df['rtn'] = (df[_col].pct_change() + 1).fillna(1)
    # 누적 수익율 계산하여 acc_rtn 컬럼에 대입
    df['acc_rtn'] = df['rtn'].cumprod()
    acc_rtn = df.iloc[-1,-1]

    return df,acc_rtn