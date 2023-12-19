# Universal API
from . import API
from .tables import TestModel

# Test Endpoint
API.path(
  "test",                                       # Endpoint name         [required]
  TestModel.add_test_data,                      # Endpoint function     [required]
  "Tests the database and response mechanism"   # Endpoint description  [optional]
)
