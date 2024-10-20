
import re
import json
import csv

def main():
    while True:
        print(''' Welcome to the Contact Management System! 

        Menu:

        1. Add a new contact
        2. Edit an existing contact
        3. Delete a contact
        4. S0earch for a contact
        5. Display all contacts
        6. Export contacts to a text file
        7. Import contacts from a text file 
        8. Quit 
        ''')

        contacts = {}

        user_option = int(input("Please enter only the number for the option you would like: "))

        if user_option == 1:
            name = input("Please enter the contacts name: ")
            phone = input("Please enter the contacts phone number: ")
            email = input("Please enter the contacts email address: ")
            additional = input("This section is where you can put any additional comments if you would like (e.g., address, notes): ")
        add_contact(contacts, name, phone, email, additional)

        if user_option == 2:
            name = input("Please enter the name of the conact to edit: ")
            section = input("please enter the section to edit(e.g., name, phone, email, add0itional): ")
            section_update = input("This is where you will put in the updated info: ")
        edit_contact(contacts, section, section_update)

        if user_option == 3:
            name = input("Enter the name of the contact you would like to delete; ")
            delete_contact(contacts, name)

        if user_option == 4:
            name_search = input("Please enter the name of the contact you want search:")
            value_needed = input("Please enter what you need from this contact(Phone Number, Email, Additional Info: ")
            with open(contacts, "r") as details:
                contact_details = json.load(details)
            search_contacts(contact_details, name_search, value_needed)

        if user_option == 5:
            display_contacts(contacts)

        if user_option == 6:
            text_file_name = input("Please enter the new file name here: ") + ".txt"
            export_to_text(contacts, text_file_name)

        if user_option == 7:
            text_file =input("Please enter the text file here: ")
            import_from_text(text_file)

        if user_option == 8:
            break





def add_contact(contacts, name, phone, email, additional):
    while True:
        with open(contacts, 'r+') as file:
            try:
                contacts = json.load(file)
            except json.decoder.JSONDecodeError:
                contacts = {}
        if not name or not re.match(r"^[A-Za-z\s]+$", name):
            print("Invalid name please try again.")
        if not phone or not re.match(r"\d{3}-\d{3}-\d{4}", phone):
            print(f"{phone}is invalid. Please use this format when entering the number: ***-***-**** ")
        if not email or not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            print(f"{email} is invalid. Please double check it and try again: ")
        if not additional:
            print("No additional info was added to this contact")

        contacts[name] = {"Phone number" : phone, "Email" : email, "Additional Info" : additional}

        if input("Would you like to add another? (yes,no): ").lower() == 'no':
            break

        file.seek(0)
        json.dump(contacts, file, indent=4)
        file.truncate()


def edit_contact(contacts, name, section, section_update):
    try:    
        with open(contacts, 'r') as file:
            contacts = json.load(file)
        for contact in contacts:
            if contact['name'] == name:
                if section in contact:
                    contact[section] = section_update
                    break
                else:
                    print(f"\nThe section {section} does not appesr to be present for {contact}")
                    return
    except FileNotFoundError as F:
        print("\nERROR:", F)                
    with open(contacts, 'w') as file:
        json.dump(contacts, file, indent=4)
        print(f"\n{contact}'s info has been updated")

def delete_contact(contacts, name):
    try:
        with open(contacts, 'r') as file:
            details = json.load(file)
        removing = name
        if removing in details:
            removed_value = details.pop(removing, None)
            print(f"\nContact {removing} with info: {removed_value} has been deleted.")
        with open( contacts , 'w') as file:
            json.dump(details, file, indent=4)
    except json.JSONDecodeError as j:
        print("\nERROR", j )
    except KeyError as K:
        print("\nERROR", K )
        
def search_contacts(contact_details, name_search, value_needed):
    try:
        if isinstance(contact_details, dict):
            for name, value in contact_details.items():
                if name == name_search and value == value_needed:
                    print(contact_details)                                                                                                                     
    except Exception as E:
        print(" Encountered an Error", E )

def display_contacts(contacts):
    with open(contacts, 'r') as file:
        details = json.load(file)
    for contact in details[contacts]:
        print("Name:", contact['name'])
        print("Phone:", contact['Phone Number'])
        if 'Email' in contact:
            print("Email:", contact['Email'])
        if 'Additional Info' in contact:
            print("Additional Info:", contact['Additional Info'])
        print("*" * 25)        
        
def export_to_text(contacts, text_file_name):
    with open(text_file_name, 'w') as file:
        json.dump(contacts, file, indent=3)
    

def import_from_text(text_file):
    with open(text_file, 'r') as file:
        read = csv.DictReader(file)
        for row in read:
            name = row['name']
            phone = row['Phone']
            email = row['Email']
            additional = row['Additional Info']

            add_contact(text_file, name, phone, email, additional)

if __name__ == '__main__':
    contacts_data = 'contacts.json'
    main()