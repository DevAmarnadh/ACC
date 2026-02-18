"""
Database Connection Tester & Fixer
Run this to diagnose database connection issues
"""
import os
from dotenv import load_dotenv

print("="*60)
print("🔧 DATABASE CONNECTION TESTER")
print("="*60)
print()

# Step 1: Check .env file
print("Step 1: Checking .env file...")
if not os.path.exists('.env'):
    print("❌ .env file not found!")
    print("Creating .env file...")
    with open('.env', 'w') as f:
        f.write('DATABASE_URL=postgresql://postgres:Single%406112123ed@db.flcdlrjzuompnirafxns.supabase.co:5432/postgres\n')
        f.write('SUPABASE_URL=https://flcdlrjzuompnirafxns.supabase.co\n')
        f.write('SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZsY2Rscmp6dW9tcG5pcmFmeG5zIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzEzNDg0ODYsImV4cCI6MjA4NjkyNDQ4Nn0.Mc6v0zTOiopEuQjAFLJCjeETyeYPKV6IoEUkIpcR7mM\n')
    print("✅ .env file created")
else:
    print("✅ .env file exists")

print()

# Step 2: Load environment variables
print("Step 2: Loading environment variables...")
load_dotenv()
db_url = os.getenv('DATABASE_URL')

if db_url:
    print("✅ DATABASE_URL found")
    # Parse URL to show details (safely)
    if '@' in db_url:
        parts = db_url.split('@')
        host_part = parts[1].split(':')[0] if ':' in parts[1] else parts[1].split('/')[0]
        print(f"   Host: {host_part}")
        print(f"   Database: postgres")
    else:
        print("⚠️  URL format might be incorrect")
else:
    print("❌ DATABASE_URL not found in .env")
    print("Please check your .env file")
    exit(1)

print()

# Step 3: Check password encoding
print("Step 3: Checking password encoding...")
if '%40' in db_url:
    print("✅ Password is URL-encoded (@ → %40)")
elif '@' in db_url.split('://')[1].split('@')[0]:
    print("⚠️  Password might not be properly encoded")
    print("   Make sure @ is encoded as %40")
else:
    print("✅ Password encoding looks correct")

print()

# Step 4: Test internet connectivity
print("Step 4: Testing internet connectivity...")
try:
    import socket
    socket.create_connection(("8.8.8.8", 53), timeout=3)
    print("✅ Internet connection active")
except:
    print("❌ No internet connection")
    print("   Supabase requires internet access")
    exit(1)

print()

# Step 5: Test database connection
print("Step 5: Testing database connection...")
print("   This may take a few seconds...")

try:
    from sqlalchemy import create_engine
    
    engine = create_engine(
        db_url,
        connect_args={
            'connect_timeout': 10,
            'sslmode': 'require'
        }
    )
    
    with engine.connect() as conn:
        result = conn.execute("SELECT 1")
        print("✅ Database connection successful!")
        print()
        
        # Test if table exists
        print("Step 6: Checking database tables...")
        try:
            result = conn.execute("SELECT COUNT(*) FROM content_history")
            count = result.scalar()
            print(f"✅ Table 'content_history' exists")
            print(f"   Records: {count}")
        except:
            print("⚠️  Table 'content_history' doesn't exist yet")
            print("   It will be created automatically on first use")
        
except Exception as e:
    print(f"❌ Database connection failed!")
    print(f"   Error: {str(e)}")
    print()
    print("Possible solutions:")
    print("1. Check internet connection")
    print("2. Verify Supabase project is active:")
    print("   https://supabase.com/dashboard/project/flcdlrjzuompnirafxns")
    print("3. Check firewall settings")
    print("4. Verify password encoding in .env file")
    print("   Password should be: Single%406112123ed (not Single@6112123ed)")
    print()
    print("The app will still work without database!")
    print("You just won't be able to save history.")
    exit(1)

print()
print("="*60)
print("✅ ALL CHECKS PASSED!")
print("="*60)
print()
print("Your database is properly configured and connected.")
print("You can now run the app:")
print()
print("   streamlit run app.py")
print()
print("="*60)
