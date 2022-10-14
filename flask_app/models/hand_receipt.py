from flask_app.config.mysqlconnection import connectToMySQL #specify folder
from flask import flash
from flask_app.models.user import User
import re

class Hand_receipt: # modify class. Every class needs a constructor __init__
    def __init__( self , data, poster=None ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.section = data['section']
        self.hand_receipt_number = data['hand_receipt_number']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.users_id = data['users_id']
        self.poster = None
    # Now we use class methods to query our database. # Create Read Update Delete queries happen in models
    @classmethod #not specific to any instances
    def get_all(cls, data): # method to get all data from the database and display on html
        query = "SELECT * FROM hand_receipts;" 
        # make sure to call the connectToMySQL function with the schema you are targeting.
        results = connectToMySQL('property_book').query_db(query) # connectToMySQL schema name
        # Create an empty list to append our instances of friends
        hand_receipts = []
        # Iterate over the db results and create instances of recipes with cls.
        for hand_receipt in results:
            hand_receipts.append( cls(hand_receipt) )
        return hand_receipts
    
    @classmethod # method to insert shows into the database
    def save(cls, data):
        query = "INSERT INTO hand_receipts (first_name, last_name, section, hand_receipt_number, created_at, updated_at, users_id) VALUES (%(first_name)s, %(last_name)s, %(section)s, %(hand_receipt_number)s, NOW(), NOW(), %(users_id)s);"
        return connectToMySQL('property_book').query_db(query, data)
    
    @classmethod 
    def all_hand_receipts_with_users(cls):
        query = "SELECT * FROM hand_receipts JOIN users ON hand_receipts.users_id = users.id" 
        results = connectToMySQL('property_book').query_db(query)
        print(results)
        
        all_hand_receipts = []
        
        for hand_receipt in results:
            one_hand_receipt = cls(hand_receipt)
            
            user_data = {
                "id":hand_receipt["users.id"],
                "first_name":hand_receipt["first_name"],
                "last_name":hand_receipt["last_name"],
                "email":hand_receipt["email"],
                "password":hand_receipt["password"],
                "created_at":hand_receipt["created_at"],
                "updated_at":hand_receipt["updated_at"],
            }
            one_hand_receipt.poster = User(user_data)
            all_hand_receipts.append(one_hand_receipt)
        
        return all_hand_receipts
    
    @staticmethod # method to validate inputs
    def validation(data):
        is_valid = True
        
        if len(data["first_name"]) < 3 or len(data["first_name"]) > 255:
            flash("first_name must be at least 3 characters")
            is_valid = False
        if len(data["last_name"]) < 3 or len(data["last_name"]) > 255:
            flash("last_name must be at least 3 characters")
            is_valid = False
        if len(data["section"]) < 3 or len(data["section"]) > 255:
            flash("section must be at least 3 characters")
            is_valid = False
        if len(data["hand_receipt_number"]) < 0 or len(data["hand_receipt_number"]) > 255:
            flash("hand_receipt must be greater than 0")
            is_valid = False
        
        return is_valid
    
    @classmethod # method to display data on html
    def get_single_hand_receipt(cls, data):
        query = "SELECT * FROM hand_receipts WHERE id=%(id)s;"
        results = connectToMySQL("property_book").query_db(query,data)
        one_hand_receipt = cls(results[0])
        return one_hand_receipt
    
    @classmethod # method to edit data and post
    def edit_hand_receipt(cls, data):
        query = "UPDATE hand_receipts SET first_name = %(first_name)s, last_name = %(last_name)s,  section = %(section)s,  hand_receipt_number = %(hand_receipt_number)s, updated_at = NOW() WHERE id = %(id)s;"
        results = connectToMySQL('property_book').query_db(query, data)
        return results
    
    
    @classmethod #to find one show
    def find_one_hand_receipt(cls, data):
        query = "SELECT * FROM hand_receipts WHERE id=%(id)s;"
        single_hand_receipt = connectToMySQL('property_book').query_db(query, data) #database sends back data. We need to save it on route (show_page) using variable
        return cls(single_hand_receipt[0])

    @classmethod
    def delete(cls, data):
        query = "DELETE FROM hand_receipts WHERE id = %(id)s;"
        results = connectToMySQL('property_book').query_db(query, data)
        return results