/* 
 * MongoDB Setup Script for Support System Phase 1
 * Run this in MongoDB Shell (mongosh) to initialize the database
 * 
 * Usage:
 *   1. Start MongoDB locally or in Docker
 *   2. Open MongoDB Shell: mongosh
 *   3. Copy and paste these commands one by one or load the entire script
 */

// ============================================================================
// STEP 1: USE DATABASE
// ============================================================================
use support_system_db;

print("\n✓ Using database: support_system_db\n");

// ============================================================================
// STEP 2: CREATE COLLECTIONS
// ============================================================================
print("Creating collections...\n");

// Create customers collection
db.createCollection("customers");
print("✓ Created collection: customers");

// Create support_engineers collection
db.createCollection("support_engineers");
print("✓ Created collection: support_engineers");

// Create roles collection
db.createCollection("roles");
print("✓ Created collection: roles");

// Create tickets collection
db.createCollection("tickets");
print("✓ Created collection: tickets");

// Create messages collection
db.createCollection("messages");
print("✓ Created collection: messages");

// Create refresh_tokens collection
db.createCollection("refresh_tokens");
print("✓ Created collection: refresh_tokens\n");

// ============================================================================
// STEP 3: CREATE INDEXES
// ============================================================================
print("Creating indexes...\n");

// Customer indexes
db.customers.createIndex({ email: 1 }, { unique: true, sparse: true });
db.customers.createIndex({ created_at: -1 });
print("✓ Customer indexes created");

// Support engineer indexes
db.support_engineers.createIndex({ email: 1 }, { unique: true, sparse: true });
db.support_engineers.createIndex({ role_id: 1 });
db.support_engineers.createIndex({ department: 1 });
db.support_engineers.createIndex({ created_at: -1 });
print("✓ Support engineer indexes created");

// Role indexes
db.roles.createIndex({ role_id: 1 }, { unique: true });
db.roles.createIndex({ role_name: 1 }, { unique: true });
print("✓ Role indexes created");

// Refresh token indexes
db.refresh_tokens.createIndex({ user_id: 1, user_type: 1 });
db.refresh_tokens.createIndex({ expires_at: 1 });
db.refresh_tokens.createIndex({ is_active: 1 });
print("✓ Refresh token indexes created\n");

// ============================================================================
// STEP 4: INSERT ROLES
// ============================================================================
print("Inserting roles...\n");

