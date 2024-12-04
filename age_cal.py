from datetime import datetime

def calculate_age(dob_str):
    # Parse the date string into a datetime object
    dob = datetime.strptime(dob_str, '%m/%d/%Y')
    
    # Get today's date
    today = datetime.now()
    
    # Calculate age
    age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
    
    return age

# Example usage
date_of_birth = '03/14/1948'  # Your date of birth in DD/MM/YYYY format
# age = calculate_age(date_of_birth)
# print(f"Age: {age} years")

def calculate_bmi(height, weight):
    return weight / (height ** 2)