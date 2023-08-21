import datetime
from app.schema import Temp_EmailBase, Category


class Temp_Email(Temp_EmailBase):
    id: int
    access_token: str
    created_at: datetime.datetime
    updated_at: datetime.datetime

    category: Category
