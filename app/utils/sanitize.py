import re

def sanitize_id_no(raw_input):
    return ''.join(re.findall(r'\d', raw_input))
