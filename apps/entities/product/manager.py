from apps.entities.product.schemas.product import ProductCreateSchema
from apps.entities.product.schemas.product_snapshot import ProductSnapshotCreateSchema
from apps.entities.base import BaseManager
from db.queries.products.product import ProductQueries
from db.queries.products.product_snapshot import ProductSnapshotQueries


class ProductManager(BaseManager):
    SAVE_DIR = "products"
    queries: ProductQueries = ProductQueries

    @classmethod
    def build_product_image_url(cls, product_id):
        return f"http://{cls.s3_client.config.host}:{cls.s3_client.config.port}/{cls.s3_client.config.bucket_name}/{cls.SAVE_DIR}/{product_id}.jpg"

    def create(self, products: list[ProductCreateSchema]):
        for product in products:  # TODO: execute concurrently
            self.s3_client.put_object(product.file_path, save_dir=self.SAVE_DIR, content_type="image/jpeg")
        self.queries.create_products(
            [
                product.dict(
                    exclude={
                        "file_path",
                    }
                )
                for product in products
            ]
        )


class ProductSnapshotManager(BaseManager):
    SAVE_DIR = "product_snapshots"
    queries: ProductSnapshotQueries = ProductSnapshotQueries

    @classmethod
    def build_snapshot_image_url(cls, product_id, filename):
        return f"http://{cls.s3_client.config.host}:{cls.s3_client.config.port}/{cls.s3_client.config.bucket_name}/{cls.SAVE_DIR}/{product_id}/{filename}"

    def create(self, snapshots: list[ProductSnapshotCreateSchema]):
        for snapshot in snapshots:
            self.s3_client.put_object(
                snapshot.file_path, save_dir=f"{self.SAVE_DIR}/{snapshot.product_id}", content_type="image/jpeg"
            )
        self.queries.create_snapshots(
            [{"filename": snapshot.filename, "product_id": snapshot.product_id} for snapshot in snapshots]
        )
