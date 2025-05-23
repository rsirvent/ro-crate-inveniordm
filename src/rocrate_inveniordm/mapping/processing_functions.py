def dateProcessing(value):
    from dateutil.parser import parse

    if not value:
        return None

    if len(value) == 4:
        # only year
        return value

    fuzzy_date = parse(value, fuzzy=True)
    if not fuzzy_date:
        print("Warning: Date {date} could not be parsed.")
        return None
    return fuzzy_date.strftime("%Y-%m-%d")


def geonamesProcessing(value):
    # map the geonmames url to the geonames id
    # example: "http://sws.geonames.org/8152662/"
    if not value:
        return None
    if not value.startswith("http://sws.geonames.org/"):
        # not a geonnames url
        return None

    replaced_url = value.replace("http://sws.geonames.org/", "")
    replaced_url = replaced_url.replace("/", "")
    return replaced_url


def doi_processing(value):
    # check if value is doi format
    # example: "https://doi.org/10.4225/59/59672c09f4a4b"
    if not value:
        return None

    if not value.startswith("https://doi.org/"):
        return None

    replaced_url = value.replace("https://doi.org/", "")
    return replaced_url


def orcidProcessing(value):
    if not value:
        return None

    if not value.startswith("https://orcid.org/"):
        return None

    replaced_url = value.replace("https://orcid.org/", "")
    return replaced_url


def authorProcessing(value):
    if value == "Person":
        return "personal"
    elif value == "Organization":
        return "organizational"
    else:
        return None


def ISO8601Processing(value):
    return "ABC"


def embargoDateProcessing(value):
    """
    Parses the date and returns it in the format YYYY-MM-DD.
    """
    from dateutil.parser import parse

    if value is None:
        return None
    fuzzy_date = parse(value, fuzzy=True)
    if not fuzzy_date:
        print("Warning: Date {date} could not be parsed.")
        return None
    return fuzzy_date.strftime("%Y-%m-%d")


def convert_to_iso_639_3(value):
    """
    Converts the value to a valid ISO-639-3 language code
    """
    import iso639

    if value is None:
        return None
    try:
        language = iso639.Language.match(value)
        code = language.part3
    except iso639.language.LanguageNotFoundError:
        return None

    return code


def typeProcessing(value):
    """
    Checks if the 'mainEntity' type includes 'ComputationalWorkflow'
    """
    if "ComputationalWorkflow" in value:
        return "workflow"
    return "dataset"


def nameProcessing(value):
    """
    family_name is mandatory in Zenodo. Does not overwrite familyName and givenName
    from the RO-Crate if they are provided
    """
    new_name = {}
    parts = value.strip().split()
    new_name["family_name"] = parts[-1] if len(parts) > 0 else ""
    new_name["given_name"] = " ".join(parts[:-1]) if len(parts) > 1 else ""

    return new_name
