import os
import json
import pytest
import urllib
from app import app
from apistar.test import TestClient
from freezegun import freeze_time

"""
    This module tests basic query against the endpoint '/places/'
"""

INDICES = {
    "admin": "munin_admin",
    "street": "munin_street",
    "addr": "munin_addr",
    "poi": "munin_poi"
}

def load_place(file_name, mimir_client, doc_type):
    """
    Load a json file in the elasticsearch and returns the corresponding Place id
    """

    index_name = INDICES.get(doc_type)

    filepath = os.path.join(os.path.dirname(__file__), 'fixtures', file_name)
    with open(filepath, "r") as f:
        place = json.load(f)
        place_id = place['id']
        mimir_client.index(index=index_name,
                        body=place,
                        doc_type=doc_type, # 'admin', 'street', 'addr' or 'poi'
                        id=place_id,
                        refresh=True)

@pytest.fixture(autouse=True)
def load_all(mimir_client, init_indices):
    load_place('admin_goujounac.json', mimir_client, 'admin')
    load_place('street_birnenweg.json', mimir_client, 'street')
    load_place('address_du_moulin.json', mimir_client, 'addr')
    load_place('orsay_museum.json', mimir_client, 'poi')

"""
    The purpose of the 4 following tests 'test_full'
    is to describe the response format for each possible
    spatial objects (Admin, Street, Address, POI)
"""

def test_full_query_admin():
    """
        Test the response format to an admin query
    """
    client = TestClient(app)
    response = client.get(
            url=f'http://localhost/v1/places/admin:osm:relation:123057?lang=fr',
            )
    assert response.status_code == 200
    assert response.headers.get('Access-Control-Allow-Origin') == '*'

    resp = response.json()

    assert resp == {
        'type': 'admin',
        'id': 'admin:osm:relation:123057',
        'name': 'Goujounac',
        'local_name': 'Goujounac',
        'class_name': 'city',
        'subclass_name': 'city',
        'geometry': {
            'type': 'Point',
            'coordinates': [1.1957467, 44.5756909],
            'center': [1.1957467, 44.5756909],
            'bbox': [1.1777833, 44.5547916, 1.2237663, 44.5978805]
        },
        'address': {
            'admin': {
                'label': 'Goujounac (46250), Lot, Occitanie, France',
            },
            'admins': [],
            'id': None,
            'label': None,
            'name': None,
            'housenumber': None,
            'postcode': '46250',
            'street': {
                'id': None,
                'name': None,
                'label': None,
                'postcodes': None
            }
        },
        'blocks': []
    }

def test_full_query_street():
    """
        Test the response format to a street query
    """
    client = TestClient(app)
    response = client.get(
        url=f'http://localhost/v1/places/35460343?lang=fr',
    )

    assert response.status_code == 200
    assert response.headers.get('Access-Control-Allow-Origin') == '*'

    resp = response.json()

    assert resp == {
        "type": "street",
        "id": "35460343",
        "name": "9a Birnenweg",
        "local_name": "9a Birnenweg",
        "class_name": "street",
        "subclass_name": "street",
        "geometry": {
            "type": "Point",
            "coordinates": [ 10.6646915, 53.847809999999996],
            "center": [ 10.6646915, 53.847809999999996]
            },
        "address": {
            "admin": None,
            "id": None,
            "label": None,
            "name": None,
            "housenumber": None,
            "postcode": "77777",
            "street": {
                "id": '35460343',
                "name": '9a Birnenweg',
                "label": '9a Birnenweg (Label)',
                "postcodes": ["77777"]
            },
            "admins": [
                { "id": "admin:osm:relation:27027", "label": "L\u00fcbeck, Schleswig-Holstein, Deutschland", "name": "L\u00fcbeck", "class_name": 6, "postcodes": [] },
                { "id": "admin:osm:relation:51529", "label": "Schleswig-Holstein, Deutschland", "name": "Schleswig-Holstein", "class_name": 4, "postcodes": [] },
                { "id": "admin:osm:relation:51477", "label": "Deutschland", "name": "Deutschland", "class_name": 2, "postcodes": [] },
                { "id": "admin:osm:relation:367854", "label": "Sankt Lorenz S\u00fcd, L\u00fcbeck, Schleswig-Holstein, Deutschland", "name": "Sankt Lorenz S\u00fcd", "class_name": 9, "postcodes": [] }
            ]
        },
        "blocks": []
    }


