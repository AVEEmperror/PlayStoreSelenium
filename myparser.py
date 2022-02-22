import json


def lexer(data: dict):
    # data = {coll_name: [data1, data 2]}

    # CLEARING THE DATA
    for key in data:
        for index, d in enumerate(data[key]):

            # NAME
            try:
                data[key][index]['name'] = data[key][index]['name'].replace('<span>', '').replace('</span>', '')
            except KeyError:
                pass

            # GENRE
            try:
                data[key][index]['genre'] = data[key][index]['genre'].replace('<span>', '').replace('</span>', '')
            except KeyError:
                pass

            # REVIEWS
            try:
                revs = data[key][index]['reviews']
                revs = revs[revs.find('">') + len('">'):revs.find('</')].replace(',', '')
                data[key][index]['reviews'] = revs
            except KeyError:
                pass

            # DEVELOPER
            try:
                dev = data[key][index]['developer']
                dev = dev[dev.find('">') + len('">'):dev.find('</')]
                data[key][index]['developer'] = dev
            except KeyError:
                pass

            # RATING


    return data

def parser(data: dict):
    # data = {coll_name: [data1, data 2]}

    outfile_name = r'GooglePlaySeleniumScrap\json\DATA.json'
    
    with open(outfile_name, 'w') as outfile:
        json.dump(data, outfile, indent=4)