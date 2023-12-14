from exponent_server_sdk import (
    DeviceNotRegisteredError,
    PushClient,
    PushMessage,
    PushServerError,
    PushTicketError,
)
import requests
from requests.exceptions import ConnectionError, HTTPError

session = requests.Session()
session.headers.update(
    {
        "accept": "application/json",
        "accept-encoding": "gzip, deflate",
        "content-type": "application/json",
    }
)


def send(token, title, message=None, extra=None):
    try:
        response = PushClient(session=session).publish(
            PushMessage(to=token,
                        title=title,
                        body=message,
                        data=extra))
    except PushServerError as exc:
        print("Push server error: ",
              {
                  'token': token,
                  'title': title,
                  'message': message,
                  'extra': extra,
                  'errors': exc.errors,
                  'response_data': exc.response_data,
              })
        raise
    except (ConnectionError, HTTPError) as exc:
        print("Connection error: ",
              {'token': token, 'message': message, 'extra': extra}
              )
    print("message sended", response.id)
