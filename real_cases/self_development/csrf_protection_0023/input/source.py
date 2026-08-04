# csrf_protection

def process_data(data):
    result = []
    for item in data:
        if item not in result:
            result.append(item)
    return result

def calculate(x, y):
    return x + y

def another_calculate(x, y):
    return x + y
