__winc_id__ = "d7b474e9b3a54d23bca54879a4f1855b"
__human_name__ = "Betsy Webshop"

import models
import peewee
from datetime import datetime

def search(term):
    # truth to be told, I think typo matching should be done through machine learning
    # but I fear that would break the limits of this assignment

    products_found = []
    term = term.lower()
    query = models.Product.select()
    possible_typos_list = [term]
    for i in range(len(term)):
        typo = list(term)
        # checking for a missing letter
        typo.pop(i)

        if ''.join(typo) not in possible_typos_list:
            possible_typos_list.append(''.join(typo))
        s = list(term)
        try:
            #checking for 2 characters swapped
            if s[i] != s[i+1]:
                s[i], s[i+1] = s[i+1], s[i]
                typo2 = ''.join(s)
                if typo2 not in possible_typos_list:
                    possible_typos_list.append(typo2)
        except IndexError:
            pass

    for item in query:
        for word in possible_typos_list:
            if word in item.name.lower() or word in item.description.lower():
                if item not in products_found:
                    products_found.append(item)

    return products_found        


def list_user_products(user_id):
    query = models.User.get_by_id(user_id)
    return query.owned_products


def list_products_per_tag(tag_id):
    tag_id = models.Tag.get_by_id(tag_id)
    query = models.Product.select()
    result = []
    for item in query:
        for tag in item.tags:
            if tag_id == tag:
                result.append(item)
    return result


def add_product_to_catalog(user_id, product):
    # function was fixed
    user = models.User.get_by_id(user_id)
    current_owned = []
    for item in user.owned_products:
        current_owned.append(item)
    current_owned.append(product)
    user.owned_products=current_owned
    user.save()
    return None

def update_stock(product_id, new_quantity):
    product = models.Product.get_by_id(product_id)
    product.quantity_on_stock = new_quantity
    product.save()
    return None


def purchase_product(product_id, buyer_id, quantity):
    product1 = models.Product.get_by_id(product_id)
    if product1.quantity_on_stock >= quantity:
        buyer = models.User.get_by_id(buyer_id)
        product1.quantity_on_stock -= quantity
        product1.save()
        models.Transaction.create(product=product1, user_buyer=buyer, quantity=quantity, timestamp=datetime.now())
        print("transaction complete")
        return None
    else:
        print("could not sell the requested amount")
        return None




def remove_product(product_id):
    product = models.Product.get_by_id(product_id)
    product.delete_instance()

def populate_test_database():
    def create_users():
        alice = models.User(name="Alice Alderton", address="Ankara, Albert street 8/A", billing_info="12345678")
        bob = models.User(name="Bob Birch", address="Budapest, Bartok Bela ut 46/B", billing_info="7654321")
        chad = models.User(name="Chad Chavez", address="Canterbury, Cross road 14/C", billing_info="0001112")

        alice.save()
        bob.save()
        chad.save()

        bass = models.Product.select().where(models.Product.name=="Bass guitar")[0]
        ukulele = models.Product.select().where(models.Product.name=="Ukulele")[0]
        sax = models.Product.select().where(models.Product.name=="Saxophone")[0]
        harp = models.Product.select().where(models.Product.name=="Blues harp")[0]


        alice.owned_products = [bass]
        bob.owned_products = [ukulele, harp]
        chad.owned_products = [sax]

        alice.save()
        bob.save()
        chad.save()

    def create_products():
        bass = models.Product(name="Bass guitar",
                              description="It's like a guitar, but way cooler.", 
                              price_in_cents=45000, 
                              quantity_on_stock=2,
                              for_sale = True)
        ukulele = models.Product(name="Ukulele",
                              description="It's like a guitar, but way smaller.", 
                              price_in_cents=2000, 
                              quantity_on_stock=2,
                              for_sale = True)
        sax = models.Product(name="Saxophone",
                              description="It's nothing like a guitar, but we still like it.", 
                              price_in_cents=67000, 
                              quantity_on_stock=2,
                              for_sale = True)
        harp = models.Product(name="Blues harp",
                              description="A harmonica is cool if you can play it, but very annoying when you can't yet!",
                              price_in_cents = 10000,
                              quantity_on_stock = 4,
                              for_sale = True)

        instrument = models.Tag.select().where(models.Tag.tag=="instrument")
        string = models.Tag.select().where(models.Tag.tag=="string")
        wind = models.Tag.select().where(models.Tag.tag=="wind")
        reed = models.Tag.select().where(models.Tag.tag=="reed")
        cheap = models.Tag.select().where(models.Tag.tag=="cheap")
        expensive = models.Tag.select().where(models.Tag.tag=="expensive")
        brown = models.Tag.select().where(models.Tag.tag=="brown")
        blue = models.Tag.select().where(models.Tag.tag=="blue")
        golden = models.Tag.select().where(models.Tag.tag=="golden")

        bass.save()
        ukulele.save()
        sax.save()
        harp.save()

        bass.tags = [instrument, string, expensive, blue]
        bass.save()

        ukulele.tags = [instrument, string, cheap, brown]
        ukulele.save()

        sax.tags = [instrument, wind, expensive, reed, golden]
        sax.save()

        harp.tags = [instrument, wind, cheap, reed, brown]
        harp.save()



    def create_tags():
        models.Tag.create(tag="instrument")
        models.Tag.create(tag="string")
        models.Tag.create(tag="wind")
        models.Tag.create(tag="reed")
        models.Tag.create(tag="cheap")
        models.Tag.create(tag="expensive")
        models.Tag.create(tag="brown")
        models.Tag.create(tag="blue")
        models.Tag.create(tag="golden")

    create_tags()
    create_products()
    create_users()

def run_tests():
    models.delete_tables()
    models.create_tables()
    populate_test_database()

    search_result = search("hapr")
    for item in search_result:
        print("test search", item.name)

    result = list_user_products(1)
    for item in result:
        print("test list user products", item.name)

    result = list_products_per_tag(2)
    for item in result:
        print("test products per tag", item.name)

    purchase_product(1,1,1)
    purchase_product(1,1,1)
    purchase_product(1,1,1)


    harp = models.Product.get_by_id(4)
    add_product_to_catalog(1, harp)
    

    models.delete_tables()

run_tests()