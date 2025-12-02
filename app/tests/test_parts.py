from datetime import date
from app import create_app
from app.models import db, Mechanics, Parts, Inventory, ServiceTickets, Customers
import unittest
from werkzeug.security import generate_password_hash
from app.util.auth import encode_token


class TestParts(unittest.TestCase):
    
    def setUp(self):
        # Set up test client and database
        self.app = create_app('testing')
        
        with self.app.app_context():
            db.drop_all()
            db.create_all()
            
            # Create test mechanic for authentication
            self.mechanic = Mechanics(
                first_name="Test", 
                last_name="Mechanic", 
                email="mechanic@email.com", 
                password=generate_password_hash('password'),
                address="123 Test St",
                salary=50000.00
            )
            db.session.add(self.mechanic)
            
            # Create test customer (required for ServiceTickets)
            self.customer = Customers(
                first_name="John",
                last_name="Doe",
                email="customer@email.com",
                password=generate_password_hash('password'),
                phone="555-1234"
            )
            db.session.add(self.customer)
            db.session.commit()
            
            # Create test inventory item
            self.inventory = Inventory(
                name="Engine Oil",
                price=25.99
            )
            db.session.add(self.inventory)
            db.session.commit()
            
            # Create test part
            self.part = Parts(
                desc_id=self.inventory.id,
                ticket_id=None
            )
            db.session.add(self.part)
            
            # Create test service ticket
            self.ticket = ServiceTickets(
                customer_id=self.customer.id,
                service_desc="Oil change",
                VIN="1HGBH41JXMN109186",
                service_date=date.today(),
                price=150.00
            )
            db.session.add(self.ticket)
            db.session.commit()
            
        self.token = encode_token(1, role="mechanic")
        self.client = self.app.test_client()
    
    # ============== INVENTORY TESTS ==============
    
    # ===== CREATE INVENTORY TESTS =====
    def test_create_inventory(self):
        # Test creating a new inventory item with authentication
        headers = {"Authorization": "Bearer " + self.token}
        inventory_payload = {
            "name": "Brake Fluid",
            "price": 18.99
        }
        
        response = self.client.post('/parts/inventory', headers=headers, json=inventory_payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['name'], "Brake Fluid")
        self.assertEqual(response.json['price'], 18.99)
    
    def test_create_inventory_unauthorized(self):
        # Negative test: Create inventory without authentication
        inventory_payload = {
            "name": "Brake Fluid",
            "price": 18.99
        }
        
        response = self.client.post('/parts/inventory', json=inventory_payload)
        self.assertEqual(response.status_code, 401)
    
    def test_create_inventory_missing_fields(self):
        # Negative test: Create inventory with missing required fields
        headers = {"Authorization": "Bearer " + self.token}
        inventory_payload = {
            "name": "Brake Fluid"
            # Missing price
        }
        
        response = self.client.post('/parts/inventory', headers=headers, json=inventory_payload)
        self.assertEqual(response.status_code, 400)
    
    # ===== READ ALL INVENTORY TESTS =====
    def test_read_inventory(self):
        # Test getting all inventory items
        response = self.client.get('/parts/inventory')
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.json) > 0)
        self.assertEqual(response.json[0]['name'], "Engine Oil")
    
    def test_read_inventory_empty(self):
        # Test getting inventory when database is empty
        with self.app.app_context():
            db.session.query(Inventory).delete()
            db.session.commit()
        
        response = self.client.get('/parts/inventory')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 0)
    
    def test_read_inventory_multiple_items(self):
        # Test getting multiple inventory items
        headers = {"Authorization": "Bearer " + self.token}
        
        # Create additional inventory items
        for i in range(3):
            inventory_payload = {
                "name": f"Item {i}",
                "price": 5.99 + i
            }
            self.client.post('/parts/inventory', headers=headers, json=inventory_payload)
        
        response = self.client.get('/parts/inventory')
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(response.json), 4)  # 1 from setUp + 3 new
    
    # ===== READ SINGLE INVENTORY ITEM TESTS =====
    def test_read_inventory_item(self):
        # Test getting a specific inventory item
        response = self.client.get('/parts/inventory/1')
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], "Engine Oil")
        self.assertEqual(response.json['price'], 25.99)
    
    def test_read_inventory_item_not_found(self):
        # Negative test: Get non-existent inventory item
        response = self.client.get('/parts/inventory/9999')
        
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json['error'], 'Inventory item not found')
    
    def test_read_inventory_item_invalid_id(self):
        # Negative test: Get inventory item with invalid ID format
        response = self.client.get('/parts/inventory/invalid')
        self.assertEqual(response.status_code, 404)
    
    # ===== UPDATE INVENTORY ITEM TESTS =====
    def test_update_inventory(self):
        # Test updating an inventory item
        headers = {"Authorization": "Bearer " + self.token}
        update_payload = {
            "name": "Updated Engine Oil",
            "price": 30.99
        }
        
        response = self.client.put('/parts/inventory/1', headers=headers, json=update_payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], "Updated Engine Oil")
        self.assertEqual(response.json['price'], 30.99)
    
    def test_update_inventory_unauthorized(self):
        # Negative test: Update inventory without authentication
        update_payload = {
            "name": "Updated Engine Oil"
        }
        
        response = self.client.put('/parts/inventory/1', json=update_payload)
        self.assertEqual(response.status_code, 401)
    
    def test_update_inventory_not_found(self):
        # Negative test: Update non-existent inventory item
        headers = {"Authorization": "Bearer " + self.token}
        update_payload = {
            "name": "Updated Oil"
        }
        
        response = self.client.put('/parts/inventory/9999', headers=headers, json=update_payload)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json['error'], 'Inventory item not found')
    
    def test_update_inventory_invalid_token(self):
        # Negative test: Update inventory with invalid token
        headers = {"Authorization": "Bearer invalidtoken123"}
        update_payload = {
            "name": "Updated Oil"
        }
        
        response = self.client.put('/parts/inventory/1', headers=headers, json=update_payload)
        self.assertEqual(response.status_code, 401)
    
    # ===== DELETE INVENTORY ITEM TESTS =====
    def test_delete_inventory(self):
        # Test deleting an inventory item
        headers = {"Authorization": "Bearer " + self.token}
        
        response = self.client.delete('/parts/inventory/1', headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['message'], 'Inventory item 1 deleted')
        
        # Verify deletion
        with self.app.app_context():
            deleted_item = db.session.get(Inventory, 1)
            self.assertIsNone(deleted_item)
    
    def test_delete_inventory_unauthorized(self):
        # Negative test: Delete inventory without authentication
        response = self.client.delete('/parts/inventory/1')
        self.assertEqual(response.status_code, 401)
    
    def test_delete_inventory_not_found(self):
        # Negative test: Delete non-existent inventory item
        headers = {"Authorization": "Bearer " + self.token}
        
        response = self.client.delete('/parts/inventory/9999', headers=headers)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json['error'], 'Inventory item not found')
    
    def test_delete_inventory_invalid_token(self):
        # Negative test: Delete inventory with invalid token
        headers = {"Authorization": "Bearer invalidtoken123"}
        
        response = self.client.delete('/parts/inventory/1', headers=headers)
        self.assertEqual(response.status_code, 401)
    
    # ============== PARTS TESTS ==============
    
    # ===== CREATE PART TESTS =====
    def test_create_part(self):
        # Test creating a new part with authentication
        headers = {"Authorization": "Bearer " + self.token}
        part_payload = {
            "desc_id": 1,
            "ticket_id": None
        }
        
        response = self.client.post('/parts', headers=headers, json=part_payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['desc_id'], 1)
        self.assertIsNone(response.json['ticket_id'])
    
    def test_create_part_unauthorized(self):
        # Negative test: Create part without authentication
        part_payload = {
            "desc_id": 1,
            "ticket_id": None
        }
        
        response = self.client.post('/parts', json=part_payload)
        self.assertEqual(response.status_code, 401)
    
    def test_create_part_missing_fields(self):
        # Negative test: Create part with missing required fields
        headers = {"Authorization": "Bearer " + self.token}
        part_payload = {
            # Missing desc_id
            "ticket_id": None
        }
        
        response = self.client.post('/parts', headers=headers, json=part_payload)
        self.assertEqual(response.status_code, 400)
    
    def test_create_part_invalid_token(self):
        # Negative test: Create part with invalid token
        headers = {"Authorization": "Bearer invalidtoken123"}
        part_payload = {
            "desc_id": 1,
            "ticket_id": None
        }
        
        response = self.client.post('/parts', headers=headers, json=part_payload)
        self.assertEqual(response.status_code, 401)
    
    # ===== READ ALL PARTS TESTS =====
    def test_read_parts(self):
        # Test getting all parts
        response = self.client.get('/parts')
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.json) > 0)
        self.assertEqual(response.json[0]['desc_id'], 1)
    
    def test_read_parts_empty(self):
        # Test getting parts when database is empty
        with self.app.app_context():
            db.session.query(Parts).delete()
            db.session.commit()
        
        response = self.client.get('/parts')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 0)
    
    def test_read_parts_multiple(self):
        # Test getting multiple parts
        headers = {"Authorization": "Bearer " + self.token}
        
        # Create additional parts
        for i in range(5):
            part_payload = {
                "desc_id": 1,
                "ticket_id": None
            }
            self.client.post('/parts', headers=headers, json=part_payload)
        
        response = self.client.get('/parts')
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(response.json), 6)  # 1 from setUp + 5 new
    
    # ===== READ SINGLE PART TESTS =====
    def test_read_part(self):
        # Test getting a specific part
        response = self.client.get('/parts/1')
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['desc_id'], 1)
        self.assertIsNone(response.json['ticket_id'])
    
    def test_read_part_not_found(self):
        # Negative test: Get non-existent part
        response = self.client.get('/parts/9999')
        
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json['error'], 'Part not found')
    
    def test_read_part_invalid_id(self):
        # Negative test: Get part with invalid ID format
        response = self.client.get('/parts/invalid')
        self.assertEqual(response.status_code, 404)
    
    # ===== UPDATE PART TESTS =====
    def test_update_part(self):
        # Test updating a part
        headers = {"Authorization": "Bearer " + self.token}
        update_payload = {
            "ticket_id": 1
        }
        
        response = self.client.put('/parts/1', headers=headers, json=update_payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['ticket_id'], 1)
    
    def test_update_part_unauthorized(self):
        # Negative test: Update part without authentication
        update_payload = {
            "ticket_id": 1
        }
        
        response = self.client.put('/parts/1', json=update_payload)
        self.assertEqual(response.status_code, 401)
    
    def test_update_part_not_found(self):
        # Negative test: Update non-existent part
        headers = {"Authorization": "Bearer " + self.token}
        update_payload = {
            "ticket_id": 1
        }
        
        response = self.client.put('/parts/9999', headers=headers, json=update_payload)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json['error'], 'Part not found')
    
    def test_update_part_invalid_token(self):
        # Negative test: Update part with invalid token
        headers = {"Authorization": "Bearer invalidtoken123"}
        update_payload = {
            "ticket_id": 1
        }
        
        response = self.client.put('/parts/1', headers=headers, json=update_payload)
        self.assertEqual(response.status_code, 401)
    
    # ===== DELETE PART TESTS =====
    def test_delete_part(self):
        # Test deleting a part
        headers = {"Authorization": "Bearer " + self.token}
        
        response = self.client.delete('/parts/1', headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['message'], 'Part 1 deleted')
        
        # Verify deletion
        with self.app.app_context():
            deleted_part = db.session.get(Parts, 1)
            self.assertIsNone(deleted_part)
    
    def test_delete_part_unauthorized(self):
        # Negative test: Delete part without authentication
        response = self.client.delete('/parts/1')
        self.assertEqual(response.status_code, 401)
    
    def test_delete_part_not_found(self):
        # Negative test: Delete non-existent part
        headers = {"Authorization": "Bearer " + self.token}
        
        response = self.client.delete('/parts/9999', headers=headers)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json['error'], 'Part not found')
    
    def test_delete_part_invalid_token(self):
        # Negative test: Delete part with invalid token
        headers = {"Authorization": "Bearer invalidtoken123"}
        
        response = self.client.delete('/parts/1', headers=headers)
        self.assertEqual(response.status_code, 401)
    
    # ===== GET AVAILABLE PARTS TESTS =====
    def test_get_available_parts(self):
        # Test getting parts not assigned to any ticket
        response = self.client.get('/parts/available')
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.json) > 0)
        self.assertEqual(response.json[0]['desc_id'], 1)
        self.assertIsNone(response.json[0]['ticket_id'])
    
    def test_get_available_parts_none_available(self):
        # Test getting available parts when all are assigned
        # Assign all parts to tickets
        with self.app.app_context():
            part = db.session.get(Parts, 1)
            part.ticket_id = 1
            db.session.commit()
        
        response = self.client.get('/parts/available')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 0)
    
    def test_get_available_parts_mixed(self):
        # Test getting available parts when some are assigned
        headers = {"Authorization": "Bearer " + self.token}
        
        # Create additional parts
        for i in range(2):
            part_payload = {
                "desc_id": 1,
                "ticket_id": None
            }
            self.client.post('/parts', headers=headers, json=part_payload)
        
        # Assign one part to a ticket
        with self.app.app_context():
            part = db.session.get(Parts, 2)
            part.ticket_id = 1
            db.session.commit()
        
        response = self.client.get('/parts/available')
        self.assertEqual(response.status_code, 200)
        # Should have 2 available parts (part 1 and part 3)
        self.assertEqual(len(response.json), 2)
        
        # Verify none have ticket_id
        for part in response.json:
            self.assertIsNone(part['ticket_id'])
    
    def test_get_available_parts_empty_database(self):
        # Test getting available parts when no parts exist
        with self.app.app_context():
            db.session.query(Parts).delete()
            db.session.commit()
        
        response = self.client.get('/parts/available')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 0)


if __name__ == '__main__':
    unittest.main()