import pymongo
from bson import ObjectId

class Connection:
    def _init_(self, options):
        self.client = pymongo.MongoClient(**options)
        self.db = self.client["MobileInternetDB"]  
        self.collection = self.db["users"]  
        print(f"Connected to MongoDB database successfully!")

    def list_rows(self):
        results = self.collection.find()  
        print("ID\t\t\t\tUsername\t\tNumber\t\tInternet Plan")
        for user in results:
            print("{0}\t{1:<20}\t{2}\t{3}".format(
                    user['_id'],
                    user['username'],
                    user['number'],
                    user['internet_plan'],
                ) 
            )

    def create_row(self):
        print("\nEnter new user details")
        username = input("Username: ")
        number = input("Mobile Number: ")
        internet_plan = input("Internet Plan (e.g., 10GB/month, Unlimited): ")

        # Insert new user document
        new_user = {
            "username": username,
            "number": number,
            "internet_plan": internet_plan
        }
        self.collection.insert_one(new_user)
        print("\nNew user added!")

    def delete_row(self):
        no = input("\nEnter number of user to remove: ")
        result = self.collection.delete_one({"number": no})
        if result.deleted_count > 0:
            print("\nUser removed successfully!")
        else:
            print("\nUser not found!")

    def update_row(self):
        no = input("\nEnter number to update: ")
        new_plan = input("Enter new internet plan: ")
        result = self.collection.update_one(
            {"number": no },
            {"$set": {"internet_plan": new_plan}}
        )
        if result.modified_count > 0:
            print("\nUser internet plan updated successfully!")
        else:
            print("\nUser not found or no changes made!")

    # Search function to find users by username
    def search_row(self):
        username = input("\nEnter username to search: ")
        # Use regex for partial matching (case-insensitive)
        results = self.collection.find({"username": {"$regex": username, "$options": "i"}})

        found = False  # Flag to check if any result is found
        print("ID\t\t\t\tUsername\t\tNumber\t\tInternet Plan")
        for user in results:
            found = True  # If we enter the loop, a document has been found
            print("{0}\t{1:<20}\t{2}\t{3}".format(
                    user['_id'],
                    user['username'],
                    user['number'],
                    user['internet_plan'],
                )
            )
        
        if not found:
            print("\nNo users found matching the search criteria.")

    def close(self):
        self.client.close()
        print("Connection closed.")


# MongoDB connection options
options = {
    "host": "localhost",
    "port": 27017,  
}

# Create a connection object
conn = Connection(options)

# Main loop for user interaction
while True:
    print("\n\t\t\tMobile Internet Database\t\t\t")
    print("1. Show all users")
    print("2. Add new user")
    print("3. Update user internet plan")
    print("4. Delete user")
    print("5. Search for a user")
    print("6. Exit")

    ch = int(input("\nEnter option: "))

    if ch == 1:
        conn.list_rows()

    elif ch == 2:
        conn.create_row()

    elif ch == 3:
        conn.update_row()

    elif ch == 4:
        conn.delete_row()

    elif ch == 5:
        conn.search_row()

    elif ch == 6:
        conn.close()
        print("Thank you!")
        break

    else:
        print("Invalid option. Please choose again.")