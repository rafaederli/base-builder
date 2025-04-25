import pandas as pd

# Load 'sales.txt' file into a DataFrame
df = pd.read_csv("sales.txt")

# Create a 'date' column by combining 'year', 'month', and 'day' columns, and convert it to datetime
df["date"] = pd.to_datetime({"year": df["year"], "month": df["month"], "day": df["day"]})

# Set a 'date' column as the DateFrame index
df.set_index(df["date"], inplace=True)

def normalize_category_1(row):
    """
    Update the value of the 'category_1' column based on the value of the 'category_0' column.
    If 'category_0' is 'cat_1', then 'category_1' will be updated to 'cat_1'.
    If 'category_0' is 'cat_2', then 'category_1' will be updated to 'cat_2'.
    If 'category_0' is 'cat_3', then 'category_1' will be updated to 'cat_3'.
    Otherwise, 'category_1' retains its original value.

    Parameters:
    row (pd.Series): A row from DataFrame containing the columns 'category_0' and 'category_1'.

    Returns:
    str: The updated value for category_1.
    """
    # Checks the value of 'category_0' and updates 'category_1' accordingly
    if row("category_0") == "cat_1":
        return "cat_1"
    elif row("category_0") == "cat_2":
        return "cat_2"
    elif row("category_0") == "cat_3":
        return "cat_3"
    else:
        # If 'category_0' is none of the above, 'category_1' retains its original value
        return row["category_1"]

# Apply the 'normalize_category_1' function to update the 'category_1' column
df["category_1"] = df.apply(normalize_category_1, axis=1)

# Load the mapping tables for 'category_2' and 'category_3' from the 'maps.xlsx' file
category_2_mapping_dataFrame = pd.read_excel("maps.xlsx", sheet_name="category_1_category_2")
category_3_mapping_dataFrame = pd.read_excel("maps.xlsx", sheet_name="category_1_category_3")

# Create a mapping dictionary for 'category_2' and 'category_3'
category_2_mapping_dictionary = {(row["category_1"], row["category_2"]): row["new_category_2"] for _, row in category_2_mapping_dataFrame.iterrows()}
category_3_mapping_dictionary = {(row["category_1"], row["category_3"]): row["new_category_3"] for _, row in category_3_mapping_dataFrame.iterrows()}

def normalize(row, column, dictionary):
    """
    Updates the value of the specified column based on a mapping file.

    Parameters:
    row (pd.Series): A row from the DataFrame containing the columns 'category_1' and the specified column.
    column (str): The name of the column to be updated.
    dictionary (dict): A mapping dictionary where the key is a tuple (category_1 value, specified column value) and the value is the updated value.

    Returns:
    str: The updated value for the specified column.
    """
    # Returns the mapped value from the dictionary, using the tuple (category_1, column value) as the key
    # If no mapping is found, returns 'NA' as a default
    return dictionary.get((row["category_1"], row[column], "NA"))

# Apply the 'normalize' function to update the 'category_2' and 'category_3' columns with the mappings
df["category_2"] = df.apply(lambda row: normalize(row, "category_2", category_2_mapping_dictionary), axis=1)
df["category_3"] = df.apply(lambda row: normalize(row, "category_3", category_3_mapping_dictionary), axis=1)
