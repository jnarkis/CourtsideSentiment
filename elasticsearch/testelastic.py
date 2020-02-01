from elasticsearch import Elasticsearch, RequestsHttpConnection
#from requests_aws4auth import AWS4Auth
#import boto3

#host = 'vpc-elastic-search-loxe2wn2q52ms5popas2vlvax4.us-west-2.es.amazonaws.com'
host = 'vpc-elastic-search-loxe2wn2q52ms5popas2vlvax4.us-west-2.es.amazonaws.com'
region = 'us-west-2'

service = 'es'
#credentials = boto3.Session().get_credentials()

es = Elasticsearch(hosts = [{'host' : host, 'port' : 443}], use_ssl = True, verify_certs = False)
print("a")
document = {
     "title" : "Moneyball",
     "director" : "Bennett Miller",
     "year" : "2011"
}
print("b")
es.index(index="movies",doc_type="_doc",id="5",body=document)
print("c")

res = es.search(index="movies", doc_type="_doc", body={"query" : {"match"  : {"director" : "Bennett Miller"}}})

print(res)
#print("%d documents found" % res['hits']['total'])
