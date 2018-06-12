import urllib2, threading, Queue, urllib

threads= 50
target_url = "http://josephus.hsutx.edu"
wordlist_file = "/tmp/all.txt" #SVNDigger
resume = None
user_agent = "Mozilla/5.0 (X11; Linux x86_64; rv:19.0) Gecko/20100101 Firefox/19.0"

def build_wordlist(wordlist_file):
    #read word list
    fd = open(wordlist_file, "rb")
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
                    print "Resuming wordlist @ %s" % resume
        else:
            words.put(word)
    return words
