from loader import dp
from .isgroup import IsGroup
from .isprivate import IsPrivate

if __name__ == "filters":
    dp.filters_factory.bind(IsGroup)
    dp.filters_factory.bind(IsPrivate)
