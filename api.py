
import json
import uuid
import urllib
import urllib2

def search(name):
    id = str(uuid.uuid4())
    url =  'https://preview.academic.microsoft.com/api/search/GetEntityResults?correlationId=' + id 
    
    query = {'Query':'@' + name +  '@'}
    headers = { 'User-Agent' : 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.96 Safari/537.36',
                'Accept':'*/*',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8' ,
                'Origin': 'https://preview.academic.microsoft.com',
                'Referer' : 'https://preview.academic.microsoft.com/',
                'Accept':'application/json',
    }
    form = urllib.urlencode(query) + '&Limit=1&Offset=0&OrderBy=&SortAscending=false' 
    request = urllib2.Request(url, form, headers)
    results = urllib2.urlopen(request)
#     resp = requests.post(url, data=payload, headers=headers)
    
#     pretty_print_POST(resp.request)
    data = json.loads(results.read())
    file1 = open(name + "reponse1.json","w") 
    file1.write(json.dumps(data, indent=4, sort_keys=False)) 
    file1.close() 
    
    article = data['entitiesInQuery'][0]
    
    filterAuthors = []
    for autor in article['entity']['aa']:
        filterAuthors.append('Composite(AA.AuId%3D' + str(autor['auId']) + ')%2C')
    
    filterAuthors = '&Filters=' + ''.join(filterAuthors).rsplit('%2C', 1)[0]
    
    form2 = urllib.urlencode(query)  + filterAuthors +'&Limit=1&Offset=0&OrderBy=&SortAscending=false'
    request = urllib2.Request(url, form2, headers)
    results = urllib2.urlopen(request)
    
    data = json.loads(results.read())
    
    file3 = open(name + "reponse2.json","w") 
    file3.write(json.dumps(data, indent=4, sort_keys=False)) 
    file3.close() 
    
def main():
    search('Accuracy and Diversity in Cross-domain Recommendations for Cold-start Users with Positive-only Feedback')
    
def pretty_print_POST(req):
    """
    At this point it is completely built and ready
    to be fired; it is "prepared".

    However pay attention at the formatting used in 
    this function because it is programmed to be pretty 
    printed and may differ from the actual request.
    """
    print('{}\n{}\n{}\n\n{}'.format(
        '-----------START-----------',
        req.method + ' ' + req.url,
        '\n'.join('{}: {}'.format(k, v) for k, v in req.headers.items()),
        req.body,
    ))
    
if __name__ == '__main__':
    main()

