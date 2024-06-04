def parse_data(data):
    try:
        for dataKey in data:
            category = data[dataKey]
            for key in category:
                category[key] = round(round(float(category[key]), 4) * 100, 2)
            category = dict(sorted(category.items(), key=lambda item: item[1], reverse=True))
            data[dataKey] = category
        return data
    except:
        print('Parse error occuired')
