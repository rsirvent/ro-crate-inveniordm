import json
from mapping.converter import (
    rc_get_rde,
    apply_mapping,
    setup_dc,
    get_arrays_from_from_values,
    get_mapping_paths,
)
from test.unit.utils import (
    add_entity_to_template,
    load_template_rc,
    set_field_in_template_rde,
    get_single_mapping,
)

publisher_string = "Test University"
publisher_entity = {
    "@id": "https://ror.org/0abcdef00",
    "@type": "Organization",
    "name": "Example University",
    "url": "https://www.example.org",
}


def test_publisher_string():
    rc = load_template_rc()
    rc, _ = set_field_in_template_rde("publisher", publisher_string, rc)
    rule_name = "publisher_mapping_1"
    rule = get_single_mapping("publisher", rule_name)
    paths = get_mapping_paths(rc, {rule_name: rule})
    dc = setup_dc()

    dc, _ = apply_mapping(rule, paths, rc, dc)

    print(dc)
    assert dc["metadata"]["publisher"] == publisher_string


def test_publisher_entity():
    rc = load_template_rc()
    rc = add_entity_to_template(publisher_entity, rc)
    rc, _ = set_field_in_template_rde("publisher", {"@id": publisher_entity["@id"]}, rc)
    dc = setup_dc()
    rule_name = "publisher_mapping_1"
    rule = get_single_mapping("publisher", rule_name)
    paths = get_mapping_paths(rc, {rule_name: rule})

    dc, _ = apply_mapping(rule, paths, rc, dc)

    print(dc)
    assert dc["metadata"]["publisher"] == publisher_entity["name"]
