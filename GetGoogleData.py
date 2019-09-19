import json
import csv
import requests
import time
import googlemaps
import tqdm
from googlemaps.places import places_nearby, places_photo,place
import numpy as np
#%%
key = "" # use your api key, this one won't work with your IP adress

# Google Maps let you access no more than 60 places for each locations. For that reason, we created several locations for multiple requests
locations = [(48.860412, 2.273805), (48.863108, 2.278405),(48.852890, 2.271134),(48.847752, 2.266433),(48.849187, 2.285682),(48.844742, 2.284094),(48.849360, 2.297999),(48.845338, 2.295563),(48.841096, 2.287845),(48.855090, 2.295894),(48.841326, 2.303095),(48.838254, 2.297818),(48.868476, 2.281494),(48.866955, 2.290874),(48.836566, 2.309866),(48.832795, 2.314104),(48.872280, 2.291487),(48.875978, 2.296515),(48.880482, 2.285067),(48.861440, 2.340431),(48.862485, 2.349881),(48.857689, 2.353121),(48.846942, 2.320690),(48.888593, 2.347121),
            (48.853955, 2.373156),(48.855454, 2.375565),(48.849980, 2.378446), (48.867384, 2.396311), (48.870886, 2.370956), (48.874283, 2.330231), (48.869459, 2.328237), (48.872695, 2.346639), (48.880515, 2.363387), (48.847151, 2.348434), (48.839094, 2.350213), (48.830306, 2.355056), (48.852048, 2.334497), (48.838222, 2.391196), (48.891092, 2.376889), (48.832649, 2.330879), (48.858770, 2.308328), (48.864215, 2.344288), (48.823762, 2.364280), (48.863164, 2.323516),(48.855017, 2.314881),(48.843600, 2.333395),(48.826586, 2.343842), 
            (48.840603, 2.324190), (48.835732, 2.370996), (48.870728, 2.307577), (48.877233, 2.313560), (48.884304, 2.322581), (48.883944, 2.338889), (48.894526, 2.340568), (48.882779, 2.360990), (48.864474, 2.371611), (48.848149, 2.397560), (48.858062, 2.400685), (48.855272, 2.321172), (48.847715, 2.310843), (48.868992, 2.357088), (48.877239, 2.357761), (48.860665, 2.362914), (48.859461, 2.387545), (48.865818, 2.301712), (48.844070, 2.364224), (48.832640, 2.300779), (48.828490, 2.321405), (48.891854, 2.361054), (48.879971, 2.378422),
            (48.876915, 2.392314)]
gmaps = googlemaps.Client(key=key)
cols  = ["lat","lng", "name", "photo_ref","rating", "user_rating_total", "vicinity", "place_id","types"]


with open('restau.csv','w') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    writer.writerow(cols)

with open('restau.csv','a') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    j=1
    for loc in locations:
        print("location number: {}".format(j))
        j+=1
        i=1
        response  = places_nearby(gmaps, location = loc, radius = 500, max_price=3, type = "restaurant")
        for obj in response['results']:
            photo  = obj["photos"][0]["photo_reference"] if ("photos" in obj) else np.float("nan")
            rating = obj["rating"] if ("rating" in obj) else np.float("nan")
            user_ratings_total = obj["user_ratings_total"] if ("user_ratings_total" in obj) else np.float("nan")
            writer.writerow([obj['geometry']['location']['lat'],obj['geometry']['location']['lng'], obj["name"], photo, rating, user_ratings_total, obj["vicinity"], obj["place_id"], obj["types"]])
        print("page number {}".format(i))
        while 'next_page_token' in response:
            i+=1
            page_token = response['next_page_token']
            time.sleep(5)
            response = places_nearby(gmaps, location = loc, radius = 500, type = "restaurant", max_price=3, page_token= page_token)
            for obj in response['results']:
                photo  = obj["photos"][0]["photo_reference"] if ("photos" in obj) else np.float("nan")
                rating = obj["rating"] if ("rating" in obj) else np.float("nan")
                user_ratings_total = obj["user_ratings_total"] if ("user_ratings_total" in obj) else np.float("nan")
                writer.writerow([obj['geometry']['location']['lat'],obj['geometry']['location']['lng'], obj["name"], photo, rating, user_ratings_total, obj["vicinity"], obj["place_id"], obj["types"]])
            print("page number {}".format(i))

photo = places_photo(gmaps, "CmRaAAAAj1V6ntNUDJ72Jtw_AoPrUKQTjzo9G51MpsbsZa8cVdSwQFE4EXXXLO7tOgV0cipgsmS4XEUUJIVmLInnIhhOLrvLXHShqde8jV68NYIFmgPO_S-pwWM39jQGkWnIRIbAEhCttHIKc125_NwpOkMS8K-wGhQwUJb43Td9tWpMAeMCI8R-TV_3OQ", max_width=300)
f = open("img.png", 'wb')
for chunk in photo:
    if chunk:
        f.write(chunk)
f.close()


place_results = place(gmaps, 'ChIJqzBe2EVu5kcRvU67ufRGCTU')