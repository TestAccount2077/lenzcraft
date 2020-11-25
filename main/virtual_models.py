

def get_items():
    
    with open('glassesSKU.csv') as f:
        return f.read()

ITEMS = get_items()


def get_models_for_db():
    
    items = []
    
    for item in ITEMS.split('\n'):
        
        if item:
            sku, name = item.split(',')
            items.append((sku, name))
        
    return tuple(items)
        

MODELS_FOR_DB = get_models_for_db()
