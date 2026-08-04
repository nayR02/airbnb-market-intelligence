from scraper.loader import load_all_cities

df = load_all_cities()
print(df.shape)
print(df.head())
print(df["city"].value_counts())