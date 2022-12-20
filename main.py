import datetime
import flask
from google.oauth2 import service_account

credentials = service_account.Credentials.from_service_account_file('cts01-psenapati-2e6bb52d5e77.json')

from google.cloud import storage
app = flask.Flask(__name__)
default_bucket_name = 'cts01-psenapati'

def generate_signed_post_policy_v4(bucket_name, blob_name):
    """Generates a v4 POST Policy and prints an HTML form."""
    # bucket_name = 'your-bucket-name'
    # blob_name = 'your-object-name'

    storage_client = storage.Client()

    policy = storage_client.generate_signed_post_policy_v4(
        bucket_name,
        blob_name,
        expiration=datetime.timedelta(minutes=10),
        fields={
          'x-goog-meta-test': 'data'
        },
        credentials=credentials
    )

    print(policy)
    # Create an HTML form with the provided policy
    header = "<form action='{}' method='POST' enctype='multipart/form-data'>\n"
    form = header.format(policy["url"])

    # Include all fields returned in the HTML form as they're required
    for key, value in policy["fields"].items():
        form += f"  <input name='{key}' value='{value}' type='hidden'/>\n"

    form += "  <input type='file' name='file'/><br />\n"
    form += "  <input type='submit' value='Upload File' /><br />\n"
    form += "</form>"

    print(form)

    return form

@app.route('/')
def hello():

    response = "<html><body>\n"
    response += "<h1>Test file upload:</h1>\n"
    response += "<p>Please allow each upload to complete before proceeding to the next step.</p>"
    response += generate_signed_post_policy_v4(default_bucket_name, "file1")
    return response

if __name__ == "__main__":
    # Used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host="0.0.0.0", port=8080, debug=True)