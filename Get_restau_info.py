import pandas as pd
import googlemaps
from googlemaps.places import places_nearby, places_photo,place
import numpy as np

restaurants = pd.read_csv("restau.csv")
#Get the most reccurent types of restaurants
type_counts = restaurants.types.value_counts()
most_known_types = list(type_counts[type_counts>=10].index)

# Keep restaurants with recurrent types
restaurants = restaurants[restaurants.types.isin(most_known_types)]
# Keep the best restaurants
restaurants = restaurants[(restaurants.rating>3.5) & (restaurants.user_rating_total>10)]
key = ""
gmaps = googlemaps.Client(key=key)

additional_info = pd.DataFrame(columns=['place_id','international_phone_number', 'weekday_opening_hours', 'reviews', 'website'])


for place_id in restaurants.place_id:
    response  = place(gmaps, place_id, language="fr", fields=["review","international_phone_number", "opening_hours", "website"])
    results = response["result"]
    website = results["website"] if ("website" in results) else np.float("nan") 
    international_phone_number = results["international_phone_number"] if ("international_phone_number" in results) else np.float("nan")
    weekday_opening_hours = results["opening_hours"]["weekday_text"] if ("opening_hours" in results) else np.float("nan")
    if "reviews" in results:
        reviews = [(element["rating"], element["text"]) for element in results["reviews"]]
    else:
        reviews = np.float("nan")
    additional_info = additional_info.append({"place_id": place_id, "international_phone_number": international_phone_number,
                                              "weekday_opening_hours": weekday_opening_hours, "reviews": reviews, "website": website}, ignore_index=True)

additional_info.to_csv("additional_info.csv")
         

len(response["result"]["reviews"])