"""
    통합 데이터 로더
"""
import pandas as pd

from loder import load_prices, load_companies, load_sectors

def load_merged():
    """
    시세(prices) + 종목(companies) + 섹터(sectors) 반환
        - 각각 데이터를 불러와서 결합하여 반환
    """
    prices = load_prices()
    companies = load_companies()
    sectors = load_sectors().rename(columns={"code":"sectorCode", "name":"sector"})

    df = (prices.merge(companies[['code', 'name', 'sectorCode', 'market']], on='code', how='left', validate='many_to_one')
            .merge(sectors[['sectorCode', 'sector']], on='sectorCode', how='left', validate='many_to_one'))
    
    return df.sort_values(['code', 'date']).reset_index(drop=True)