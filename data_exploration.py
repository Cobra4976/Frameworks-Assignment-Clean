# CORD-19 Data Exploration Script
# Step 1: Loading and Basic Exploration

import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

print("🔬 CORD-19 Data Analysis - Step 1: Data Loading and Exploration")
print("=" * 60)

# Step 1.1: Load the data with flexible path checking
print("📥 Loading the dataset...")

# Try to load from Desktop first
desktop_path = os.path.expanduser('~/Desktop/metadata.csv')
current_path =  r'C:\Users\USER\Desktop'

try:
    if os.path.exists(desktop_path):
        df = pd.read_csv(desktop_path)
        print(f"✅ Loaded from Desktop: {len(df):,} records")
    elif os.path.exists(current_path):
        df = pd.read_csv(current_path)
        print(f"✅ Loaded from current directory: {len(df):,} records")
    else:
        print("❌ metadata.csv not found in Desktop or current directory")
        print("📍 Checking other common locations...")
        
        # Check other common locations
        other_paths = [
            os.path.expanduser('~/Documents/metadata.csv'),
            os.path.expanduser('~/Downloads/metadata.csv'),
            './data/metadata.csv'
        ]
        
        file_found = False
        for path in other_paths:
            if os.path.exists(path):
                df = pd.read_csv(path)
                print(f"✅ Found and loaded from: {path}")
                print(f"✅ Records loaded: {len(df):,}")
                file_found = True
                break
        
        if not file_found:
            print("❌ metadata.csv not found in any common location")
            print("📋 Please place metadata.csv in one of these locations:")
            print("   • Desktop: ~/Desktop/metadata.csv")
            print("   • Current folder: ./metadata.csv")
            print("   • Documents: ~/Documents/metadata.csv")
            print("   • Downloads: ~/Downloads/metadata.csv")
            print("\n🔗 Download from: https://www.kaggle.com/datasets/allen-institute-for-ai/CORD-19-research-challenge")
            exit()
            
except PermissionError:
    print("❌ Permission denied. Try these solutions:")
    print("1. Close Excel or any program that has the file open")
    print("2. Move the file to your Desktop")
    print("3. Run as administrator (Windows)")
    print("4. Check file permissions")
    exit()
except Exception as e:
    print(f"❌ Error loading file: {e}")
    print("💡 Make sure the file is a valid CSV file")
    exit()

# If dataset is too large, work with a sample
if len(df) > 100000:
    print(f"📊 Dataset is large ({len(df):,} rows). Taking a sample of 50,000 rows for analysis...")
    df = df.sample(n=50000, random_state=42).reset_index(drop=True)
    print(f"✅ Working with {len(df):,} sampled records")

print("\n" + "="*60)
print("🔍 BASIC DATA EXPLORATION")
print("="*60)

# Step 1.2: Examine the first few rows
print("\n📋 First 5 rows of the dataset:")
print("-" * 40)
print(df.head())

# Step 1.3: Check DataFrame dimensions and structure
print(f"\n📊 Dataset Dimensions:")
print(f"   Rows: {df.shape[0]:,}")
print(f"   Columns: {df.shape[1]:,}")

print(f"\n📝 Column Names:")
for i, col in enumerate(df.columns, 1):
    print(f"   {i:2d}. {col}")

# Step 1.4: Data types
print(f"\n🏷️  Data Types:")
print("-" * 30)
data_types = df.dtypes.value_counts()
for dtype, count in data_types.items():
    print(f"   {dtype}: {count} columns")

print(f"\n📋 Detailed Column Information:")
print("-" * 40)
info_df = pd.DataFrame({
    'Column': df.columns,
    'Non-Null Count': df.count(),
    'Null Count': df.isnull().sum(),
    'Null Percentage': (df.isnull().sum() / len(df) * 100).round(2),
    'Data Type': df.dtypes
})
print(info_df.to_string(index=False))

# Step 1.5: Basic statistics for important columns
print(f"\n📈 KEY INSIGHTS:")
print("-" * 20)

# Check date range if publish_time exists
if 'publish_time' in df.columns:
    # Convert publish_time to datetime, handling errors
    df['publish_time'] = pd.to_datetime(df['publish_time'], errors='coerce')
    valid_dates = df['publish_time'].dropna()
    
    if len(valid_dates) > 0:
        print(f"   📅 Date Range: {valid_dates.min().strftime('%Y-%m-%d')} to {valid_dates.max().strftime('%Y-%m-%d')}")
        print(f"   📅 Papers with valid dates: {len(valid_dates):,} ({len(valid_dates)/len(df)*100:.1f}%)")
    else:
        print("   📅 No valid dates found in publish_time column")
else:
    print("   📅 No publish_time column found")

