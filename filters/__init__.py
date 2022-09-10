from loader import dp
from .isgroup import IsGroup
from .isprivate import IsPrivate
from .isadmin import IsAdmin

if __name__ == "filters":
    dp.filters_factory.bind(IsGroup)
    dp.filters_factory.bind(IsPrivate)
    dp.filters_factory.bind(IsAdmin)