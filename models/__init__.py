from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase

__all__ = ['author', 'book', 'borrow', 'BaseOrm']


convention = {
    "all_column_names": lambda constraint, table: "_".join(
        [column.name for column in constraint.columns.values()]
    ),
    "ix": "ix__%(table_name)s__%(all_column_names)s",
    "uq": "uq__%(table_name)s__%(all_column_names)s",
    "ck": "ck__%(table_name)s__%(constraint_name)s",
    "fk": "fk__%(table_name)s__%(all_column_names)s__%(referred_table_name)s",
    "pk": "pk__%(table_name)s",
}


class BaseOrm(DeclarativeBase):
    metadata = MetaData(naming_convention=convention)

    repr_cols_num = 3
    repr_cols = set()

    # def __repr__(self):
    #     cols = []
    #     for col_idx, col_name in enumerate(self.__table__.__dict__.keys()):
    #         if col_idx >= self.repr_cols_num:
    #             break
    #         if col_name in self.repr_cols:
    #             self.repr_cols.remove(col_name)
    #         cols.append(f"{col_name}={getattr(self, col_name)}")
    #     for col_name in self.repr_cols:
    #         cols.append(f"{col_name}={getattr(self, col_name)}")
    #
    #     return ", ".join(cols)