def test_full_query_address():
    """
        Test the response format to an address query
    """
    client = TestClient(app)
    id_moulin = urllib.parse.quote_plus("addr:5.108632;48.810273")

    response = client.get(
        url=f'http://localhost/v1/places/{id_moulin}?lang=fr',
    )

    assert response.status_code == 200
    assert response.headers.get('Access-Control-Allow-Origin') == '*'

    resp = response.json()

    assert resp == {
        'type': 'address',
        'id': 'addr:5.108632;48.810273',
        'name': '4 Rue du Moulin',
        'local_name': '4 Rue du Moulin',
        'class_name': 'address',
        'subclass_name': 'address',
        'geometry': {
            'type': 'Point',
            'coordinates': [5.108632, 48.810273],
            'center': [5.108632, 48.810273]
        },
        'address': {
            'admin': None,
            'id': 'addr:5.108632;48.810273',
            'label': '4 Rue du Moulin (Val-d\'Ornain)',
            'name': '4 Rue du Moulin',
            'housenumber': '4',
            'postcode': '55000',
            'street': {
                'id': 'street:553660045D',
                'name': 'Rue du Moulin',
                'label': "Rue du Moulin (Val-d'Ornain)",
                'postcodes': ['55000']
            },
            'admins': [
                {'id': 'admin:osm:relation:7382', 'label': 'Meuse, Grand Est, France', 'name': 'Meuse', 'class_name': 6, 'postcodes': []},
                {'id': 'admin:osm:relation:3792876', 'label': 'Grand Est, France', 'name': 'Grand Est', 'class_name': 4, 'postcodes': []},
                {'id': 'admin:osm:relation:2202162', 'label': 'France', 'name': 'France', 'class_name': 2, 'postcodes': []},
                {'id': 'admin:osm:relation:2645341', 'label': "Val-d'Ornain (55000), Meuse, Grand Est, France", 'name': "Val-d'Ornain", 'class_name': 8, 'postcodes': ['55000']}
            ]
        },
        'blocks': []
    }

@freeze_time("2018-06-14 8:30:00", tz_offset=0)
def test_full_query_poi():
    """
        Test the response format to a POI query
    """
    client = TestClient(app)
    response = client.get(
        url=f'http://localhost/v1/places/osm:way:63178753?lang=fr',
    )

    assert response.status_code == 200
    assert response.headers.get('Access-Control-Allow-Origin') == '*'

    resp = response.json()

    assert resp == {
        'type': 'poi',
        'id': 'osm:way:63178753',
        'name': "Musée d'Orsay",
        'local_name': "Musée d'Orsay",
        'class_name': 'museum',
        'subclass_name': 'museum',
        'geometry': {
            'type': 'Point',
            'coordinates': [2.3265827716099623, 48.859917803575875],
            'center': [2.3265827716099623, 48.859917803575875]
        },
        'address': {
            'admin': None,
            'id': 'addr_poi:osm:way:63178753',
            'label': '1 Rue de la Légion d\'Honneur (Paris)',
            'name': '1 Rue de la Légion d\'Honneur',
            'housenumber': '1',
            'postcode': '75007',
            'street': {
                'id': 'street_poi:osm:way:63178753',
                'name': 'Rue de la Légion d\'Honneur',
                'label': 'Rue de la Légion d\'Honneur (Paris)',
                'postcodes': ['75007']
            },
            'admins': [
                {'id': 'admin:osm:relation:2188567', 'label': "Quartier Saint-Thomas-d'Aquin (75007), Paris 7e Arrondissement, Paris, Île-de-France, France", 'name': "Quartier Saint-Thomas-d'Aquin", 'class_name': 10, 'postcodes': ['75007']},
                {'id': 'admin:osm:relation:9521', 'label': 'Paris 7e Arrondissement (75007), Paris, Île-de-France, France', 'name': 'Paris 7e Arrondissement', 'class_name': 9, 'postcodes': ['75007']},
                {'id': 'admin:osm:relation:7444', 'label': 'Paris (75000-75116), Île-de-France, France', 'name': 'Paris', 'class_name': 8, 'postcodes': ['75000', '75001', '75002', '75003', '75004', '75005', '75006', '75007', '75008', '75009', '75010', '75011', '75012', '75013', '75014', '75015', '75016', '75017', '75018', '75019', '75020', '75116']},
                {'id': 'admin:osm:relation:71525', 'label': 'Paris, Île-de-France, France', 'name': 'Paris', 'class_name': 6, 'postcodes': []},
                {'id': 'admin:osm:relation:8649', 'label': 'Île-de-France, France', 'name': 'Île-de-France', 'class_name': 4, 'postcodes': []},
                {'id': 'admin:osm:relation:2202162', 'label': 'France', 'name': 'France', 'class_name': 2, 'postcodes': []}
            ]
        },
        'blocks': [
            {'type': 'opening_hours', 'status': 'open', 'next_transition_datetime': '2018-06-14T21:45:00+02:00', 'seconds_before_next_transition': 40500, 'is_24_7': False, 'raw': 'Tu-Su 09:30-18:00; Th 09:30-21:45', 'days': [{'dayofweek': 1, 'local_date': '2018-06-11', 'status': 'closed', 'opening_hours': []}, {'dayofweek': 2, 'local_date': '2018-06-12', 'status': 'open', 'opening_hours': [{'beginning': '09:30', 'end': '18:00'}]}, {'dayofweek': 3, 'local_date': '2018-06-13', 'status': 'open', 'opening_hours': [{'beginning': '09:30', 'end': '18:00'}]}, {'dayofweek': 4, 'local_date': '2018-06-14', 'status': 'open', 'opening_hours': [{'beginning': '09:30', 'end': '21:45'}]}, {'dayofweek': 5, 'local_date': '2018-06-15', 'status': 'open', 'opening_hours': [{'beginning': '09:30', 'end': '18:00'}]}, {'dayofweek': 6, 'local_date': '2018-06-16', 'status': 'open', 'opening_hours': [{'beginning': '09:30', 'end': '18:00'}]}, {'dayofweek': 7, 'local_date': '2018-06-17', 'status': 'open', 'opening_hours': [{'beginning': '09:30', 'end': '18:00'}]}]},
            {'type': 'phone', 'url': 'tel:+33140494814', 'international_format': '+33140494814', 'local_format': '+33140494814'},
            {'type': 'information', 'blocks': [{'type': 'services_and_information', 'blocks': [{'type': 'accessibility', 'wheelchair': 'yes', 'toilets_wheelchair': 'unknown'}, {'type': 'internet_access', 'wifi': True}, {'type': 'brewery', 'beers': [{'name': 'Tripel Karmeliet'}, {'name': 'Delirium'}, {'name': 'Chouffe'}]}]}]},
            {'type': 'website', 'url': 'http://www.musee-orsay.fr'}
        ]
    }



