from typing import Annotated
from datetime import datetime

from sqlalchemy import text
from sqlalchemy.orm import mapped_column


int_pk = Annotated[int, mapped_column(primary_key=True)]
created_at = Annotated[datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))]
updated_at = Annotated[datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"), onupdate=datetime.utcnow)]
str_uniq = Annotated[str, mapped_column(unique=True, nullable=False)]
str_null_true = Annotated[str, mapped_column(nullable=True)]
