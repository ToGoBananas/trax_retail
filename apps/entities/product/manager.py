from apps.entities.base import BaseManager
from apps.entities.product.schemas.product import ProductCreateSchema
from apps.entities.product.schemas.product_snapshot import ProductSnapshotCreateSchema


class ProductManager(BaseManager):

    def create(self, products: list[ProductCreateSchema]):
        for product in products:  # TODO: execute concurrently
            self.s3_client.put_object(product.file_path, save_dir='products', content_type='image/jpeg')
        self.db_client.executemany(
            'INSERT INTO product (id, name) VALUES (%(id)s, %(name)s)', [product.dict(exclude={'file_path',}) for product in products]
        )


class ProductSnapshotManager(BaseManager):

    def create(self, snapshots: list[ProductSnapshotCreateSchema]):
        for snapshot in snapshots:
            self.s3_client.put_object(snapshot.file_path, save_dir=f'product_snapshots/{snapshot.product_id}', content_type='image/jpeg')
        self.db_client.executemany(
            'INSERT INTO product_snapshot (product_id, filename) VALUES (%(product_id)s, %(filename)s)',
            [
                {"filename": snapshot.filename, "product_id": snapshot.product_id}
                for snapshot in snapshots
            ]
        )

