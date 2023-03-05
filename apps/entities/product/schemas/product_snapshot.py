from apps.entities.product.types import UPC
from core.utils import ImmutableModel


class ProductSnapshotCreateSchema(ImmutableModel):
    product_id: UPC
    file_path: str

    @property
    def filename(self):
        return self.file_path.split("/")[-1]