def test_type_query_admin():
    client = TestClient(app)
    response = client.get(
        url=f'http://localhost/v1/places/admin:osm:relation:123057?lang=fr&type=admin',
    )
    assert response.status_code == 200
    assert response.headers.get('Access-Control-Allow-Origin') == '*'

    resp = response.json()

    assert resp["id"] == "admin:osm:relation:123057"
    assert resp["name"] == "Goujounac"

def test_type_query_street():
    client = TestClient(app)
    response = client.get(
        url=f'http://localhost/v1/places/35460343?lang=fr&type=street',
    )

    assert response.status_code == 200
    assert response.headers.get('Access-Control-Allow-Origin') == '*'

    resp = response.json()

    assert resp["id"] == "35460343"
    assert resp["name"] == "9a Birnenweg"

def test_type_query_address():
    client = TestClient(app)
    id_moulin = urllib.parse.quote_plus("addr:5.108632;48.810273")

    response = client.get(
        url=f'http://localhost/v1/places/{id_moulin}?lang=fr&type=address',
    )

    assert response.status_code == 200
    assert response.headers.get('Access-Control-Allow-Origin') == '*'

    resp = response.json()

    assert resp["id"] == "addr:5.108632;48.810273"
    assert resp["name"] == "4 Rue du Moulin"


def test_type_query_poi():
    client = TestClient(app)
    response = client.get(
        url=f'http://localhost/v1/places/osm:way:63178753?lang=fr&type=poi',
    )

    assert response.status_code == 200
    assert response.headers.get('Access-Control-Allow-Origin') == '*'

    resp = response.json()

    assert resp["id"] == "osm:way:63178753"
    assert resp["name"] == "Musée d'Orsay"
    assert resp["local_name"] == "Musée d'Orsay"
    assert resp["class_name"] == "museum"
    assert resp["subclass_name"] == "museum"
    assert resp["blocks"][0]["type"] == "opening_hours"
    assert resp["blocks"][1]["type"] == "phone"
    assert resp["blocks"][0]["is_24_7"] == False

def test_type_unknown():
    client = TestClient(app)

    id_moulin = urllib.parse.quote_plus("addr:5.108632;48.810273")

    response = client.get(
        url=f'http://localhost/v1/places/{id_moulin}?lang=fr&type=globibulga',
    )
    assert response.status_code == 400
    assert response._content == b'{"message":"Wrong type parameter: type=globibulga"}'

def test_wrong_type():
    client = TestClient(app)

    id_moulin = urllib.parse.quote_plus("addr:5.108632;48.810273")

    response = client.get(
        url=f'http://localhost/v1/places/{id_moulin}?lang=fr&type=poi',
    )
    assert response.status_code == 404
    assert response._content == b'{"message":"place addr:5.108632;48.810273 not found with type=poi"}'

def test_basic_short_query_poi():
    client = TestClient(app)
    response = client.get(
        url=f'http://localhost/v1/places/osm:way:63178753?lang=fr&verbosity=short',
    )

    assert response.status_code == 200
    assert response.headers.get('Access-Control-Allow-Origin') == '*'

    resp = response.json()

    assert resp["id"] == "osm:way:63178753"
    assert resp["name"] == "Musée d'Orsay"
    assert resp["local_name"] == "Musée d'Orsay"
    assert resp["class_name"] == "museum"
    assert resp["subclass_name"] == "museum"
    assert resp["blocks"][0]["type"] == "opening_hours"
    assert len(resp["blocks"]) == 1 # it contains only the block opening hours

def test_wrong_verbosity():
    client = TestClient(app)

    response = client.get(
        url=f'http://localhost/v1/places/osm:way:63178753?lang=fr&verbosity=shoooooort',
    )
    assert response.status_code == 400
    assert response._content == b'{"message":"verbosity shoooooort does not belong to the set of possible verbosity values=[\'long\', \'short\']"}'
