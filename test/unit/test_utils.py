from test.unit.utils import (
    add_entity_to_template,
    load_template_rc,
    set_field_in_template_rde,
    get_single_mapping,
    get_mapping_class,
)


def test_load_template_rc():
    rc = load_template_rc()

    assert "@context" in rc
    assert "@graph" in rc
    assert len(rc["@graph"]) == 2
    assert rc["@graph"][0]["@id"] == "ro-crate-metadata.json"
    assert rc["@graph"][1]["@id"] == "./"


def test_set_field_in_template_rde():
    rc = load_template_rc()
    name = "Test name"

    out, index = set_field_in_template_rde("name", name, rc)

    assert len(out["@graph"]) == 2
    assert out["@graph"][index]["@id"] == "./"
    assert out["@graph"][index]["name"] == name


def test_add_entity_to_template():
    rc = load_template_rc()
    entity = {
        "@id": "https://orcid.org/0000-0000-0000-0000",
        "@type": "Person",
        "name": "Jane Smith",
    }

    out = add_entity_to_template(entity, rc)

    assert len(out["@graph"]) == 3
    assert out["@graph"][-1] == entity


def test_get_single_mapping():
    out = get_single_mapping("title", "name_mapping")
    expected = {"from": "name", "to": "metadata.title"}

    assert out == expected


def test_get_mapping_class():
    out = get_mapping_class("title")
    expected = {
        "mappings": {
            "name_mapping_additional_fallback": {
                "from": "@alternativeName",
                "to": "metadata.title",
            },
            "name_mapping": {"from": "name", "to": "metadata.title"},
        },
        "ifNonePresent": {"metadata.title": ":unkn"},
    }

    assert out == expected
