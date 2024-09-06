import time
import asyncio
from asyncio import Queue

class Product:
    def __init__(self, product_name: str, checkout_time: float):
        self.product_name = product_name
        self.checkout_time = checkout_time


class Customer:
    def __init__(self, customer_id: int, products: list[Product]):
        self.customer_id = customer_id
        self.products = products


async def checkout_customer(queue: Queue, cashier_number: int):
    cashier_total_time = 0  # Initialize cashier's total time
    cashier_start_time = time.perf_counter()  # Start time for the cashier
    customer_count = 0  # Count how many customers this cashier checks out
    while not queue.empty():
        customer: Customer = await queue.get()
        customer_start_time = time.perf_counter()
        print(f"The Cashier_{cashier_number} will checkout Customer_{customer.customer_id}")
        for product in customer.products:
            print(f"The Cashier_{cashier_number} "
                  f"will checkout Customer_{customer.customer_id}'s "
                  f"Product_{product.product_name} "
                  f"in {product.checkout_time} secs")
            await asyncio.sleep(product.checkout_time)
        
        # customer_checkout_time = time.perf_counter() - customer_start_time
       
        print(f"The Cashier_{cashier_number} finished checkout Customer_{customer.customer_id} "
              f"in {round(time.perf_counter() - customer_start_time, ndigits=2)} secs")

        customer_count += 1  # Increment customer count
        cashier_total_time += round(time.perf_counter() - customer_start_time)  # Add to cashier's total time
        queue.task_done()

    return customer_count, cashier_total_time

    # After all customers are processed, store total time and customer count for the cashier
    # cashier_total_time = time.perf_counter() - cashier_start_time
    # cashier_times[cashier_number] = round(cashier_total_time, ndigits=2)
    # cashier_customer_counts[cashier_number] = customer_count


def generate_customer(customer_id: int) -> Customer:
    all_products = [Product('beef', 1),
                    Product('banana', .4),
                    Product('sausage', .4),
                    Product('diapers', .2)]
    return Customer(customer_id, all_products)


async def customer_generation(queue: Queue, customers: int):
    customer_count = 0
    while True:
        customers = [generate_customer(the_id)
                     for the_id in range(customer_count, customer_count + customers)]
        for customer in customers:
            print("waiting to put customer in line...")
            await queue.put(customer)
            print("Customer put in line...")
        customer_count = customer_count + len(customers)
        await asyncio.sleep(.001)
        return customer_count



async def main():
    number_of_cashiers = 5  # You can change this to any number of cashiers you want

    customer_queue = Queue(3)
    customers_start_time = time.perf_counter()

    # Dynamically create lists to store the total times and customer counts for each cashier
    cashier_times = [0] * number_of_cashiers
    cashier_customer_counts = [0] * number_of_cashiers

    customer_producer = asyncio.create_task(customer_generation(customer_queue, 10))
    cashiers = [checkout_customer(customer_queue, i) for i in range(number_of_cashiers)]

    result = await asyncio.gather(customer_producer, *cashiers)
    print(result)
    print("---------------------")
    # Print the total times and customer counts after all cashiers are done
    count = 0
    for i in result[1:]:
        # print(i[0])
        print(f"The Cashier_{count} take {i[0]} customers total {i[1]} secs")
        count += 1
    print(" ")
    print(f"The supermarket process finished {customer_producer.result()} customers "
          f"in {round(time.perf_counter() - customers_start_time, ndigits=2)} secs")


if __name__ == "__main__":
    asyncio.run(main())
