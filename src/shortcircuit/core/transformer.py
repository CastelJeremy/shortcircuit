import base64
import json
import html
import datetime


def base64_encode(buffer: str):
    return base64.b64encode(buffer.encode()).decode()


def base64_decode(buffer: str):
    return base64.b64decode(buffer.encode()).decode()


def format_json(buffer: str):
    try:
        return json.dumps(json.loads(buffer), indent=4)
    except:
        raise Exception("JSON is invalid!")

def csv_to_json(buffer: str):
    header, *data = buffer.split("\n")
    data = [el for el in data if el]
    return json.dumps(list([
        dict(
            zip(header.split(','), line.split(','))
        )
        for line in data
    ]))

def html_escape(buffer: str):
    return html.escape(buffer)

def html_unescape(buffer: str):
    return html.unescape(buffer)

def unix_timestamp_to_datetime(buffer: str):
    time_stamp = int(buffer)
    return datetime.datetime.utcfromtimestamp(time_stamp).strftime('%Y-%m-%d %H:%M:%SZ')


def transform_str(str_input: str, transformer: str):
    transformer_fn = TRANSFORMER_FN_MAP.get(transformer)
    if transformer_fn:
        return transformer_fn(str_input)
    return str_input


TRANSFORMER_FN_MAP = {
    "Base64 encode": base64_encode,
    "Base64 decode": base64_decode,
    "Format JSON": format_json,
    "CSV to JSON": csv_to_json,
    "HTML Encode": html_escape,
    "HTML Decode": html_unescape,
    "Epoch Converter": unix_timestamp_to_datetime,
}
