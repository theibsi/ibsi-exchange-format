import copy


def flatten_yaml_dict(x):
    """
    Flattens complicated, nested concept structures into a flat list of concept elements. For example,
    features can be divided into features sets, which may have shared attributes. This is very friendly for reading
    and updating by humans, but hard for machine processing. This function helps create a single unified structure,
    consisting of a list of dictionary objects for each concept.
    :param x: dict extracted from a yaml file
    :return: dict
    """

    def _extract_concept(x, concept: str, uid: str, shared_attributes: dict | None = None):
        # This is a recursive generator which steps through a yaml dictionary and flattens everything.
        if isinstance(x, list):
            # List of concepts.
            for list_object in x:
                yield from _extract_concept(list_object, concept, uid, shared_attributes=shared_attributes)

        elif isinstance(x, dict):
            # Name or uid should always be specified
            if "name" in x or uid in x:
                # Single concept. If specified, any shared attributes should be added to the current
                concept_element = copy.deepcopy(x)
                if shared_attributes is not None:
                    concept_element.update(shared_attributes)

                yield concept_element

            elif concept in x:
                # Nested concepts, potentially with shared attributes.
                if "shared-attributes" in x:
                    shared_attributes = x["shared-attributes"]
                yield from _extract_concept(x[concept], concept, uid, shared_attributes=shared_attributes)

            elif len(x) == 1:
                # Set of concepts with a trivial name (key).
                for _, value in x.items():
                    yield from _extract_concept(value, concept, uid, shared_attributes=shared_attributes)
            else:
                raise TypeError("dict or list is expected.")
        else:
            raise TypeError("dict or list is expected.")

    # Principle of least astonishment requires that we don't update x by reference.
    y = copy.deepcopy(x)

    # Main concepts and their uid-attributes.
    concepts = [
        ("imaging", "image-uid"),
        ("mask", "mask-uid"),
        ("image-processing", "image-processing-uid"),
        ("image-filters", "image-filter-uid"),
        ("features", "feature-uid"),
        ("models", "model-uid")
    ]

    # Iterate over the main concepts.
    for concept_name, concept_uid in concepts:
        if concept_name not in x:
            continue

        # Update the concept with a list of flattened concept elements.
        y[concept_name] = list(_extract_concept(
            x[concept_name],
            concept=concept_name,
            uid=concept_uid
        ))

    return y
