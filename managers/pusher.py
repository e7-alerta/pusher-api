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


def send(to, title, message=None, data:dict=[]):
    try:
        response = PushClient(session=session).publish(
            PushMessage(to=to,
                        title=title,
                        body=message,
                        data=data))
    except PushServerError as exc:
        print("Push server error: ",
              {
                  'token': to,
                  'title': title,
                  'message': message,
                  'data': data,
                  'errors': exc.errors,
                  'response_data': exc.response_data,
              })
        raise
    except (ConnectionError, HTTPError) as exc:
        print("Connection error: ",
              {'token': to, 'message': message, 'data': data}
              )
    print("message sended", response.id)
