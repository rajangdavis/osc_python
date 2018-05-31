# OSvCPython

[![Maintainability](https://api.codeclimate.com/v1/badges/7be0820423b00dade9c8/maintainability)](https://codeclimate.com/github/rajangdavis/osvc_python/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/7be0820423b00dade9c8/test_coverage)](https://codeclimate.com/github/rajangdavis/osvc_python/test_coverage)
[![Build Status](https://travis-ci.org/rajangdavis/osvc_python.svg?branch=master)](https://travis-ci.org/rajangdavis/osvc_python)
[![PyPI version](https://badge.fury.io/py/osvc-python.svg)](https://badge.fury.io/py/osvc-python)
[![Known Vulnerabilities](https://snyk.io/test/github/rajangdavis/osvc_python/badge.svg)](https://snyk.io/test/github/rajangdavis/osvc_python)
[![FOSSA Status](https://app.fossa.io/api/projects/git%2Bgithub.com%2Frajangdavis%2Fosvc_python.svg?type=shield)](https://app.fossa.io/projects/git%2Bgithub.com%2Frajangdavis%2Fosvc_python?ref=badge_shield)

An (under development) Python library for using the [Oracle Service Cloud REST API](https://docs.oracle.com/cloud/latest/servicecs_gs/CXSVC/) influenced by the [ConnectPHP API](http://documentation.custhelp.com/euf/assets/devdocs/november2016/Connect_PHP/Default.htm)

## Todo
I am looking to implement the following items soon:
1. OSvCPythonQueryResultsSet, an object for performing multiple queries
2. OSvCPythonAnalyticsReportResults, an object for running Analytics Reports
3. Test suite (in progress)
4. Documentation
  

## Compatibility

The library is being tested against Oracle Service Cloud May 2017 using Python 2.7.13.

TravisCI to be set up soon!

All of the HTTP methods should work on any version of Oracle Service Cloud since version May 2015; however, there maybe some issues with querying items on any version before May 2016. This is because ROQL queries were not exposed via the REST API until May 2016.


## Use Cases
You can use this Python Library for basic scripting and microservices. The main features that work to date are as follows:

1. [Simple configuration](#client-configuration)
2. [Running ROQL queries](oscpythonqueryresults-example)
3. Convenience methods for Analytics filters and setting dates
	1. ['dti', converts a date string to ISO8601 format](#dti--date-to-iso8601)
4. Basic CRUD Operations via HTTP Methods
	1. [Create => Post](#create)
	2. [Read => Get](#read)
	3. [Update => Patch](#update)
	4. [Destroy => Delete](#delete)

## Installing Python (for Windows)
[Try this link.](https://github.com/BurntSushi/nfldb/wiki/Python-&-pip-Windows-installation)
The link covers how to:
1. Install Python
2. Add Python to your PATH (expose it to the command line)
3. How to install pip, a Python package manager

## Installation

Install with pip:

    $ pip install osvc-python


## Client Configuration

An OSvCPythonClient class lets the library know which credentials and interface to use for interacting with the Oracle Service Cloud REST API.
This is helpful if you need to interact with multiple interfaces or set different headers for different objects.

```python

# Configuration is as simple as importing the package
# and entering in credentials

from 'osvc_python' import OSvCPythonClient

# Configuration Client
self.rn_client = OSvCPythonClient(
		username=env('OSC_ADMIN'),
		password=env('OSC_PASSWORD'),
		interface=env('OSC_SITE')
	)

# Optional Configuration Settings
# rn_client.change_version('v1.4') 		#=> Changes REST API version, default is 'v1.3'
# rn_client.ssl_off()				#=> Turns off SSL verification
# rn_client.suppress_rules()			#=> Supresses Business Rules
rn_client.is_demo() 				#=> Changes 'custhelp' domain to 'rightnowdemo'
```





## OSvCPythonQueryResults example

This is for running one ROQL query. Whatever is allowed by the REST API (limits and sorting) is allowed with this library.

OSvCPythonQueryResults only has one function: 'query', which takes an OSvCPythonClient object and string query (example below).

```python
from 'osvc_python' import OSvCPythonClient,OSvCPythonQueryResults

rn_client = OSvCPythonClient(env('OSC_ADMIN'),
			    env('OSC_PASSWORD'),
    			    env('OSC_SITE'))

q = OSvCPythonQueryResults(rn_client)
query = "DESCRIBE Answers"
results = q.query(query)

print results.status_code 			#=> 200
print results.content 				#=> JSON representation of results
print results.pretty_content	 		#=> Pretty printed JSON String of results


```


### 'dti' => date to iso8601

dti lets you type in a date and get it in ISO8601 format. Explicit date formatting is best.

```python

dti("January 1st, 2014") # => 2014-01-01T00:00:00-08:00  # => 1200 AM, January First of 2014

dti("January 1st, 2014 11:59PM MDT") # => 2014-01-01T23:59:00-06:00 # => 11:59 PM Mountain Time, January First of 2014

dti("January 1st, 2014 23:59 PDT") # => 2014-01-01T23:59:00-07:00 # => 11:59 PM Pacific Time, January First of 2014

dti("January 1st") # => 2017-01-01T00:00:00-08:00 # => 12:00 AM, January First of this Year

```


## Basic CRUD operations

### CREATE
```python
#### OSvCPythonConnect.post( <client>, <url>, <json_data> )
#### returns a OSvCPythonResponse object

# Here's how you could create a new ServiceProduct object
# using Python variables, hashes(sort of like JSON), and arrays to set field information

from osvc_python import env,OSvCPythonClient, OSvCPythonConnect

rn_client = OSvCPythonClient(env('OSC_ADMIN'),
			    env('OSC_PASSWORD'),
			    env('OSC_SITE'))

opc = OSvCPythonConnect(rn_client)

new_product = {}
new_product['names'] = []
new_product['names'].append({'labelText':'NEW_PRODUCT', 'language':{'id':1}})
new_product['displayOrder'] = 4

new_product['adminVisibleInterfaces'] = []
new_product['adminVisibleInterfaces'].append({'id':1})
new_product['endUserVisibleInterfaces'] = []
new_product['endUserVisibleInterfaces'].append({'id':1})

res = opc.post('serviceProducts',new_product)

print res.status_code # => 201
print res.content # => JSON body
# callback with JSON details

```







### READ
```python
#### OSvCPythonConnect.get( <client>, optional (<url>/<id>/...<params>) )
#### returns a OSvCPythonResponse object
# Here's how you could get an instance of ServiceProducts

from osvc_python import env,OSvCPythonClient, OSvCPythonConnect

rn_client = OSvCPythonClient(env('OSC_ADMIN'),
			    env('OSC_PASSWORD'),
			    env('OSC_SITE'))

opc = OSvCPythonConnect(rn_client)
res = opc.get('serviceProducts/164')

print res.status_code # => 200
print res.pretty_content # => Pretty Printed JSON response
# {
#     "links": [
#         {
#             "href": "https://{env('OSC_SITE')}.rightnowdemo.com/services/rest/connect/v1.3/serviceProducts/164", 
#             "rel": "self"
#         }, 
#         {
#             "href": "https://{env('OSC_SITE')}.rightnowdemo.com/services/rest/connect/v1.3/serviceProducts/164", 
#             "rel": "canonical"
#         }, 
#         {
#             "href": "https://{env('OSC_SITE')}.rightnowdemo.com/services/rest/connect/v1.3/metadata-catalog/serviceProducts", 
#             "mediaType": "application/schema+json", 
#             "rel": "describedby"
#         }
#     ], 
# ...
# }
```






### UPDATE
```python
#### OSvCPythonConnect.patch(<url>, <json_data> )
#### returns a OSvCPythonResponse object
# Here's how you could update an Answer object
# using Python variables, lists, and dicts
# to set field information
from osvc_python import env,OSvCPythonClient, OSvCPythonConnect

rn_client = OSvCPythonClient(env('OSC_ADMIN'),
			    env('OSC_PASSWORD'),
			    env('OSC_SITE'))
			    
opc = OSvCPythonConnect(rn_client)

# Patch example
answer_updated_hash = {}
answer_updated_hash['summary'] = "Python TEST UPDATED"
answer_updated_hash['solution'] = "PYTHON TEST UPDATED"
updated_answer = opc.patch('answers/154',answer_updated_hash)
print updated_answer.status_code
print updated_answer.content #=> Returns as JSON

```






### DELETE
```python
#### OSvCPythonConnect.delete(<url> )
#### returns a OSvCPythonResponse object
# Here's how you could delete an Answer object
# and OSvCPythonConnect classes

from osvc_python import env,OSvCPythonClient, OSvCPythonConnect

rn_client = OSvCPythonClient(env('OSC_ADMIN'),
			    env('OSC_PASSWORD'),
			    env('OSC_SITE'))

opc = OSvCPythonConnect(rn_client)
deleted_answer = opc.delete('answers/154')
print deleted_answer.status_code #=> 200

```


## License
[![FOSSA Status](https://app.fossa.io/api/projects/git%2Bgithub.com%2Frajangdavis%2Fosvc_python.svg?type=large)](https://app.fossa.io/projects/git%2Bgithub.com%2Frajangdavis%2Fosvc_python?ref=badge_large)