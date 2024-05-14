SQL_GENERATION_PROMPT = """
Based on the table metadata and schema generate a sql query to answer the user question
TableName:
TableName: details
Description: Contains all details regarding the restaurants and restaurant menu
Columns:
restaurantname: Name of restaurants
item_type: Categories the item [Starters, Main Course, Desserts]
item_name: Name of item
description: Description regarding the item
ingredients: Ingredients of each item. Always lowercase this column values while querying.
cost: Cost of each item in $
preparation_time: Time taken to prepare each item in minutes
veg_non_veg: Specifies if the dish is veg or non veg[veg, non-veg]

Schema:
create table details(
restaurantname VARCHAR(255),
item_type VARCHAR(50),
item_name VARCHAR(255),
description TEXT,
ingredients TEXT,
cost DOUBLE,
preparation_time INT,
veg_non_veg VARCHAR(50)
);

<<Example 1>>
User Query: What are the restaurants in my area

Response:
SELECT distinct restaurantname FROM details

<<Example 2>>
User Query: What is the menu for the restaurant Bistro Fusion?
    
Response:
SELECT * FROM details
WHERE  lower(restaurantname) like "%bistro fusion%"

<<Example 3>>
User Query: {input}

Response:
"""
