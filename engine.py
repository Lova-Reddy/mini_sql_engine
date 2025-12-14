import csv
import os

def load_data(filename):
    """Loads CSV data into a list of dictionaries."""
    if not filename.endswith('.csv'):
        filename += '.csv'
        
    if not os.path.exists(filename):
        raise FileNotFoundError(f"Table '{filename}' not found.")

    with open(filename, mode='r', newline='') as f:
        reader = csv.DictReader(f)
        return list(reader)

def evaluate_condition(row, condition):
    """
    Evaluates a WHERE condition against a row.
    Supports: =, !=, >, <, >=, <=
    """
    if not condition:
        return True

    # Simple parser for condition: e.g., "age > 20"
    ops = ['>=', '<=', '!=', '=', '>', '<']
    operator = None
    
    for op in ops:
        if op in condition:
            operator = op
            break
            
    if not operator:
        raise ValueError("Invalid operator in WHERE clause")

    col, val = condition.split(operator, 1)
    col = col.strip()
    val = val.strip()

    # Get row value
    if col not in row:
        raise ValueError(f"Column '{col}' does not exist")
        
    row_val = row[col]

    # Type conversion (attempt to compare as numbers if possible)
    try:
        row_val = float(row_val)
        val = float(val)
    except ValueError:
        # Keep as strings, remove quotes if present
        val = val.strip("'").strip('"')

    if operator == '=': return row_val == val
    if operator == '!=': return row_val != val
    if operator == '>': return row_val > val
    if operator == '<': return row_val < val
    if operator == '>=': return row_val >= val
    if operator == '<=': return row_val <= val
    
    return False

def execute(parsed_query):
    # 1. Load Data (FROM)
    data = load_data(parsed_query['table'])
    
    # 2. Filter Data (WHERE)
    if parsed_query['condition']:
        data = [row for row in data if evaluate_condition(row, parsed_query['condition'])]
        
    # 3. Aggregation (COUNT)
    # Check if any column is a COUNT aggregation
    # The requirement asks to support COUNT(*) and COUNT(column) 
    is_count = False
    for col in parsed_query['columns']:
        if col.lower().startswith("count("):
            is_count = True
            break
            
    if is_count:
        return [{"COUNT": len(data)}]

    # 4. Projection (SELECT)
    # If columns is ["*"], return all data
    if parsed_query['columns'] == ['*']:
        return data
        
    # Otherwise select specific columns
    result = []
    for row in data:
        new_row = {}
        for col in parsed_query['columns']:
            if col in row:
                new_row[col] = row[col]
            else:
                raise ValueError(f"Column '{col}' not found")
        result.append(new_row)
        
    return result