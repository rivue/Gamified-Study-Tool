import re
from flask import request

emoji_pattern = re.compile("[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F700-\U0001F77F\U0001F780-\U0001F7FF\U0001F800-\U0001F8FF\U0001F900-\U0001F9FF\U0001FA70-\U0001FAFF\U0001FB00-\U0001FBFF\U0001FC00-\U0001FCFF\U0001FD00-\U0001FDFF\U0001FE00-\U0001FEFF\U0001FF00-\U0001FFFF]+", flags=re.UNICODE)

def decode_if_needed(s):
    # try:
    #     decoded_s = s.encode('latin1').decode('unicode_escape')
    #     if s != decoded_s:
    #         return decoded_s
    #     else:
    #         return s
    # except:
    #     return s
    return s
    
def extract_single_emoji(text):
    print(f"String: {text}")
    emojis = emoji_pattern.findall(text)
    print(f"Emojis: {emojis}")
    if not emojis:
        return None
    if emojis[0] == "\",":
        return None
    return emojis[0]

def remove_emojis(text):
    return emoji_pattern.sub(r'', text)

def remove_emojis_except_first(text):
    first_char = text[0] if text else ''
    if emoji_pattern.fullmatch(first_char):
        return first_char + emoji_pattern.sub(r'', text[1:])
    else:
        return emoji_pattern.sub(r'', text)
    
def mask_email(email):
    """
    someone@example.com -> s*****@example.com
    """
    try:
        local, domain = email.split('@')
    except ValueError:
        # If the email doesn't have '@', return it as is
        return email

    # Mask the local part: Keep the first character and replace the rest with `*`
    masked_local = local[0] + '*' * (len(local) - 1)

    return masked_local + '@' + domain

def clean_text(text):
    """Remove unwanted unicode artifacts like [U+202C] and other non-standard characters."""
    text = re.sub(r"\[U\+\w{4,5}\]", "", text)  # Remove unicode markers
    return text.strip()

def get_client_ip():
    forwarded_ip = request.headers.get("X-Forwarded-For")
    if forwarded_ip:
        return forwarded_ip.split(",")[0].strip()  # Extract first real IP
    return request.remote_addr or "127.0.0.1"

def parse_group_structure():
    groups = []
    form = request.form.to_dict(flat=False)  # get a dict where each value is a list
    # Find all group names; keys look like "groupNames[0]", "groupNames[1]", etc.
    group_name_pattern = re.compile(r'^groupNames\[(\d+)\]$')
    for key, values in form.items():
        match = group_name_pattern.match(key)
        if match:
            index = match.group(1)
            group_name = values[0]  # expecting one value per group name
            # Now extract sections for this group.
            # They come with keys like "groupSections[<index>][]"
            section_pattern = re.compile(r'^groupSections\[' + re.escape(index) + r'\]\[\]$')
            sections = []
            for k, v in form.items():
                if section_pattern.match(k):
                    # There might be multiple values if appended multiple times.
                    sections.extend(v)
            groups.append({'name': group_name, 'sections': sections})
    return groups
