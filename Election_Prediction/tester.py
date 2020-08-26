import pandas as pd

cars = {
        'Brand': ['Honda Civic','Toyota Corolla','Ford Focus','Audi A4', 'Honda Civic'],
        'Price': [22000,25000,27000,35000,18000]
        }

df = pd.DataFrame(cars, columns = ['Brand', 'Price'])

#print (df)

grouped = df.groupby('Brand')['Price'].sum()['Honda Civic']

#print(grouped)

def list_comp(df):
  return df.assign(is_rich=['RED' if df['Brand'][0] == df['Price'][0] else 'no' for x in df['Price']])

list_comp(df)
print(df)
print(df['Brand'][0])

for x in df['Price']:
    print(x, y)