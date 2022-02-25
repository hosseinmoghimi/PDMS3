


def str_to_html(value):
    html=""
    lines=value.splitlines()
    for line in lines:
        html=html+line+"<br>"
    return html