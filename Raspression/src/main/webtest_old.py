import urllib
import urllib2
import web

def testCall():
    url = "http://192.168.0.74:8001/lightboard/colour"
    value = { "red" : url }

    data = urllib.urlencode(value)
    req = urllib2.Request(url, data)
    response = urllib2.urlopen(req)
    the_page = response.read()

    print the_page

urls = {
    '/', 'test'
}


class test:
    def GET(self):
        output = "fuck right off"
        return output

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()

