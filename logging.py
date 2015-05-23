import cookielib
import urllib
import urllib2


# Store the cookies and create an opener that will hold them
cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))

# Add our headers
opener.addheaders = [('User-agent', 'John Paul The Second')]

# Install our opener (note that this changes the global opener to the one
# we just made, but you can also just call opener.open() if you want)
urllib2.install_opener(opener)

# The action/ target from the form
authentication_url = 'http://bidthebag.app.inf.re/accounts/login/'
#GET CSRF TOKEN HERE XD
# Input parameters we are going to send
payload = {
  'csrfmiddlewaretoken': 'tayXfmX8ENm0cswGRMx3g2UINIc5AgC4',
  'id_username': 'kacpertest',
  'id_password': 'kacperrest'
  }

# Use urllib to encode the payload
data = urllib.urlencode(payload)

# Build our Request object (supplying 'data' makes it a POST)
req = urllib2.Request(authentication_url, data)

# Make the request and read the response
resp = urllib2.urlopen(req)
contents = resp.read()
print(contents)
