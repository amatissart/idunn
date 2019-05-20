from apistar import validators
from idunn.blocks.base import BlocksValidator
from idunn.api.utils import LONG, BLOCKS_BY_VERBOSITY
from idunn.utils.types import BaseType


class PlaceMeta(BaseType):
    source = validators.String(allow_null=True)

class Place(BaseType):
    type = validators.String()
    id = validators.String(allow_null=True)
    name = validators.String(allow_null=True)
    local_name = validators.String(allow_null=True)
    class_name = validators.String(allow_null=True)
    subclass_name = validators.String(allow_null=True)
    geometry = validators.Object(allow_null=True)
    address = validators.Object(allow_null=True)
    blocks = BlocksValidator(allowed_blocks=BLOCKS_BY_VERBOSITY.get(LONG))
    meta = PlaceMeta
