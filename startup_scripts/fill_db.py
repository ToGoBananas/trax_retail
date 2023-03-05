import os
from pathlib import Path

from apps.entities.product.manager import ProductManager, ProductSnapshotManager
from apps.entities.product.schemas.product import ProductCreateSchema
from apps.entities.product.schemas.product_snapshot import ProductSnapshotCreateSchema

from faker import Faker


fake = Faker()
PRODUCT_PATH = Path(__file__).resolve().parent.resolve().joinpath("data", "products")
SNAPSHOTS_PATH = Path(__file__).resolve().parent.resolve().joinpath("data", "snapshots")


def create_products():
    products = []
    for file_name in os.listdir(PRODUCT_PATH):
        upc = file_name.split('.')[0]
        products.append(ProductCreateSchema(
            file_path=os.path.join(PRODUCT_PATH, file_name),
            name=fake.name(),
            id=upc
        ))
    ProductManager().create(products)


def create_snapshots():
    snapshots = []
    for upc in os.listdir(SNAPSHOTS_PATH):
        for file_name in os.listdir(os.path.join(SNAPSHOTS_PATH, upc)):
            snapshots.append(ProductSnapshotCreateSchema(
                file_path=os.path.join(SNAPSHOTS_PATH, upc, file_name),
                product_id=upc
            ))
    ProductSnapshotManager().create(snapshots)


create_products()
create_snapshots()
