from main import redis, Order
import time

GROUP = 'payment-group'
KEY = 'refund_order'

try:
    redis.xgroup_create(KEY, GROUP)
except Exception:
    print('Group already exists!')

while True:
    try:
        results = redis.xreadgroup(GROUP, KEY, {KEY: '>'}, None)

        if results != []:
            print(results)
            for result in results:
                obj = result[1][0][1]
                order = Order.get(obj['pk'])
                order.status = 'refunded'
                order.save()

    except Exception as e:
        print(str(e))
    time.sleep(1)
