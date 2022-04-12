from uuid import uuid4


def generate_unique_user_code():
    code = ''.join(str(uuid4()).split('-'))[:8]
    return code
