import urllib2, Queue, threading, os

target= "http://josephus.hsutx.edu/"
directory = "C:\Users\\asdf\PycharmProjects\BlackHat\Chapter5\extract_web_app"
# directory = "/Users/root/Downloads/joomla-3.1.1" # linux
filters = [".jpg",".gif","png",".css"]
threads = 10

os.chdir(directory)
#This will store the files that I am attempting to locate on remote serv
web_paths = Queue.Queue()

for r, d, f in os.walk("."):
    for files in f:
        remote_path = "%s%s" % (r, files)
        if remote_path.startswith("."):
            remote_path = remote_path[1:]
        # this will prevent any file types listed in filters from being picked up
        if os.path.splitext(files)[1] not in filters:
            web_paths.put(remote_path)

def test_remote():
    while not web_paths.empty():
        path = web_paths.get()
        url = "%s%s" % (target, path)

        request = urllib2.put(remote_path)

        try:
            response = urllib2.urlopen(request)
            content = response.read()
            print "[%d] --> %s" % (response.code, path)
            response.close()
        except urllib2.HTTPError as error:
            print "Failed %s" % error.code
            pass
for i in range(threads):
    print "Initiating thread #%d" % i
    t = threading.Thread(target = test.remote)
    t.start()


# headers = {}
# headers['User-Agent'] = "Googlebot"
#
# request = urllib2.Request(url, headers = headers)
# response = urllib2.urlopen(request)
#
# f = open("josephus.txt", "w")
# content = response.read()
# f.write(content)
# f.close()
#
# # print response.read()
# # response.close()
#
