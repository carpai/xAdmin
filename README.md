# xAdmin Project

## Project Requirements
install only the pymongo==2.8.1, DO NOT TRY TO USE pymongo 3.x

we use mongokit as we use mongodb, and for python3, mongokit support has a bug:
you need to install mongokit first, and then install mongokit-py3.



## Project prepare

before running app server, you need to use setup.py to install xAdmin as a site-package. otherwize, 
you will get a `xAdmin distribution not found` error.

Just type:

```shell
  $ YOURPY3 setup.py develop
```
  
  
## Tips
 
### mongokit Document type

```
- None # Untyped field
- bool 
- int 
- float
- long
- (bytes)
- str
- list
- dict
- datetime.datetime
- bson.binary.Binary
- pymongo.objectid.ObjectId
- bson.dbref.DBRef
- bson.code.Code
- type(re.compile(""))
- uuid.UUID
- CustomType
```
