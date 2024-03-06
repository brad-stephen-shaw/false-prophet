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


def count_bank_holidays(data, date_column, name='holiday_bank_count', proportion=False, append=True):
    '''
    Function to count bank holidays
    '''
    
    d = pd.DataFrame(index=data.index)
    d[name] = data[date_column].apply(count_holidays_helper)
    
    if proportion:
        d[f'{name}_prop'] = d[name] / data[date_column].dt.days_in_month
        
    if append:
        return pd.concat([data, d], axis=1)
    
    else:
        return d
    
