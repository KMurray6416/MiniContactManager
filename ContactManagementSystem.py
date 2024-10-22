import re
import json
import csv

def main():

    contacts = {
        "John Doe": {
            "Phone number": "123-456-7890",
            "Email": "john.doe@example.com",
            "Additional Info": "123 Elm St, Springfield"
        },
        "Jane Smith": {
            "Phone number": "987-654-3210",
            "Email": "jane.smith@example.com",
            "Additional Info": "456 Oak St, Springfield"
        },
        "Alice Johnson": {
            "Phone number": "555-123-4567",
            "Email": "alice.johnson@example.com",
            "Additional Info": "789 Pine St, Springfield"
        },
        "Bob Brown": {
            "Phone number": "444-777-8888",
            "Email": "bob.brown@example.com",
            "Additional Info": "321 Maple St, Springfield"
        }
    }


    while True:
        print(''' \nWelcome to the Contact Management System! 

        Menu:

        1. Add a new contact
        2. Edit an existing contact
        3. Delete a contact
        4. Search for a contact
        5. Display all contacts
        6. Export contacts to a text file
        7. Import contacts from a text file 
        8. Quit 
        ''')

        user_option = get_user_option()

        if user_option == 1:
            # Adding a contact
            while True:
                name = input("Please enter the contact's name: ")
                if not name or not re.match(r"^[A-Za-z\s]+$", name):
                    print("Invalid name.")
                    continue
                phone = input("Please enter the contact's phone number (format: ***-***-****): ")
                if not phone or not re.match(r"\d{3}-\d{3}-\d{4}", phone):
                    print(f"{phone} is invalid. Please use this format: ***-***-****.")
                    continue
                email = input("Please enter the contact's email address: ")
                if not email or not re.match(r'[^@]+@[^@]+\.[^@]+', email):
                    print(f"{email} is invalid. Please double-check it.")
                    continue
                additional = input("Any additional comments (e.g., address, notes): ")

                add_contact(contacts, name, phone, email, additional)
                print("\nYour new contact has been added to your contacts")
                break  # Exit the loop if input is valid

        elif user_option == 2:
            # Editing a contact
            while True:
                name = input("Please enter the name of the contact to edit: ")
                section = input("Please enter the section to edit (e.g., phone, email, additional): ")
                section_update = input("Enter the updated info: ")

                if name in contacts:
                    edit_contact(contacts, name, section, section_update)
                    break  # Exit the loop if contact is found and updated
                else:
                    user_retry = input("Contact or section not found. Would you like to try again? (yes,no)")
                    if user_retry == 'no':
                        break
                    

        elif user_option == 3:
            # Deleting a contact
            while True:
                name = input("Enter the name of the contact you would like to delete: ")
                if name in contacts:
                    delete_contact(contacts, name)
                    break  # Exit the loop if contact is deleted
                else:
                    print(f"Contact {name} not found. Please try again.")

        elif user_option == 4:
            # Searching for a contact
            while True:
                name_search = input("Please enter the name of the contact you want to search: ")
                value_needed = input("Please enter what you need from this contact (Phone Number, Email, Additional Info): ")
                
                if name_search in contacts:
                    search_contacts(contacts, name_search, value_needed)
                    break  # Exit the loop if search is successful
                else:
                    print("Contact not found. Please try again.")

        elif user_option == 5:
            # Displaying all contacts
            display_contacts(contacts)

        elif user_option == 6:
            # Exporting contacts to a text file
            text_file_name = input("Please enter the new file name here: ") + ".txt"
            export_to_text(contacts, text_file_name)

        elif user_option == 7:
            # Importing contacts from a text file
            text_file = input("Please enter the text file here: ")
            import_from_text(text_file, contacts)

        elif user_option == 8:
            break

def get_user_option():
    while True:
        try:
            user_option = int(input("Please enter only the number for the option you would like: "))
            if 1 <= user_option <= 8:
                return user_option
            else:
                print("Invalid option. Please enter a number between 1 and 8.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def add_contact(contacts, name, phone, email, additional):
    contacts[name] = {
        "Phone number": phone,
        "Email": email,
        "Additional Info": additional
    }
    save_contacts(contacts)

def edit_contact(contacts, name, section, section_update):
    contacts[name]['{section}'] = section_update
    save_contacts(contacts)
    print(f"{name}'s info has been updated.")

def delete_contact(contacts, name):
    removed_value = contacts.pop(name, None)
    print(f"Contact {name} with info: {removed_value} has been deleted.")
    save_contacts(contacts)

def search_contacts(contacts, name_search, value_needed):
    contact_info = contacts[name_search]
    print(f"{name_search}: {contact_info.get(value_needed, 'Not found')}")

def display_contacts(contacts):
    for contact_name, contact_info in contacts.items():
        print("Name:", contact_name)
        print("Phone:", contact_info.get("Phone number", "N/A"))
        print("Email:", contact_info.get("Email", "N/A"))
        print("Additional Info:", contact_info.get("Additional Info", "N/A"))
        print("*" * 25)

def export_to_text(contacts, text_file_name):
    with open(text_file_name, 'w') as file:
        json.dump(contacts, file, indent=3)

def import_from_text(text_file, contacts):
    try:
        with open(text_file, 'r') as file:
            read = csv.DictReader(file)
            for row in read:
                add_contact(contacts, row['name'], row['Phone'], row['Email'], row['Additional Info'])
    except FileNotFoundError:
        print("Text file not found.")
    except Exception as e:
        print("An error occurred while importing:", e)

def save_contacts(contacts):
    with open('contacts.json', 'w') as file:
        json.dump(contacts, file, indent=4)

if __name__ == '__main__':
    main()
