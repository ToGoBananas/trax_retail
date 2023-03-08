from pydantic import constr

from apps.entities.product.types import UPC
from core.types import NaiveDatetime
from core.types import TINYTEXT
from core.utils import ImmutableModel


class ProductCreateSchema(ImmutableModel):
    id: UPC
    name: constr(min_length=1, max_length=TINYTEXT.max_length, strip_whitespace=True)
    file_path: str


class ProductDBSchema(ImmutableModel):
    id: UPC
    name: constr(min_length=1, max_length=TINYTEXT.max_length, strip_whitespace=True)
    file_name: constr(min_length=10, max_length=10)
    created: NaiveDatetime
