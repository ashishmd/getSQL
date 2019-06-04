# getSQL

It is a service to generate MySQL queries based on the select columns and where conditions passed as params of API request.

In most of the cases, other than developers, no other people in a software company knows MySQL. Let it be be a person from from marketing team or from sales team, they often wants to take stats from the DB. For that they have to come to developers and ask them to write a query as per the requirements.

This service gives the option to generate query as per requirement without intervention of developers in such scenarios. 

Requirements:
* Python - 3.7.2
* Django - 2.17
* django-mysql - 3.0.0
* mysql-connector-python - 8.0.15     
* mysqlclient - 1.4.2

## Usage:
You will have to import data of your MySQL Database: (Support will be added soon to import)
```
1. Tables (Table Name, Alias)
2. Columns (Column Name, Table Name, is_primary, is_indexed, Foreign Key Column Name, Foreign key Table Name)
3. Relations (Table 1, Table 2, Relation type [has_one, belongs_to, has_many])
```

### Generate SQL API Format:
```buildoutcfg
curl --request POST \
  --url http://127.0.0.1:8000/generate_query \
  --header 'authorization: Basic YXNoaXNobTphc2hpc2hAMTIz' \
  --header 'content-type: multipart/form-data; boundary=---011000010111000001101001' \
  --header 'cookie: csrftoken=54pjTJyOr4x36PqKRKlmYLhgwWcaFVm2IUSn5YpUNkUfBQjxLYXx4lQhYPLmuBK8; sessionid=fydp236dubrv48r550w0pk412qnftnt4' \
  --header 'x-csrftoken: 54pjTJyOr4x36PqKRKlmYLhgwWcaFVm2IUSn5YpUNkUfBQjxLYXx4lQhYPLmuBK8' \
  --cookie 'csrftoken=54pjTJyOr4x36PqKRKlmYLhgwWcaFVm2IUSn5YpUNkUfBQjxLYXx4lQhYPLmuBK8; sessionid=fydp236dubrv48r550w0pk412qnftnt4' \
  --form 'JSONString={
  "select_fields": [ "Contacts.Name", "Contacts.*", "*", "IndustryTypes.Name"],
  "where_conditions": {
    "where_clauses": [
    	{
        "primary_value": "Contacts.Name",
        "primary_type": "column",
        "operator": "=",
        "secondary_value": "CEO",
        "secondary_type": "string",
        "id": 1
      },
      {
        "primary_value": "Contacts.JobTitle",
        "primary_type": "column",
        "operator": "=",
        "secondary_value": "CEO",
        "secondary_type": "string",
        "id": 2
      },
      {
        "primary_value": "SalesAccounts.Name",
        "primary_type": "column",
        "operator": "=",
        "secondary_value": "CEO",
        "secondary_type": "string",
        "id": 3
      }
    ],
    "where_clause_type": "custom",
    "custom_conditions": "(#1 and #2 ) or #3",
    "skip_data_presence_check": true,
    "skip_data_presence_tables": ["SalesAccounts"]
  } 
}'
```
### Generate SQL API Params:
System will consume the following JSONString as a param in API Request. 

```python
{
  "select_fields": [ "Students.Name", "Students.*", "*", "IndustryTypes.Name"],
  "where_conditions": {
    "where_clauses": [
    	{
        "primary_value": "Students.Name",
        "primary_type": "column",
        "operator": "=",
        "secondary_value": "CEO",
        "secondary_type": "string",
        "id": 1
      },
      {
        "primary_value": "Students.JobTitle",
        "primary_type": "column",
        "operator": "=",
        "secondary_value": "CEO",
        "secondary_type": "string",
        "id": 2
      },
      {
        "primary_value": "Schools.Name",
        "primary_type": "column",
        "operator": "=",
        "secondary_value": "CEO",
        "secondary_type": "string",
        "id": 3
      }
    ],
    "where_clause_type": "custom",
    "custom_conditions": "(#1 and #2 ) or #3",
    "skip_data_presence_check": true,
    "skip_data_presence_tables": ["Schools"]
  } 
}
```
#### select_fields
Array of columns that you want to get from DB. Columns should be in the format <table_name>.<column_name>
#### where_conditions
It contains where_clauses, where_clause_type, skip_data_presence_check, skip_data_presence_tables
#### where_clauses
primary_value , primary_type, operator, secondary_value, secondary_type.
primary_value and secondary_value can be a column or value. Its type is specified in the repective type params.
id param will be used once the custom where_clause_type is supported.
#### where_clause_type
Values can be "and" / "or" / "custom". System will use it to append and / or conditions in all where clause.
#### custom_conditions 
To process custom where_conditions, pass where_clause_type as "custom". Then you can specify id values of where clause in a format like "((#1 and #2) or #3)"
. Where condition will be formed as per the custom condition given.  
#### skip_data_presence_check
If this variable is set true, only LEFT JOINS will be used in the query. 
#### skip_data_presence_tables
If skip_data_presence_check is set as false, you can specify tables for which you want to use left joins.

### Result
If all params are valid, System will generate a query by automatically making the `JOINS` and give you the resultant query. Based on the number of paths (flow of relationships from one table to others), you can get multiple queries in result.
