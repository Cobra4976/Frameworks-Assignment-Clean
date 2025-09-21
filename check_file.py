import os
import pandas as pd

# Check current directory
print("Current working directory:", os.getcwd())
print("Files in current directory:", os.listdir('.'))

# Check if metadata.csv exists
filename = 'metadata.csv'
if os.path.exists(filename):
    print(f"✅ {filename} found!")
    
    # Check file permissions
    print(f"File size: {os.path.getsize(filename):,} bytes")
    print(f"Readable: {os.access(filename, os.R_OK)}")
    print(f"Writable: {os.access(filename, os.W_OK)}")
    
    # Try to open just the first few lines
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            first_line = f.readline()
            print("✅ File can be opened!")
            print(f"First line preview: {first_line[:100]}...")
    except Exception as e:
        print(f"❌ Cannot open file: {e}")
        
    # Try pandas read with small sample
    try:
        df_test = pd.read_csv(filename, nrows=5)
        print("✅ Pandas can read the file!")
        print(f"Columns: {list(df_test.columns)}")
    except Exception as e:
        print(f"❌ Pandas cannot read file: {e}")
        
else:
    print(f"❌ {filename} not found in current directory")
    print("Available CSV files:", [f for f in os.listdir('.') if f.endswith('.csv')])