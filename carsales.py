#!/usr/bin/env python
# coding: utf-8

print("This is the implementation of Dataquest's \"Exploring eBay Car Sales Data\" guided project, which, as the name suggests, uses a dataset of eBay car listings in Germany.")

import numpy as np
import pandas as pd
import os

dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, 'autos.csv')

autos = pd.read_csv(filename, encoding='Latin-1')

print("Informações Gerais do dataset:")
print(autos.info())
print("Head do dataset:")
print(autos.head())


print("Observations: The dataset seems to be mostly intact. Most of the columns contain the full 50K entries, but a few of them such as \"notRepairedDamage\" and \"vehicleType\" are missing quite a few thousand entries.")
#Cleaning Column Names

autos.columns = ['date_crawled', 'name', 'seller', 'offer_type', 'price', 'abtest',
       'vehicle_type', 'registration_year', 'gearbox', 'power_ps', 'model',
       'odometer', 'registration_month', 'fuel_type', 'brand',
       'unrepaired_damage', 'ad_created', 'nr_of_pictures', 'postal_code',
       'last_seen']

print(autos.head())

print("In this section we basically just cleaned up the name of the columns without altering any data.")
print("Data Exploration")

print(autos.describe(include='all'))

print("Apparently the columns \"seller\", \"offer_type\", \"abtest\", \"vehicle_type\", \"gearbox\" and \"odometer\" all have very low numbers of unique entries, which may indicate they are good candidates for being dropped.")
print("Strangely, \"registration_year\", \"registration_month\", \"nr_of_pictures\" and \"postal_code\" seem to return NAN, which is counter intuitive.")
print("Let's investigate this further.")

print(autos.registration_year.value_counts())
print(autos.nr_of_pictures.value_counts())
print(autos.postal_code.value_counts())
print(autos.registration_month.value_counts())

print("Analyzing theses results we can tell that, appart from \"nr_of_pictures\", all other columns with NAN in unique actually have many distinct values. For some reason describe() isn't being able to parse this data correctly. Therefore, we are going to drop \"nr_of_pictures\".")

autos = autos.drop(["nr_of_pictures"], axis=1)
print(autos.head())
print(autos.dtypes)

print("From the code above we can tell which columns are objects (in this case strings) and which are integer numbers. We wish to change \"price\" and \"odometer\" from strings to numbers.")

autos.price = (autos.price
                    .str.replace("$","")
                    .str.replace(",","")
                    .astype(int))
print(autos.price.head())

autos.odometer = (autos.odometer
                    .str.replace("km","")
                    .str.replace(",","")
                    .astype(int))
autos.rename({"odometer" : "odometer_km"}, axis=1, inplace=True)
print(autos.odometer_km.head())

print("Continuing Exploration of Columns")
print("We will continue exploring odometer_km and price to try and find outliers so we can remove them.")

print(autos.odometer_km.unique().shape)
print(autos.price.unique().shape)
print(autos.odometer_km.describe())
print(autos.price.describe())
print(autos.odometer_km.value_counts().sort_index(ascending=True))

print("There doesn't seem to be anything unusual with the ranges of the odometer_km column, so we will leave it as is.")

print(autos.price.value_counts().sort_index(ascending=True))

print("It seems there are a few cars both on the very low end (zero euros) and very high end (99 million euros) of prices. To fix this we could create a minimum and maximum value and then filter our price column to these values. I arbitrarily chose that 1 euro and 1 million euros would be the minimum and maximum, respectively.")

autos = autos[autos.price.between(1, 1000000)]

print(autos.price.value_counts().sort_index(ascending=True))

print("Understanding Date Ranges")

print((autos.date_crawled
             .str[:10]
             .value_counts(normalize=True, dropna=False)
             .sort_index()))

print("From exploring date_crawled we can gather that the crawling was made over roughly a month, from March 5th, 2016 to April 7th, 2016. Beyond that, there doesn't seem to be any day which had a lot more crawling done than any other.")

print((autos.last_seen
             .str[:10]
             .value_counts(normalize=True, dropna=False)
             .sort_index()))

print("The last_seen column is pretty similar to date_crawled, even starting and ending on the same days.")

print((autos.ad_created
             .str[:10]
             .value_counts(normalize=True, dropna=False)
             .sort_index()))

print("ad_created is a little bit different from the two before, since it has some older listings, going back as far as the 11th of june, 2015.")

print("Now, exploring the distribution of registration_year:")

print(autos.registration_year.describe())

print("From this result we can straight up tell that some entries are wrong, since the minimum year is 1000, and the maximum is 9999, which shows we need to clean up this column's data. Let's find out how many of our entries lie beyond 1900-2016:")

print((~autos["registration_year"].between(1900,2016)).sum() / autos.shape[0])

print("Since only 3.8% of our data lie beyond these boundaries, let's remove these outliers:")

autos = autos[autos["registration_year"].between(1900,2016)]

print(autos["registration_year"].value_counts(normalize=True))

print("From the percentage of each year, aquired above, it seems most cars were registere in the past 30 or so years.")

print("Exploring Brands")

print(autos.brand.value_counts())

print("We can see that the top 5 most popular car brands are german, which is kind of fitting since theses listings are from German eBay. Anyway, we will compare the average pricing from the top 5 brands to the bottom 5 brands:")

top_5_brands = ['volkswagen', 'bmw', 'opel', 'mercedes_benz', 'audi']

top_5_mean_prices = {}
for brand in top_5_brands:
    brand_only = autos[autos["brand"] == brand]
    mean_price = brand_only["price"].mean()
    top_5_mean_prices[brand] = int(mean_price)

print(top_5_mean_prices)

bottom_5_brands = ['lada', 'lancia', 'rover', 'trabant', 'daewoo']

bottom_5_mean_prices = {}
for brand in bottom_5_brands:
    brand_only = autos[autos["brand"] == brand]
    mean_price = brand_only["price"].mean()
    bottom_5_mean_prices[brand] = int(mean_price)

print(bottom_5_mean_prices)

print("Comparing the top brands and bottom brands we can infer that the consumer preference doesn't come from better pricing, since almost all top 5 brands (except OPEL) have higher average prices than the bottom 5. Therefore, the german market preference might come from product quality or other less objective reasons such as taste and culture.")

print("Exploring Mean Mileage from Brands")

top_5_mean_mileage = {}
for brand in top_5_brands:
    brand_only = autos[autos["brand"] == brand]
    mean_price = brand_only["odometer_km"].mean()
    top_5_mean_mileage[brand] = int(mean_price)

print(top_5_mean_mileage)

mean_mileage = pd.Series(top_5_mean_mileage).sort_values(ascending=False)
mean_prices = pd.Series(top_5_mean_prices).sort_values(ascending=False)

brand_info = pd.DataFrame(mean_mileage, columns=['mean_mileage'])
brand_info["mean_price"] = mean_prices
print(brand_info)

print("There doesn't seem to be any relation between average mileage and average car price from what we can gather in this table. Overall, the conclusion we could achieve is that BMWs, Mercedes and Audis are just more expensive cars.")