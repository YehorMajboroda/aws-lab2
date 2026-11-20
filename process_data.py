import json
import urllib.request
import boto3
import pandas as pd

bucket_name = "sumdu-lab2-yehor-2026"
dates = [f"2022{month:02d}01" for month in range(1, 13)]
data_all = []

print("Завантаження даних НБУ за 2022 рік...")
for d in dates:
    url_usd = f"https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?valcode=USD&date={d}&json"
    url_eur = f"https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?valcode=EUR&date={d}&json"

    req_usd = urllib.request.urlopen(url_usd)
    req_eur = urllib.request.urlopen(url_eur)

    data_all.extend(json.loads(req_usd.read().decode("utf-8")))
    data_all.extend(json.loads(req_eur.read().decode("utf-8")))

df = pd.DataFrame(data_all)
csv_file = "currency_rates.csv"
df.to_csv(csv_file, index=False)

s3 = boto3.client("s3")
s3.upload_file(csv_file, bucket_name, "data/currency_rates.csv")
print("Дані за 2022 рік успішно завантажено на S3!")
