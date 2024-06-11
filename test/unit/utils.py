import json
from mapping.converter import (
    rc_get_rde,
    apply_mapping,
    setup_dc,
    get_arrays_from_from_values,
    get_paths,
)


def load_template_rc(file="test/unit/template-crate.json"):
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
