import pandas as pd
import numpy as np
import holidays

def create_date_features(data, date_column, feature_definitions, append=False):
    '''
    Function to create date-based features.
    '''
    
    # copy
    d = pd.DataFrame(index=data.index)
    
    # update
    for feature in feature_definitions.keys():
        d[feature] = data[date_column].apply(feature_definitions[feature])
        
    if append:
        return pd.concat([data, d], axis=1)
    
    else:
        return d
    
    
def count_business_days(data, date_column, name='holiday_business_day_count', proportion=False, append=True):
    '''
    Function to count business days in month
    '''
    
    d = pd.DataFrame(index=data.index)
    
    begin = data[date_column].values.astype('datetime64[D]')
    end = (data[date_column] + pd.DateOffset(months=1)).values.astype('datetime64[D]')
    
    d[name] = np.busday_count(begindates=begin, enddates=end)
    
    if proportion:
        d[f'{name}_prop'] = d[name] / data[date_column].dt.days_in_month
        
    if append:
        return pd.concat([data, d], axis=1)
    
    else:
        return d
    

def count_holidays_helper(u, region='GB'):
    '''
    Helper function to count bank holidays
    '''
    
    hols = holidays.country_holidays(region)
    days = pd.date_range(u, u + pd.DateOffset(months=1))
    return sum(y in hols for y in days)


def count_bank_holidays(data, date_column, name='holiday_bank_count', region='GB', proportion=False, append=True):
    '''
    Function to count bank holidays
    '''
    
    d = pd.DataFrame(index=data.index)
    d[name] = data[date_column].apply(count_holidays_helper, region=region)
    
    if proportion:
        d[f'{name}_prop'] = d[name] / data[date_column].dt.days_in_month
        
    if append:
        return pd.concat([data, d], axis=1)
    
    else:
        return d
    
    

def create_relu(data, date_column, dates, append=True):
    '''
    Function to create a ReLU based on difference in months between
    dates and data[date_column].
    Returns a column for each date in dates.
    '''
    
    d = pd.DataFrame()
    
    for date in dates:
        
        # get difference in months
        delta = (data[date_column].dt.year * 12 + data[date_column].dt.month) - (date.year * 12 + date.month)
        relu = np.maximum(0, delta)
        
        d = pd.concat([d, pd.DataFrame({f"trend_relu_{date.strftime('%Y%m')}": relu})], axis=1)
        
    
    if append:
        return pd.concat([data, d], axis=1)
    
    else:
        return d
    
    
def create_change_points(data, date_column, dates, append=True):
    '''
    Function to create a change point. Will be 1 where dates >= data[date_column].
    Returns a column for each date in dates.
    '''
    
    d = pd.DataFrame()
    
    for date in dates:
        
        # get difference in months
        d = pd.concat(
                [d, pd.DataFrame({f"trend_change_{date.strftime('%Y%m')}": (data[date_column] >= date) * 1})],
                axis=1)
        
    
    if append:
        return pd.concat([data, d], axis=1)
    
    else:
        return d
    
    
def create_fourier_seasonality(data, periodicity, n_components, append=True):
    '''
    Function to create Fourier seasonality.
    '''
    
    idx = np.arange(len(data))
    d = pd.DataFrame()
    
    for n in range(1, n_components + 1):
        d[f'season_fourier_cos_{n}'] = np.cos(2 * np.pi * n * idx / periodicity)
        d[f'season_fourier_sin_{n}'] = np.sin(2 * np.pi * n * idx / periodicity)
        
    if append:
        return pd.concat([data, d], axis=1)
    
    else:
        return d  