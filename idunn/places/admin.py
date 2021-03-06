from .place import Place
from idunn.api.utils import build_blocks, get_geom

class Admin(Place):
    PLACE_TYPE = 'admin'

    @classmethod
    def build_admin(cls, es_place):
        return {
            'label': es_place.get('label')
        }

    @classmethod
    def get_postcodes(cls, es_place):
        return es_place.get("zip_codes")

    @classmethod
    def load_place(cls, es_place, lang, settings, verbosity):
        admin_addr = cls.build_address(es_place)

        return cls(
            id=es_place.get('id', ''),
            name=es_place.get('name', ''),
            local_name=es_place.get('name'),
            class_name=es_place.get('zone_type'),
            subclass_name=es_place.get('zone_type'),
            geometry=get_geom(es_place),
            address=admin_addr,
            blocks=build_blocks(es_place, lang, verbosity)
        )
