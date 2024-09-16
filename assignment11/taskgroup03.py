import time
import asyncio
from asyncio import Queue
from random import randrange

class Product:
    def __init__(self, product_name: str, checkout_time: float):
        self.product_name = product_name
        self.checkout_time = checkout_time

class Customer:
    def __init__(self, customer_id: int, products: list[Product]):
        self.customer_id = customer_id
        self.products = products

async def checkout_customer(queue: Queue, cashier_number: int):
    customer_count = 0  # Counter for the number of customers served.
    total_checkout_time = 0  # Total time spent by this cashier.
    total_time = 0

    while not queue.empty():
        customer: Customer = await queue.get()
        customer_start_time = time.perf_counter()
        print(f"Cashier_{cashier_number} will checkout Customer_{customer.customer_id}")

        for product in customer.products:
            if cashier_number == 2:
                adjusted_time = 0.1  # Cashier_2 ปรับ cashier 2 
                total_checkout_time += 0.1
                total_time += 0.1
            else:
                adjusted_time = round(product.checkout_time + (0.1 * cashier_number), 2)
                total_time += product.checkout_time + (0.1 * cashier_number)

            print(f"Cashier_{cashier_number} checking out Customer_{customer.customer_id}'s "
                  f"{product.product_name} in {adjusted_time} secs")
            await asyncio.sleep(adjusted_time)

        print(f"Cashier_{cashier_number} finished Customer_{customer.customer_id} "
              f"in {round(time.perf_counter() - customer_start_time, ndigits=2)} secs")
        
        queue.task_done()
        customer_count += 1
        total_checkout_time += time.perf_counter() - customer_start_time

    return customer_count, total_time

def generate_customer(customer_id: int) -> Customer:
    all_products = [Product('beef', 1),
                    Product('banana', .4), 
                    Product('sausage', .4), 
                    Product('diapers', .2)]
    return Customer(customer_id, all_products)

async def customer_generation(queue: Queue, customers: int):
    customer_count = 0
    while True:
        customers = [generate_customer(the_id) for the_id in range(customer_count, customer_count + customers)]
        for customer in customers:
            print(f"Waiting to put Customer_{customer.customer_id} in line.... ")
            await queue.put(customer)
            print(f"Customer_{customer.customer_id} put in line...")
        customer_count += len(customers)
        await asyncio.sleep(.001)
        return customer_count

async def main():
    CUSTOMER = 10
    QUEUE = 5
    CASHIER = 5
    customer_queue = Queue(QUEUE)
    customers_start_time = time.perf_counter()
    
    async with asyncio.TaskGroup() as group:
        customer_producer = group.create_task(customer_generation(customer_queue, CUSTOMER))
        cashiers = [group.create_task(checkout_customer(customer_queue, i)) for i in range(CASHIER)]
    
    results = await asyncio.gather(customer_producer, *cashiers)
    
    print("---------------------- Cashier Performance ----------------------")
    for i, (customer_count, total_checkout_time) in enumerate(results[1:], start=0):
        print(f"Cashier_{i} took {customer_count} customers in {round(total_checkout_time, ndigits=1)} secs.")
    print("---------------------------------------------------------------")
    print(f"The supermarket process finished {results[0]} customers "
          f"in {round(time.perf_counter() - customers_start_time, ndigits=2)} secs")

if __name__ == "__main__":
    asyncio.run(main())