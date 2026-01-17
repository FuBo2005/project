def filter_strings(filter_func, string_array):
    """
    Function to filter an array of strings using a lambda function.
    
    Arguments:
    filter_func (function): Lambda function for filtering
    string_array (list): Array of strings to filter
    
    Returns:
    list: Filtered array of strings
    """
    return [s for s in string_array if filter_func(s)]


def main():
    """
    Main function to demonstrate the filtering.
    """
    # Test array of English words/phrases (4-5 examples)
    test_array = [
        "apple",
        "an orange",
        "banana",
        "test",
        "avocado"
    ]
    
    print("Original array of strings:")
    for s in test_array:
        print(f"  '{s}'")
    print()
    
    # 1. Exclude strings with spaces
    print("1. Strings without spaces:")
    no_spaces = filter_strings(lambda x: ' ' not in x, test_array)
    for s in no_spaces:
        print(f"  '{s}'")
    print()
    
    # 2. Exclude strings starting with the letter "a"
    print("2. Strings not starting with 'a':")
    no_a_start = filter_strings(lambda x: not x.lower().startswith('a'), test_array)
    for s in no_a_start:
        print(f"  '{s}'")
    print()
    
    # 3. Exclude strings shorter than 5 characters
    print("3. Strings with length at least 5 characters:")
    min_length_5 = filter_strings(lambda x: len(x) >= 5, test_array)
    for s in min_length_5:
        print(f"  '{s}'")


if __name__ == "__main__":
    main()