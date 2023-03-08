from db.queries.base import QueriesBase


class ProductQueries(QueriesBase):
    def create_products(self, products: list[dict]):
        return self.db_client.executemany("INSERT INTO product (id, name) VALUES (%(id)s, %(name)s)", products)