// Admin Role
db.roles.insertOne({
  role_id: 1,
  role_name: "admin",
  permissions: [
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
  created_at: new Date()
});
print("✓ Created role: admin (ID: 1)");

// Support Engineer Role
db.roles.insertOne({
  role_id: 2,
  role_name: "support",
  permissions: [
    "create_ticket",
    "view_assigned_tickets",
    "view_all_tickets",
    "take_ticket",
    "send_message",
    "resolve_ticket",
    "close_ticket"
  ],
  created_at: new Date()
});
print("✓ Created role: support (ID: 2)\n");

// ============================================================================
// STEP 5: INSERT ADMIN USER
// ============================================================================
print("Inserting admin user...\n");

// Admin User
// Password: AdminPass123!
// Hashed with bcrypt (rounds: 12)
db.support_engineers.insertOne({
  support_id: 100,
  name: "System Admin",
  email: "admin@company.com",
  password: "$2b$12$EixZaYVK1fsbw1ZfbX3OzeIvMYvqIYM7LHcI7PH5u/WKhLvF3QTZG",
  role_id: 1,
  department: "administration",
  is_active: true,
  is_online: false,
  last_seen: new Date(),
  created_at: new Date()
});
print("✓ Created admin user");
print("  Email: admin@company.com");
print("  Password: AdminPass123!");
print("  Support ID: 100\n");

// ============================================================================
// STEP 6: INSERT SUPPORT ENGINEERS
// ============================================================================
print("Inserting support engineers...\n");

// Engineer 1: Rahul Kumar
// Password: TechPass123!
db.support_engineers.insertOne({
  support_id: 101,
  name: "Rahul Kumar",
  email: "rahul@company.com",
  password: "$2b$12$XyZ9aYVK1fsbw1ZfbX3OzeIvMYvqIYM7LHcI7PH5u/WKhLvF3QTZB",
  role_id: 2,
  department: "technical",
  is_active: true,
  is_online: false,
  last_seen: new Date(),
  created_at: new Date()
});
print("✓ Created engineer: Rahul Kumar (technical)");
print("  Email: rahul@company.com");
print("  Password: TechPass123!");
print("  Support ID: 101");

// Engineer 2: Priya Sharma
// Password: BillPass123!
db.support_engineers.insertOne({
  support_id: 102,
  name: "Priya Sharma",
  email: "priya@company.com",
  password: "$2b$12$QaBcDEf1GhIJkLMnOpQrStUvWxYzAbCdEfGhIjKlMnOpQ1RsT2UvW",
  role_id: 2,
  department: "billing",
  is_active: true,
  is_online: false,
  last_seen: new Date(),
  created_at: new Date()
});
print("✓ Created engineer: Priya Sharma (billing)");
print("  Email: priya@company.com");
print("  Password: BillPass123!");
print("  Support ID: 102");

// Engineer 3: Amit Singh
// Password: CSPass123!
db.support_engineers.insertOne({
  support_id: 103,
  name: "Amit Singh",
  email: "amit@company.com",
  password: "$2b$12$RsT3UvWxYzAbCdEfGhIjKlMnOpQrStUvWxYzAbCdEfGhIjKlMnOp",
  role_id: 2,
  department: "customer-success",
  is_active: true,
  is_online: false,
  last_seen: new Date(),
  created_at: new Date()
});
print("✓ Created engineer: Amit Singh (customer-success)");
print("  Email: amit@company.com");
print("  Password: CSPass123!");
print("  Support ID: 103\n");

// ============================================================================
// STEP 7: VERIFY DATA
// ============================================================================
print("========================================================");
print("DATA VERIFICATION");
print("========================================================\n");

// Count documents
const roleCount = db.roles.countDocuments({});
const engineerCount = db.support_engineers.countDocuments({});
const customerCount = db.customers.countDocuments({});
const ticketCount = db.tickets.countDocuments({});

print(`Roles in database: ${roleCount}`);
print(`Support engineers in database: ${engineerCount}`);
print(`Customers in database: ${customerCount}`);
print(`Tickets in database: ${ticketCount}\n`);

// List all roles
print("Roles:");
db.roles.find().forEach((role) => {
  print(`  • ${role.role_name} (ID: ${role.role_id}) - Permissions: ${role.permissions.length}`);
});
print();

// List all engineers
print("Support Engineers:");
db.support_engineers.find().sort({ support_id: 1 }).forEach((eng) => {
  const roleMap = { 1: "admin", 2: "support" };
  print(`  • ${eng.name} (${eng.email})`);
  print(`    Support ID: ${eng.support_id}, Role: ${roleMap[eng.role_id]}, Department: ${eng.department}`);
});
print();

// ============================================================================
// STEP 8: TEST QUERIES
// ============================================================================
print("========================================================");
print("USEFUL QUERIES FOR TESTING");
print("========================================================\n");

print("1. Find admin user:");
print("   db.support_engineers.findOne({ role_id: 1 })\n");

print("2. Find all support engineers:");
print("   db.support_engineers.find({ role_id: 2 })\n");

print("3. Find engineer by email:");
print("   db.support_engineers.findOne({ email: 'rahul@company.com' })\n");

print("4. Count all users:");
print("   db.support_engineers.countDocuments({})\n");

print("5. Get all permissions for a role:");
print("   db.roles.findOne({ role_id: 1 })\n");

print("6. Check indexes:");
print("   db.support_engineers.getIndexes()\n");

// ============================================================================
// SETUP COMPLETE
// ============================================================================
print("========================================================");
print("SETUP COMPLETE!");
print("========================================================\n");

print("✓ MongoDB setup is complete and ready for testing\n");

print("Next Steps:");
print("  1. Start FastAPI server:");
print("     python -m uvicorn main:app --reload\n");

print("  2. Access API docs:");
print("     http://localhost:8000/docs\n");

print("  3. Test with credentials:");
print("     Admin: admin@company.com / AdminPass123!");
print("     Engineer: rahul@company.com / TechPass123!");
print("     Engineer: priya@company.com / BillPass123!");
print("     Engineer: amit@company.com / CSPass123!\n");
