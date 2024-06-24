import json
import requests

import upload.credentials as credentials


def load_template_rc(file="test/data/template-crate.json"):
    with open(file) as f:
        rc = json.load(f)
    return rc


def set_field_in_template_rde(field, value, rc, rde_id="./"):
    graph = rc.get("@graph")
    for i, entity in enumerate(graph):
        if entity["@id"] == rde_id:
            break

    rc["@graph"][i][field] = value
    return rc, i


def add_entity_to_template(entity, rc):
    rc["@graph"].append(entity)
    return rc


def get_single_mapping(mapping_class, rule, mapping_file_name="mapping/mapping.json"):
    mapping_file = open(mapping_file_name)
    m = json.load(mapping_file)

    if not mapping_class.endswith("_mapping"):
        mapping_class += "_mapping"

    rule = m["$root"][mapping_class]["mappings"][rule]

    return rule


def get_mapping_class(mapping_class, mapping_file_name="mapping/mapping.json"):
    mapping_file = open(mapping_file_name)
    m = json.load(mapping_file)

    if not mapping_class.endswith("_mapping"):
        mapping_class += "_mapping"

    mapping_class = m["$root"][mapping_class]

    return mapping_class


def get_request_headers():
    api_key = credentials.get_api_key()
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }
    return headers


def fetch_inveniordm_record(record_id):
    api_url = credentials.get_repository_base_url()
    r = requests.get(
        f"{api_url}/api/deposit/depositions/{record_id}",
        headers=get_request_headers(),
    )
    r.raise_for_status()
    return r.json()
