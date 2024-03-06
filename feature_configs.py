import numpy as np

date_feature_definitions_monthly = {
    'trend_yr': lambda u: u.year,
    'trend_qtr': lambda u: u.quarter,
    'trend_mth': lambda u: u.month,
    'season_qtr_cos': lambda u: np.cos(2 * np.pi * (u.quarter - 1) / 4),
    'season_qtr_sin': lambda u: np.sin(2 * np.pi * (u.quarter - 1) / 4),
    'season_mth_cos': lambda u: np.cos(2 * np.pi * (u.month - 1) / 12),
    'season_mth_sin': lambda u: np.sin(2 * np.pi * (u.month - 1) / 12),
    'season_is_jan': lambda u: (u.month == 1) * 1,
    'season_is_mar': lambda u: (u.month == 3) * 1,
    'season_is_apr': lambda u: (u.month == 4) * 1,
    'season_is_dec': lambda u: (u.month == 12) * 1,
}

