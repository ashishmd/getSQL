# getSQL

It is a service to generate MySQL queries based on the select columns and where conditions passed as params of API request.

In most of the cases, other than developers, no other people in a software company knows MySQL. Let it be be a person from from marketing team or from sales team, they often wants to take stats from the DB. For that they have to come to developers and ask them to write a query as per the requirements.

This service gives the option to generate query as per requirement without intervention of developers in such scenarios. 

Requirements:
* Python - 3.7.2
* Django - 2.17
* django-mysql - 3.0.0.post1
* mysql-connector-python - 8.0.15     
* mysqlclient - 1.4.2.post1

## Usage:
You will have to import data of your MySQL Database: 
```
1. Tables (Table Name, Alias)
2. Columns (Column Name, Table Name, is_primary, is_indexed, Foreign Key Column Name, Foreign key Table Name)
3. Relations (Table 1, Table 2, Relation type [has_one, belongs_to, has_many])
```

System will consume the JSONString as a param in API Request. 

```python
{
  "select_fields": [ "Students.Name", "Students.*", "*"],
  "where_conditions": {
    "where_clauses": [
      {
        "primary_value": "Students.JobTitle",
        "primary_type": "column",
        "operator": "=",
        "secondary_value": "CEO",
        "secondary_type": "string",
        "id": 1
      },
      {
        "primary_value": "Schools.Name",
        "primary_type": "column",
        "operator": "=",
        "secondary_value": "CEO",
        "secondary_type": "string",
        "id": 1
      }
    ],
    "where_clause_type": "or",
    "skip_data_presence_check": false,
    "skip_data_presence_tables": ["Students, Schools"]
  } 
}
```

If all params are valid, System will generate a query by automatically making the `JOINS` and give you the resultant query. Based on the number of paths (flow of relationships from one table to others), you can get multiple queries in result.
