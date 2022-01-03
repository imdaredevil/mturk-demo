import base64
import requests


url = input()
response = requests.get(url)
content_type = response.headers["content-type"]
encoded_body = base64.b64encode(response.content)
print("data:{};base64,{}".format(content_type, encoded_body.decode()))