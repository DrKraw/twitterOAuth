import constants
import oauth2
import urlparse
# Create a consumer, which uses CONSUMER_KEY and CONSUMER_SECRET to identify app uniquely
consumer = oauth2.Consumer(constants.CONSUMER_KEY, constants.CONSUMER_SECRET)
client = oauth2.Client(consumer)

# Use the client to perform a request for the request token
response, content = client.request(constants.REQUEST_TOKEN_URL, 'POST')
if response.status != 200:
    print("An Error occurred getting the request token from Twitter!")
# Get the request token parsing the query string returned
request_token = dict(urlparse.parse_qsl(content.decode('utf-8')))

# Ask the user to authorize our app and give us the pin code
print(" Go to the following site in your browser: ")
print("{}?oauth_token={}".format(constants.AUTHORIZATION_URL, request_token['oauth_token']))

oauth_verifier = input("What is the PIN? ")

# Create a token object which contains the request token, and the verifier
token = oauth2.Token(request_token['oauth_token'], request_token['oauth_token_secret'])
token.set_verifier(oauth_verifier)
client = oauth2.Client(consumer, token)
# Ask twitter for an access token, and twitter knows it should give us it
# because weve verified the request token
response, content = client.request(constants.ACCESS_TOKEN_URL, 'POST')
access_token = dict(urlparse.parse_qsl(content.decode('utf-8')))

print(access_token)
# Create an 'authorized_token' Token object and use that to perform Twitter API Calls on behalf of the user
authorized_token = oauth2.Token(access_token['oauth_token'], access_token['oauth_token_secret'])
authorized_client = oauth2.client(consumer, authorized_token)
# Make Twitter API calls!!
response, client = authorized_client.request('https://api.twitter.com/1.1/search/tweets.json')
