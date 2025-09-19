import json
import random
import string

def generate_valid_username(base_name, index):
    """
    Generate username yang valid: hanya huruf, angka, underscore
    """
    # Hapus karakter khusus dan pastikan hanya alfanumeric + underscore
    clean_name = ''.join(c for c in base_name if c.isalnum() or c == '_')
    return f"{clean_name}_{index}"

def generate_valid_ktp(index):
    """
    Generate nomor KTP yang valid: hanya angka 16 digit
    """
    base_ktp = "122121020102"  # 12 digit pertama
    sequential = str(index).zfill(4)  # 4 digit sequential
    return base_ktp + sequential

def generate_valid_email(base_email, index):
    """
    Generate email yang valid
    """
    return f"{base_email}{index}@gmail.com"

def generate_users(num_users):
    users = []
    for i in range(1, num_users + 1):
        username = generate_valid_username("tofankamil", i)
        email = generate_valid_email("tovan.kamil", i)
        ktp = generate_valid_ktp(i)
        
        user = {
            "username": username,
            "password": "password123",
            "sponsor_username": "jhonlenon23",
            "email": email,
            "phone_number": f"08229230{1000 + i}",
            "address": f"Jl Tebet No {i}",
            "province": "DKI Jakarta",
            "city": "Jakarta",
            "district": "Pancoran",
            "postal_code": "12780",
            "ktp": ktp
        }
        users.append(user)
    return users

# Generate 1000 users
users_data = generate_users(1000)

# Save to JSON file
with open('users_data.json', 'w') as f:
    json.dump(users_data, f, indent=2)

print("Generated 1000 valid users in users_data.json")
print("Contoh data pertama:")
print(json.dumps(users_data[0], indent=2))