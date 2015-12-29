def format_fuzzy_direction(angle):
    # text = ['E', 'S', 'W', 'N']
    text = ['NE', 'E', 'SE', 'S', 'SW', 'W', 'NW', 'N']
    s = 360/len(text)
    return text[int((angle-s/2)//s%len(text))]


def format_distance(distance):
    if distance > 1:
       text = '{:,.0f}km'.format(distance)
    else:
       text = '{:,.0f}m'.format(distance*1000)
    return text
