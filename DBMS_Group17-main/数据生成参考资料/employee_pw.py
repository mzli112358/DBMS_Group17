import pandas as pd
import random
import string

def generate_secret():
    letters = random.choices(string.ascii_lowercase, k=3)
    digits = random.choices(string.digits, k=3)
    secret = letters + digits
    random.shuffle(secret)
    return ''.join(secret)

secrets = [generate_secret() for _ in range(2000)]

df = pd.DataFrame(secrets, columns=['passwords'])
df.to_csv('emploeyees_passwords.csv', index=False)