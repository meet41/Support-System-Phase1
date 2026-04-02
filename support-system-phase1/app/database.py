from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
from config import settings
from datetime import datetime

class Database:
    """MongoDB connection and initialization"""
    
    def __init__(self):
        self.client = None
        self.db = None

    def connect(self):
        """Connect to MongoDB and setup collections"""
        try:
            self.client = MongoClient(settings.MONGODB_URL, serverSelectionTimeoutMS=5000)
            self.client.admin.command('ping')
            self.db = self.client[settings.DATABASE_NAME]
            print("✅ Connected to MongoDB")
            self._create_collections()
            self._create_indexes()
            self._insert_default_roles()
        except ServerSelectionTimeoutError:
            print("❌ MongoDB connection failed")
            raise

    def disconnect(self):
        """Disconnect from MongoDB"""
        if self.client:
            self.client.close()
            print("✅ Disconnected from MongoDB")

    def _create_collections(self):
        """Create required collections"""
        collections = [
            "customers",
            "support_engineers",
            "roles",
            "tickets",
            "messages",
            "refresh_tokens"
        ]
        existing = self.db.list_collection_names()
        
        for collection in collections:
            if collection not in existing:
                self.db.create_collection(collection)
                print(f"✅ Created collection: {collection}")

    def _create_indexes(self):
        """Create database indexes for optimal query performance"""
        # Customer indexes
        self.db.customers.create_index([("email", 1)], unique=True)
        self.db.customers.create_index([("created_at", -1)])

        # Support engineer indexes
        self.db.support_engineers.create_index([("email", 1)], unique=True)
        self.db.support_engineers.create_index([("role_id", 1)])
        self.db.support_engineers.create_index([("department", 1)])
        self.db.support_engineers.create_index([("created_at", -1)])

        # Role indexes
        self.db.roles.create_index([("role_id", 1)], unique=True)
        self.db.roles.create_index([("role_name", 1)], unique=True)

        # Ticket indexes
        self.db.tickets.create_index([("ticket_number", 1)], unique=True)
        self.db.tickets.create_index([("customer_id", 1)])
        self.db.tickets.create_index([("assigned_engineer_id", 1)])
        self.db.tickets.create_index([("status", 1)])
        self.db.tickets.create_index([("priority", 1)])
        self.db.tickets.create_index([("created_at", -1)])

        # Refresh token indexes
        self.db.refresh_tokens.create_index([("user_id", 1), ("user_type", 1)])
        self.db.refresh_tokens.create_index([("expires_at", 1)])
        self.db.refresh_tokens.create_index([("is_active", 1)])

        print("✅ Indexes created successfully")

    def _insert_default_roles(self):
        """Insert default roles if not exists"""
        # Admin role
        if not self.db.roles.find_one({"role_id": 1}):
            self.db.roles.insert_one({
                "role_id": 1,
                "role_name": "admin",
                "permissions": [
                    "create_ticket",
                    "view_all_tickets",
                    "take_ticket",
                    "send_message",
                    "resolve_ticket",
                    "close_ticket",
                    "manage_engineers",
                    "view_analytics",
                    "manage_roles"
                ],
                "created_at": datetime.utcnow()
            })
            print("✅ Admin role inserted")

        # Support engineer role
        if not self.db.roles.find_one({"role_id": 2}):
            self.db.roles.insert_one({
                "role_id": 2,
                "role_name": "support",
                "permissions": [
                    "create_ticket",
                    "view_assigned_tickets",
                    "view_all_tickets",
                    "take_ticket",
                    "send_message",
                    "resolve_ticket",
                    "close_ticket"
                ],
                "created_at": datetime.utcnow()
            })
            print("✅ Support role inserted")

    def get_db(self):
        """Get database instance"""
        return self.db

db = Database()
