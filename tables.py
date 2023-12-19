# Overlord library
from core.library import models, uuid, JsonResponse, api, console


class TestModel(models.Model):
  """
  This is a test model used to demonstrate Overlord's Universal API
  and should not be deployed to production

  It contains two columns within it's database table `uuid` & `data` which
  demonstrates how you can create a unique uuid field for your models

  Also contains a single function which allows you add a new row with
  a unique `uuid` and return a success response upon completion
  """
  uuid = models.CharField(
    null=False,
    blank=False,
    unique=True,
    default=uuid,
    max_length=36,
    primary_key=True
  )
  data = models.TextField(
    null=False,
    blank=False,
    default="no data provided"
  )

  @staticmethod
  def add_test_data(req, *args, **kwargs) -> JsonResponse:
    """
    This function adds a row to your database table with a piece of `data`
    which also has a universal unique identifier (uuid) attached to it

    If the row is created successfully the api will respond with "success response"
    If the row fails to be created the api will respond with an "error response"

    An error response via the `api.error` function will only provide insightful
    data if the server is running in DEBUG mode, otherwise the message will read
    "[ERROR] 500 Internal Server" so that users do not get in-sight into your
    production server
    """
    try:
      # Get the test data from the request body
      test_data = api.get_body(req)
      # Print the received test_data to console
      console.out(f"\n> Received Test Data\n\n{test_data}\n")
      # Create the test data in a db table row
      TestModel.objects.update_or_create(data=test_data)
      # Return a success response
      return api.success()
    except Exception as db_error:
      # Return an error response
      return api.error(db_error)
