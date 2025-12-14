import parser
import engine
import sys

def print_table(data):
    """Helper to print list of dicts as a table."""
    if not data:
        print("No results found.")
        return
        
    # Get headers
    headers = list(data[0].keys())
    
    # Print headers
    print(" | ".join(headers))
    print("-" * (len(headers) * 10))
    
    # Print rows
    for row in data:
        print(" | ".join(str(row[col]) for col in headers))
    print(f"\n({len(data)} rows)\n")

def main():
    print("Mini SQL Engine Started.")
    print("Type 'exit' or 'quit' to stop.")
    
    while True:
        try:
            # Get input
            query = input("sql> ")
            
            # Check exit condition
            if query.lower() in ['exit', 'quit']:
                break
                
            # Parse
            parsed = parser.parse_query(query)
            
            # Execute
            result = engine.execute(parsed)
            
            # Print
            print_table(result)
            
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()