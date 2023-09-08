import pandas as pd
from api.contacts.schema import Contact
# Create a list of dictionaries with contact information
contacts = [
    {
        "firstName": "John",
        "lastName": "Doe",
        "companyName": "ABC Inc.",
        "email": "john.doe@example.com",
    },
    {
        "firstName": "Jane",
        "lastName": "Smith",
        "companyName": "XYZ Corp",
        "email": "jane.smith@example.com",
    },
    {
        "firstName": "Mike",
        "lastName": "Johnson",
        "companyName": "LMN Ltd",
        "email": "mike.johnson@example.com",
    },
]

# Create a DataFrame from the list of dictionaries
df = pd.DataFrame(contacts)

# Save the DataFrame as a CSV file
# 
print(Contact.__annotations__.items())
print([field.alias for _, field in Contact.model_fields.items()])
