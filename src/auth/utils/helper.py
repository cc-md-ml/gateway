import json

from httpx import Response


def parse_response_to_dict(response: Response) -> dict:
    """
    Loads json response into dict
    """
    return json.loads(response.content.decode('utf-8'))
