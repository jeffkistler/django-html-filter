"""
Some helpful utilities.
"""

def parse_content_type(content_type):
    """
    Parse the Content-Type header.
    """
    # Split the type and the params
    if ';' in content_type:
        i = content_type.index(';')
        plisttext = content_type[i:]
        content_type = content_type[:i]
    else:
        plisttext = ''
    # Parse the params
    params = {}
    if plisttext:
        while plisttext[:1] == ';':
            # TODO: Handle quoted params
            plisttext = plisttext[1:]
            if ';' in plisttext:
                end = plisttext.index(';')
            else:
                end = len(plisttext)
            param = plisttext[:end]
            if '=' in param:
                i = param.index('=')
                name = param[:i].strip().lower()
                value = param[i+1:].strip()
            else:
                name, value = param, True
            params[name] = value
            plisttext = plisttext[end:]
            print plisttext
    return content_type, params

def parse_subtype(content_type):
    """
    Parse the subtype of a Content-Type.
    """
    content_type, params = parse_content_type(content_type)
    fields = content_type.split('/')
    for i in range(len(fields)):
        fields[i] = fields[i].strip().lower()
    subtype = '/'.join(fields[1:])
    return subtype
