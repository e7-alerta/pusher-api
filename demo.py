from exponent_server_sdk import (
    DeviceNotRegisteredError,
    PushClient,
    PushMessage,
    PushServerError,
    PushTicketError,
)
import os
import requests
from requests.exceptions import ConnectionError, HTTPError

# Optionally providing an access token within a session if you have enabled push security
session = requests.Session()

# EXPO_TOKEN = "AAAAIht5BNQ:APA91bGzu1yR2Rnntvdg2CgDc8T_yTugIvXG8zjF0_3fpbuvudlvabJqJY4aoHTGeq3yxhqGCQN-Q99EtuQK0u41nDUp56j5hd9hiqjvXF9CF8ns1cA_omVlvTou71oCL6svp0gAs0No"
session.headers.update(
    {
        "accept": "application/json",
        "accept-encoding": "gzip, deflate",
        "content-type": "application/json",
    }
)


# Basic arguments. You should extend this function with the push features you
# want to use, or simply pass in a `PushMessage` object.
def send_push_message(token, title, message=None, extra=None):
    try:
        response = PushClient(session=session).publish(
            PushMessage(to=token,
                        title=title,
                        body=message,
                        data=extra))
    except PushServerError as exc:
        # Encountered some likely formatting/validation error.
        print("Push server error",
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
        # Encountered some Connection or HTTP error - retry a few times in
        # case it is transient.
        print("Connection error",
            {'token': token, 'message': message, 'extra': extra}
        )


    try:
        response.validate_response()
    except DeviceNotRegisteredError:
        print("Device not registered")
        # Mark the push token as inactive
        # from notifications.models import PushToken
        # PushToken.objects.filter(token=token).update(active=False)
    except PushTicketError as exc:
        # Encountered some other per-notification error.
        print( "Push ticket error",
            {
                'token': token,
                'message': message,
                'extra': extra,
                'push_response': exc.push_response._asdict(),
            }
       )


if __name__ == '__main__':
    token = "ExponentPushToken[dX0rL3AiD9q90-JC7jIScI]"
    send_push_message(
        token,
        "Hello world!",
        "This is a push notification message with custom data!"
    )