# Check title and abstract availability
if 'title' in df.columns:
    titles_available = df['title'].notna().sum()
    print(f"   📖 Papers with titles: {titles_available:,} ({titles_available/len(df)*100:.1f}%)")
else:
    print("   📖 No title column found")

if 'abstract' in df.columns:
    abstracts_available = df['abstract'].notna().sum()
    print(f"   📄 Papers with abstracts: {abstracts_available:,} ({abstracts_available/len(df)*100:.1f}%)")
else:
    print("   📄 No abstract column found")

# Check journal information
if 'journal' in df.columns:
    unique_journals = df['journal'].nunique()
    print(f"   📰 Unique journals: {unique_journals:,}")
else:
    print("   📰 No journal column found")

# Check authors
if 'authors' in df.columns:
    papers_with_authors = df['authors'].notna().sum()
    print(f"   👥 Papers with author info: {papers_with_authors:,} ({papers_with_authors/len(df)*100:.1f}%)")
else:
    print("   👥 No authors column found")

print(f"\n🎯 MISSING DATA ANALYSIS:")
print("-" * 30)
missing_data = df.isnull().sum().sort_values(ascending=False)
missing_data = missing_data[missing_data > 0]

if len(missing_data) > 0:
    print("   Top columns with missing data:")
    for col, missing_count in missing_data.head(10).items():
        percentage = (missing_count / len(df)) * 100
        print(f"   • {col}: {missing_count:,} ({percentage:.1f}%)")
else:
    print("   ✅ No missing data found!")

# Step 1.6: Sample of actual data
print(f"\n📝 SAMPLE DATA PREVIEW:")
print("-" * 30)
sample_cols = ['title', 'publish_time', 'journal', 'authors']
available_cols = [col for col in sample_cols if col in df.columns]

if available_cols:
    sample_df = df[available_cols].head(3)
    for idx, row in sample_df.iterrows():
        print(f"\n   Paper {idx + 1}:")
        for col in available_cols:
            value = str(row[col])
            if pd.isna(row[col]):
                value = "N/A"
            elif len(value) > 100:
                value = value[:100] + "..."
            print(f"   {col}: {value}")
else:
    print("   ⚠️  Standard columns (title, publish_time, journal, authors) not found")
    print("   Available columns:", list(df.columns[:5]))

# Step 1.7: Data quality assessment
print(f"\n🔬 DATA QUALITY ASSESSMENT:")
print("-" * 35)

# Check for duplicate rows
duplicates = df.duplicated().sum()
print(f"   🔄 Duplicate rows: {duplicates:,}")

# Check for completely empty rows
empty_rows = df.isnull().all(axis=1).sum()
print(f"   ⬜ Completely empty rows: {empty_rows:,}")

# Memory usage
memory_usage = df.memory_usage(deep=True).sum() / 1024**2  # Convert to MB
print(f"   💾 Memory usage: {memory_usage:.1f} MB")

print(f"\n🎉 Step 1 Complete!")
print("="*60)
print("📊 SUMMARY:")
print(f"   • Successfully loaded {len(df):,} records")
print(f"   • Dataset has {df.shape[1]} columns")
print(f"   • {len(missing_data)} columns have missing data")
print(f"   • Memory usage: {memory_usage:.1f} MB")

print("\n🔄 NEXT STEPS:")
print("1. ✅ Data loading complete")
print("2. 📝 Create data_cleaning.py for Step 2")
print("3. 📊 Create visualizations in Step 3")
print("4. 🌐 Build Streamlit app in Step 4")

# Optional: Save a summary report
print(f"\n💾 Saving data summary...")
try:
    summary_stats = {
        'total_rows': len(df),
        'total_columns': len(df.columns),
        'columns_with_missing_data': len(missing_data),
        'duplicate_rows': int(duplicates),
        'memory_usage_mb': round(memory_usage, 1),
        'date_range': {
            'min': valid_dates.min().strftime('%Y-%m-%d') if 'publish_time' in df.columns and len(valid_dates) > 0 else 'N/A',
            'max': valid_dates.max().strftime('%Y-%m-%d') if 'publish_time' in df.columns and len(valid_dates) > 0 else 'N/A'
        },
        'analysis_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    # Save summary to a simple text file
    with open('data_exploration_summary.txt', 'w') as f:
        f.write("CORD-19 Data Exploration Summary\n")
        f.write("=" * 40 + "\n\n")
        for key, value in summary_stats.items():
            f.write(f"{key}: {value}\n")
    
    print("✅ Summary saved to 'data_exploration_summary.txt'")
    
except Exception as e:
    print(f"⚠️  Could not save summary: {e}")

print("\n🎯 Ready for Step 2: Data Cleaning!")
print("   Create a new file called 'data_cleaning.py' for the next step.")