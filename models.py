# Models go here
import peewee

db = peewee.SqliteDatabase("betsy.db")

class Tag(peewee.Model):
    tag = peewee.CharField(unique=True)

    class Meta:
        database = db

class Product(peewee.Model):
    name = peewee.TextField()
    description = peewee.TextField()
    price_in_cents = peewee.IntegerField(constraints=[peewee.Check("price_in_cents > 0")])
    quantity_on_stock = peewee.IntegerField(constraints=[peewee.Check("quantity_on_stock > 0")])
    tags = peewee.ManyToManyField(Tag)

    class Meta:
        database = db
        indexes = (
        (("name", "description"), True),
        )

class User(peewee.Model):
    name = peewee.TextField()
    address = peewee.TextField()
    billing_info = peewee.TextField()
    owned_products = peewee.ManyToManyField(Product)

    class Meta:
        database = db



class Transaction(peewee.Model):
    product = peewee.ForeignKeyField(Product)
    user_buyer = peewee.ForeignKeyField(User)
    quantity = peewee.IntegerField(constraints=[peewee.Check("quantity > 0")])
    timestamp = peewee.DateTimeField()

    class Meta:
        database = db

def create_tables():
    with db:
        db.create_tables([User, Product, Tag, Transaction, Product.tags.get_through_model(), User.owned_products.get_through_model()])


def delete_tables():
    with db:
        db.drop_tables([User, Product, Tag, Transaction, Product.tags.get_through_model(), User.owned_products.get_through_model()])
