import base64
import json


def base64_encode(buffer: str):
    return base64.b64encode(buffer.encode()).decode()


def base64_decode(buffer: str):
    return base64.b64decode(buffer.encode()).decode()


def format_json(buffer: str):
    try:
        return json.dumps(json.loads(buffer), indent=4)
    except:
        raise Exception("JSON is invalid!")


def transform_str(str_input: str, transformer: str):
    transformer_fn = TRANSFORMER_FN_MAP.get(transformer)
    if transformer_fn:
        return transformer_fn(str_input)
    return str_input


TRANSFORMER_FN_MAP = {
    "Base64 encode": base64_encode,
    "Base64 decode": base64_decode,
    "JSON Format": format_json,
}
