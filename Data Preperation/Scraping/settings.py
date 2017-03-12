headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36"}

## Uses proxybonanaz.com shared proxies service to gather proxies that will be used to scrape amazon.com and goodreads.com
def proxy_paid():
    f = open('proxylist.csv','r')
    text = f.readlines()
    freshproxlist = []
    username = ''
    password = ''
    for line in text:
        prox ={
            'http':'http://{}:{}@{}:{}/'.format(username,password,line.strip(),60099),
            'https':'https://{}:{}@{}:{}/'.format(username,password,line.strip(),60099)
            }
        freshproxlist.append( prox )
    f.close()
    return freshproxlist
