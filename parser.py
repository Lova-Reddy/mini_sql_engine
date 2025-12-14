def parse_query(query):
    """
    Parses a simple SQL query into its components.
    Supported Grammar: SELECT [columns] FROM [table] WHERE [condition]
    """
    # Normalize query: remove extra whitespace and ensure consistent casing for keywords
    query = query.strip()
    
    # 1. basic validation
    if not query.lower().startswith("select"):
        raise ValueError("Query must start with SELECT")
        
    # 2. Split by keywords to isolate parts
    # We use a simple strategy: split by ' FROM ' and ' WHERE '
    
    # meaningful parts
    select_part = ""
    from_part = ""
    where_part = None

    # Find the indices of keywords
    lower_q = query.lower()
    idx_from = lower_q.find(" from ")
    idx_where = lower_q.find(" where ")

    # Extract SELECT part
    if idx_from != -1:
        select_part = query[7:idx_from].strip() # 7 is len("SELECT ")
    else:
        raise ValueError("Query must contain FROM clause")

    # Extract FROM and WHERE parts
    if idx_where != -1:
        # WHERE clause exists
        from_part = query[idx_from + 6 : idx_where].strip()
        where_part = query[idx_where + 7 :].strip()
    else:
        # No WHERE clause
        from_part = query[idx_from + 6 :].strip()

    return {
        "columns": [c.strip() for c in select_part.split(",")],
        "table": from_part,
        "condition": where_part
    }