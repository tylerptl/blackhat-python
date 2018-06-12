import urllib2

url = "http://www.nostarch.com"

headers = {}
headers['User-Agent'] = "Googlebot"

request = urllib2.Request(url, headers = headers)
response = urllib2.urlopen(request)

f = open("nostarch.txt", "w")
content = response.read()
f.write(content)
f.close()

# print response.read()
# response.close()

