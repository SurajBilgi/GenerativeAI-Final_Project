SQL_GENERATION_PROMPT = """
Based on the table metadata and schema generate a sql query to answer the user question
MetaData:
TableName: name
Description: Contains the name for each restaurant in the  area of the user
Columns:
id: contains unique id for each restaurant
name: contains name of restaurant

TableName:
TableName: details
Description: Contains all details regarding the restaurants menu
Columns:
restaurant_id: Foreign key that links this table with table `name`
item_type: Categories the item [Starters, Main Course, Desserts]
item_name: Name of item
description: Description regarding the item
ingredients: Ingredients of each item. Always lowercase this column values while querying.
cost: Cost of each item in $
preparation_time: Time taken to prepare each item in minutes

Schema:
create table restaurants.name(
    id int,
    name VARCHAR(255)
);

create table restaurants.details(
restaurant_id int,
item_type VARCHAR(50),
item_name VARCHAR(255),
description TEXT,
ingredients TEXT,
cost double,
preparation_time int
);

<<Example 1>>
User Query: What are the restaurants in my area

Response:
SELECT * FROM restaurants.name

<<Example 2>>
User Query: What is the menu for the restaurant Bistro Fusion?
    
Response:
SELECT * FROM restaurants.details
WHERE restaurant_id in (SELECT id FROM name WHERE lower(name) like "%bistro fusion%")

<<Example 3>>
User Query: {input}

Response:
"""
