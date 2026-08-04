from scraper.loader import load_all_cities
from scraper.cleaner import run_cleaning_pipeline, save_cleaned

df_raw = load_all_cities()
df_clean = run_cleaning_pipeline(df_raw)
save_cleaned(df_clean)

print(df_clean.shape)
print(df_clean.dtypes)
print(df_clean.isnull().sum())