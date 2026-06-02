#!/usr/bin/env python3
"""
Appwrite Database & Collections Setup Script
Automatically creates all required database, collections, and buckets for DataMint AI
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Appwrite Configuration
APPWRITE_ENDPOINT = "https://sgp.cloud.appwrite.io/v1"
APPWRITE_PROJECT_ID = "6a1d855e00147768df88"
APPWRITE_API_KEY = os.getenv("APPWRITE_API_KEY")  # You need to provide this

# Database & Collection Names
DATABASE_NAME = "datamint"
DATABASE_ID = "6a1e2f910004t14c7d952"  # Actual database ID from Appwrite

COLLECTIONS = [
    {"name": "users", "id": "users", "description": "User profiles"},
    {"name": "datasets", "id": "datasets", "description": "Uploaded datasets"},
    {"name": "saved-queries", "id": "saved_queries", "description": "Saved search queries"},
    {"name": "downloads", "id": "downloads", "description": "Download history"},
    {"name": "data-sources", "id": "data_sources", "description": "Configured data sources"},
]

BUCKETS = [
    {"name": "datamint-uploads", "id": "datamint_uploads", "description": "File uploads"},
    {"name": "datamint-exports", "id": "datamint_exports", "description": "Exported files"},
]

def setup_appwrite():
    """Setup Appwrite database and collections"""
    
    try:
        from appwrite.client import Client
        from appwrite.services.databases import Databases
        from appwrite.services.storage import Storage
        from appwrite.exception import AppwriteException
    except ImportError:
        print("❌ Appwrite SDK not installed!")
        print("Run: pip install appwrite")
        sys.exit(1)
    
    if not APPWRITE_API_KEY:
        print("❌ APPWRITE_API_KEY not set in .env")
        print("\nTo get API Key:")
        print("1. Go to: https://cloud.appwrite.io/console")
        print("2. Settings → API Keys")
        print("3. Create new API key with all permissions")
        print("4. Add to .env: APPWRITE_API_KEY=your_key_here")
        sys.exit(1)
    
    # Initialize Appwrite Client
    client = Client()
    client.set_endpoint(APPWRITE_ENDPOINT)
    client.set_project(APPWRITE_PROJECT_ID)
    client.set_key(APPWRITE_API_KEY)
    
    databases = Databases(client)
    storage = Storage(client)
    
    print("🚀 Starting Appwrite Setup...")
    print(f"Endpoint: {APPWRITE_ENDPOINT}")
    print(f"Project: {APPWRITE_PROJECT_ID}\n")
    
    # Debug: List all databases
    print("📊 Available databases:")
    database_id = None
    try:
        all_dbs = databases.list()
        # Handle DatabaseList object properly
        db_list = []
        if hasattr(all_dbs, 'databases'):
            db_list = all_dbs.databases
        elif isinstance(all_dbs, dict):
            db_list = all_dbs.get('databases', [])
        
        if len(db_list) > 0:
            for db in db_list:
                db_id = db.id if hasattr(db, 'id') else db.get('$id')
                db_name = db.name if hasattr(db, 'name') else db.get('name')
                print(f"  - {db_name} (ID: {db_id})")
            # Use the first database
            database_id = db_list[0].id if hasattr(db_list[0], 'id') else db_list[0].get('$id')
            print(f"✓ Using database: {database_id}")
        else:
            print("  No databases found - creating new one...")
            # Create new database
            new_db = databases.create(DATABASE_ID, DATABASE_NAME)
            database_id = new_db.id if hasattr(new_db, 'id') else new_db.get('$id')
            print(f"✓ Created database: {DATABASE_NAME} (ID: {database_id})")
    except Exception as e:
        print(f"Error: {e}")
        print(f"Error type: {type(e)}")
        sys.exit(1)
    
    # Step 1 is already done in the listing above
    print("\n📦 Database setup complete")
    print(f"   Database ID: {database_id}")
    
    # Step 2: Create Collections
    print("\n📋 Setting up Collections...")
    created_collections = []
    
    for collection_config in COLLECTIONS:
        collection_name = collection_config["name"]
        collection_id = collection_config["id"]
        description = collection_config.get("description", "")
        
        try:
            # Try to get existing collection
            col = databases.get_collection(database_id, collection_id)
            print(f"✓ Collection exists: {col.name if hasattr(col, 'name') else col.get('name')} (ID: {col.id if hasattr(col, 'id') else col.get('$id')})")
            col_id = col.id if hasattr(col, 'id') else col.get("$id")
            created_collections.append({
                "name": collection_name,
                "id": col_id
            })
        except Exception as e:
            # Try to create collection if it doesn't exist
            try:
                print(f"  Creating collection: {collection_name}...", end="")
                col = databases.create_collection(
                    database_id, 
                    collection_id, 
                    collection_name
                )
                col_id = col.id if hasattr(col, 'id') else col.get("$id")
                created_collections.append({
                    "name": collection_name,
                    "id": col_id
                })
                print(f" ✓")
            except Exception as create_error:
                print(f" ✗")
                print(f"    Error: {create_error}")
    
    print(f"\n✓ Collections ready: {len(created_collections)}/{len(COLLECTIONS)}")
    for col in created_collections:
        print(f"  - {col['name']}: {col['id']}")
    
    # Step 3: Create Storage Buckets
    print("\n📁 Setting up Storage Buckets...")
    created_buckets = []
    
    for bucket_config in BUCKETS:
        bucket_name = bucket_config["name"]
        bucket_id = bucket_config["id"]
        description = bucket_config.get("description", "")
        
        try:
            # Try to get existing bucket
            bucket = storage.get_bucket(bucket_id)
            bucket_id_val = bucket.id if hasattr(bucket, 'id') else bucket.get('$id')
            bucket_name_val = bucket.name if hasattr(bucket, 'name') else bucket.get('name')
            print(f"✓ Bucket exists: {bucket_name_val} (ID: {bucket_id_val})")
            created_buckets.append({
                "name": bucket_name,
                "id": bucket_id_val
            })
        except Exception as e:
            # Try to create bucket if it doesn't exist
            try:
                print(f"  Creating bucket: {bucket_name}...", end="")
                bucket = storage.create_bucket(bucket_id, bucket_name)
                bucket_id_val = bucket.id if hasattr(bucket, 'id') else bucket.get("$id")
                created_buckets.append({
                    "name": bucket_name,
                    "id": bucket_id_val
                })
                print(f" ✓")
            except Exception as create_error:
                print(f" ✗")
                print(f"    Error: {create_error}")
    
    print(f"\n✓ Buckets ready: {len(created_buckets)}/{len(BUCKETS)}")
    for bucket in created_buckets:
        print(f"  - {bucket['name']}: {bucket['id']}")
    
    # Step 4: Print Configuration
    print("\n" + "="*60)
    print("✅ APPWRITE SETUP COMPLETE!")
    print("="*60)
    print("\n📝 Update your src/config/appwrite.ts with these IDs:\n")
    
    print("```typescript")
    print("export const APPWRITE_CONFIG = {")
    print("  databases: {")
    print(f"    MAIN: \"{database_id}\",")
    print("  },")
    print("  collections: {")
    for col in created_collections:
        print(f"    {col['name'].upper().replace('-', '_')}: \"{col['id']}\",")
    print("  },")
    print("  buckets: {")
    for bucket in created_buckets:
        bucket_name_const = bucket['name'].upper().replace('-', '_')
        print(f"    {bucket_name_const}: \"{bucket['id']}\",")
    print("  }")
    print("};")
    print("```\n")
    
    print("📌 Or copy this JSON format:")
    print(f"""
{{
  "DATABASE_ID": "{database_id}",
  "COLLECTIONS": {{
""", end="")
    for col in created_collections:
        print(f'    "{col["name"]}": "{col["id"]}",' if col != created_collections[-1] else f'    "{col["name"]}": "{col["id"]}"', end="")
        print()
    print(f"""  }},
  "BUCKETS": {{
""", end="")
    for bucket in created_buckets:
        print(f'    "{bucket["name"]}": "{bucket["id"]}",' if bucket != created_buckets[-1] else f'    "{bucket["name"]}": "{bucket["id"]}"', end="")
        print()
    print("  }")
    print("}\n")
    
    return database_id, created_collections, created_buckets

if __name__ == "__main__":
    setup_appwrite()
