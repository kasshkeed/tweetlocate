import requests
import pandas as pd

# Twitter API v2 credentials
BEARER_TOKEN = 'AAAAAAAAAAAAAAAAAAAAALKZugEAAAAA5X0G0S8E1Vf65CesJ2D6Bqn5nkc%3D8lgocZ2OJUwBNfP4nCY8imxmPDLs0pIvCZmIzn4SM57oopdZcL'

# Function to create the headers for the request
def create_headers(bearer_token):
    headers = {
        "Authorization": f"Bearer {bearer_token}",
        "User-Agent": "v2TweetLookupPython"
    }
    return headers

# Function to get tweets within a radius using Twitter API v2
def get_tweets_within_radius_v2(lat, lon, radius=1):
    url = "https://api.twitter.com/2/tweets/search/recent"
    query_params = {
        'query': f'point_radius:[{lon} {lat} {radius}km]',
        'tweet.fields': 'author_id,text,geo',
        'max_results': 100
    }
    headers = create_headers(BEARER_TOKEN)
    response = requests.get(url, headers=headers, params=query_params)
    if response.status_code != 200:
        raise Exception(f"Request returned an error: {response.status_code} {response.text}")
    
    tweets_data = []
    for tweet in response.json().get('data', []):
        tweets_data.append({
            'username': tweet['author_id'],  # Note: Twitter API v2 does not directly provide usernames
            'tweet': tweet['text'],
            'location': f"point_radius:[{lon} {lat} {radius}km]"  # Placeholder, actual geo info requires another API call
        })
    
    return pd.DataFrame(tweets_data)

# Function to find the user with the most tweets
def find_user_with_most_tweets(tweets_df):
    user_counts = tweets_df['username'].value_counts()
    if user_counts.empty:
        return None, None
    top_user = user_counts.idxmax()
    top_user_tweets = tweets_df[tweets_df['username'] == top_user]
    return top_user, top_user_tweets

# Define the center of the search area
center_lat = 40.7128  # Example latitude (New York City)
center_lon = -74.0060  # Example longitude (New York City)
radius = 1  # Define the radius in kilometers (API v2 uses kilometers)

try:
    # Get tweets within the radius
    print(f"Fetching tweets within {radius}km of ({center_lat}, {center_lon})")
    tweets_df = get_tweets_within_radius_v2(center_lat, center_lon, radius)

    if not tweets_df.empty:
        # Find the user with the most tweets
        top_user, top_user_tweets = find_user_with_most_tweets(tweets_df)
        if top_user:
            print(f"User with the most tweets: {top_user}")
            print("\nTweets:\n")
            for index, row in top_user_tweets.iterrows():
                print(f"Username: {row['username']}")
                print(f"Tweet: {row['tweet']}")
                print(f"Location: {row['location']}")
                print("-" * 40)
        else:
            print("No users with tweets found within the specified range.")
    else:
        print("No tweets found within the specified range.")
except Exception as e:
    print(f"An error occurred: {e}")
