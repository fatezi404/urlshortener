import base64
import uuid 


def generate_short_id(): # TODO: Add async if something will crash o_O
    uuid_key = uuid.uuid4()
    return base64.urlsafe_b64encode(uuid_key.bytes).rstrip(b'=').decode()[:8]
