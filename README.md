# simple_query_build

Builds SQL queries from two main classes: `Filter` and `Query`.

They ended up looking too repetitive throughout the code so
I decided to define the aliases `f` and `q` to them, respectively.

<!-- Note: This is not meant to disrupt the SQL way of building queries, but to
ensure an easy, safe and bug free way of sanitizing and object-mapping,
to deviver it in various flavors using Python. -->

## Here's how to use it

Creating simple criteria:

```python
filter = f.equals('column_name', 'some_value')
print(filter.dump_parts())
# Output:
#     column_name = 'some_value'
```

Composed criteria:

```python
filter = (f()
          .add(f.create('colmun_bool', 'is', False))
          .add_or(f.create('another_column_bool', 'is_not', True)))
print(filter.dump_parts())
# Output:
#     colmun_bool IS FALSE OR another_column_bool IS NOT TRUE
```

They can be nested:

```python
filter = (f()
          .add(f.create('colmun_bool', 'is', False))
          .add_or(f.create('another_column_bool', 'is_not', True))
          .add_or(f()
                  .add(f.equals('some_number', 100))
                  .add(f.like('some_text', '%to match%'))
                  .wrap_it()))
print(filter.dump_parts())
# Output:
#     colmun_bool IS FALSE OR another_column_bool IS NOT TRUE OR
#     (some_number = 100 AND some_text LIKE '%to match%')
```

Create an `INSERT` statement:

```python
query = (q("insert")
         .entity("users")
         .set_data({
             "name": "name",
             "email": "email"
         }))
print(query.dump())
# Output:
#     INSERT INTO users (name, email) VALUES ('name', 'email');
```

Create an `UPDATE` statement:

```python
query = (q("update")
         .entity("users")
         .set_data({"name": "new name", })
         .filter(f.equals("id", 1)))
print(query.dump())
# Output:
#     UPDATE users SET name = 'new name' WHERE id = 1;
```

Create a `DELETE` statement:

```python
query = (q("delete")
         .entity("users")
         .filter(f.equals("id", 1)))
print(query.dump())
# Output:
#     DELETE FROM users WHERE id = 1;
```

Create a `SELECT` statement:

```python
query = (q("select")
         .entity("users")
         .set_columns(["name",])
         .filter(f().limit(5)))
print(query.dump())
# Output:
#     SELECT name FROM users LIMIT 5;
```
