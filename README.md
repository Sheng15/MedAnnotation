# Welcome to MedAnnotation

MedAnnotation leverages the authentication API provided by CouchDB to protect data and provides services including storing clinical trials, fetching files and query for data. Query features include keyword search, semantic search, prediction search and a hybrid of semantic and predication search.


# Enviroment setup

Require python with 3.5 or higher,
Couchdb with 2.0 or higher.

## Python modules setup
```
pip install mmh3
pip install couchdb ( "https://couchdb-python.readthedocs.io/en/latest/" for more detials)
pip install treelib  ("https://treelib.readthedocs.io/en/latest/pyapi.html" for more detials)
```

## CouchDB setup

For windows and macOS user, installation from binaries is recommended.
After installation, visit http://127.0.0.1:5984/_utils#setup for first time setup.
** choose single node
** set admin of the database
** bind a private or public ip address to couchdb


For Ubuntu(16.4.0) user,just run

```
$ sudo yum -y install epel-release && yum install couchdb
$ curl -L https://couchdb.apache.org/repo/bintray-pubkey.asc \
    | sudo apt-key add –
$ echo "deb https://apache.bintray.com/couchdb-deb {distribution} main" \
    | sudo tee -a /etc/apt/sources.list
$ sudo apt-get update && sudo apt-get install couchdb
```

First time setup will be finished during installation

# How to use

Import all the python file and invoke the method for usage.
```
$import couchdbProcesser
$import dbQuery
$import fikeProcesser
$import meshTree
```

## Examples

Let's assume couch is bind at localhost at default port 5984,
Using (admin:password) and query "demo" database     


### Connection
Pass authentication credentials and/or use SSL to create a  server object with all the authority the user has 
```
$ server = couchdbProcesser.authConnection("localhost:5984","admin","password"):
```
### Set authentication
Set the admins and members of a database
```
$ couchdbProcesser.setPermission(server,"demo",["admin1","admin2"],["member1","member2"])
```
**NOTICE** : However, this method will just set the permissions according to the given list,
without any check that whether the given user is exist , this method will over write any former set!

###  Create a user
the database and its permission will be set at the same time
```
$ couchdbProcesser.addUser("localhost:5984","admin","password","newUser","newPassword")
```
### Fetch files
find all the annotations made  to a particular clinical trial 
```
$ couchdbProcesser.get_annotation_all(server,"demo","example.txt")
```
###  Save files
```
$ fileProcesser.save_annotated_text(server,"newUser","demo","example.txt","example.ann")
```
**NOTICE** :  there should be another database "demosearch" exist to store index documents, 
	                     a statistic document of the docs count and words count should be initialized

### Save all files of a folder to database
```
$ fileProcesser.save(server,"newUser","folder_path","demo")
```

### Load meshTree
meshTree is a tree object, use meshTree.show() to print the detial of the tree
```
$ meshTree,meshDic = meshTree.loadMeshTree()
```
# How to query
## Keyword search
```
$ result = dbQuery.keywordSearch(server,"blood","demosearch")
```
a list of the ids of all docs found,
"Blood" ,"blood" or other cases such "BlOoD" just return the same result

to search catagory,for example, whether a clinical trial contains the patient's name?
run this:
```
$ result = dbQuery.keywordSearch(server,"[patientName]","demosearch")
```
of course patient's name should be annoated 

set preference?
run this
```
$ docs = keywordSearch(server,"blood","demosearch",time = true,limit = 500, TFIDF = true)
```
TFIDF only implement for keyword search

## Senmatic search
Quite similar to examples above， except no TFIDF supported
```
$ result = dbQuery.semanticSearch(server,"[disease]","demosearch")
```
this just find all doc that contains tokens that catagory of which is in the subtree of "disease"


## PredicateSearch
```
$ result = dbQuery.predicateSearch(server,"blood","cause","demosearch")
```
a term here can both be the subject or object

## SemanticPredicateSearch
Nothing new there. Both suject and object can be expended.
Cannot expend predicate now, but is there a hierarchy for predicate？
```
$ result1 = dbQuery.semanticPredicateSearch(server,"blood","cause","disease","demosearch")
$ result2 = dbQuery.semanticPredicateSearch(server,"blood","cause","[disease]","demosearch")
$ result3 = dbQuery.semanticPredicateSearch(server,"[chemocals]","cause","[disease]","demosearch")
```
# TODO List
1. Normalising of entities and concepts
2. Implementation of catagory of entities and concepts
3. Building index of each particular entity and concept.
