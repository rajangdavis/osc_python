import os
from datetime import datetime
from dateutil import parser
from .osvc_python_client import OSvCPythonClient
from .osvc_python_connect import OSvCPythonConnect
from .osvc_python_query_results import OSvCPythonQueryResults

def env(var):
	return os.environ[var]

def dti(date_string):
	try:
		return parser.parse(date_string).isoformat()
	except Exception as e:
		raise e.message()

def arrf(**kwargs):
	filter_attrs = ['attributes',
					'dataType',
					'name',
					'operator',
					'prompt',
					'values']
	filter_hash = {}
	for attrs in filter_attrs:
		if attrs in kwargs:
			filter_hash[attrs] = kwargs[attrs]
	return filter_hash

__all__ = ['env','dti','arrf','OSvCPythonConnect','OSvCPythonClient','OSvCPythonQueryResults']