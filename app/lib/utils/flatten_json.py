def flatten_json(input_json):
    result = {}

    # Raise a TypeError if input_json is None
    if input_json is None:
        raise TypeError("input_json cannot be None")

    # Helper function to traverse and flatten the JSON
    def traverse(current, parent_key: str):
        if isinstance(current, dict):
            for key, value in current.items():
                traverse(value, f"{parent_key}/{key}".strip())
        elif isinstance(current, int):
            # When an integer is reached, store it in the result
            parent_key_parts = parent_key.split("/")
            if len(parent_key_parts) >= 2:
                category = parent_key_parts[0]  # e.g., "short" or "tall"
                # get the last part as the street name
                street_name = parent_key_parts[-1]
                result.setdefault(category, {})[street_name] = current

    # Start traversal
    for main_key, sub_json in input_json.items():
        traverse(sub_json, main_key)

    return result