#!/usr/bin/env python3
"""
Initialize database with default admin user
Run this script once to set up the first admin account
"""

from datetime import datetime
from pymongo import MongoClient
from app.config import settings
from app.utils.security import security_service

def init_database():
    """Initialize database and create first admin user"""
    try:
        # Connect to MongoDB
        client = MongoClient(settings.MONGODB_URL, serverSelectionTimeoutMS=5000)
        client.admin.command('ping')
        db = client[settings.DATABASE_NAME]
        print("✅ Connected to MongoDB")
        
        # Create collections
        collections = ["customers", "support_engineers", "roles", "tickets", "messages"]
        existing = db.list_collection_names()
        
        for collection in collections:
            if collection not in existing:
                db.create_collection(collection)
                print(f"✅ Created collection: {collection}")
        
        # Create indexes
        db.customers.create_index([("email", 1)], unique=True)
        db.support_engineers.create_index([("email", 1)], unique=True)
        db.roles.create_index([("role_id", 1)], unique=True)
        print("✅ Indexes created")
        
        # Insert default roles
        if not db.roles.find_one({"role_id": 1}):
            db.roles.insert_one({
                "role_id": 1,
                "role_name": "admin",
                "permissions": [
                    "create_ticket", "view_all_tickets", "take_ticket", 
                    "send_message", "resolve_ticket", "close_ticket",
                    "manage_engineers", "view_analytics", "manage_roles"
                ],
                "created_at": datetime.utcnow()
            })
            print("✅ Admin role created")
        
        if not db.roles.find_one({"role_id": 2}):
            db.roles.insert_one({
                "role_id": 2,
                "role_name": "support",
                "permissions": [
                    "view_assigned_tickets", "take_ticket", "send_message",
                    "resolve_ticket", "close_ticket"
                ],
                "created_at": datetime.utcnow()
            })
            print("✅ Support role created")
        
        # Create first admin user
        admin_email = "admin@support.com"
        admin_exists = db.support_engineers.find_one({"email": admin_email})
        
        if not admin_exists:
            admin_password = "Admin@123456"  # Change this to a secure password
            hashed_pw = security_service.hash_password(admin_password)
            
            admin_doc = {
                "support_id": 100,
                "name": "System Administrator",
                "email": admin_email,
                "password": hashed_pw,
                "role_id": 1,  # Admin role
                "department": "Administration",
                "is_active": True,
                "is_online": False,
                "last_seen": datetime.utcnow(),
                "created_at": datetime.utcnow()
            }
            
            db.support_engineers.insert_one(admin_doc)
            print("✅ Admin user created")
            print(f"   Email: {admin_email}")
            print(f"   Password: {admin_password}")
            print("   ⚠️  CHANGE THIS PASSWORD IMMEDIATELY IN PRODUCTION!")
        else:
            print("ℹ️  Admin user already exists")
        
        client.close()
        print("\n✅ Database initialization completed successfully!")
        print("\nNext steps:")
        print("1. Start the server: python -m uvicorn app.main:app --reload")
        print(f"2. Login as admin with email: {admin_email}")
        print("3. Use the access token to register new engineers")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        raise

if __name__ == "__main__":
    init_database()
