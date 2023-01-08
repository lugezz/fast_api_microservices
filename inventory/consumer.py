from main import redis, Product
import time

GROUP = 'inventory-group'
KEY = 'order_completed'

try:
    redis.xgroup_create(KEY, GROUP)
except Exception:
    print('Group already exists!')

while True:
    try:
        results = redis.xreadgroup(GROUP, KEY, {KEY: '>'}, None)

        if results:
            for result in results:
                obj = result[1][0][1]
                try:
                    product = Product.get(obj['product_id'])
                    product.quantity = product.quantity - int(obj['quantity'])
                    print(f"{obj['quantity']} reduced from {product.name}")
                    product.save()
                except Exception:
                    redis.xadd('refund_order', obj, '*')

    except Exception as e:
        print(str(e))
    time.sleep(1)
