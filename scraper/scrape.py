import requests
import json
import pandas as pd

URL = "https://tcp-us-prod-rnd.shl.com/voiceRater/shl-ai-hiring/shl_product_catalog.json"

response = requests.get(URL)
text = response.text

# Fix the malformed newline in "Microsoft 365 (New)"
text = text.replace('"Microsoft \n    365 (New)"', '"Microsoft 365 (New)"')

data = json.loads(text)

print("Total records:", len(data))

df = pd.DataFrame(data)
df.to_csv("catalog/shl_catalog.csv", index=False)

print("CSV saved successfully!")