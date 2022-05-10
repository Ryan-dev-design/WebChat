from base64 import b64encode
from uuid import uuid4
print(b64encode(uuid4().bytes + uuid4().bytes))