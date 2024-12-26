import os

# Get environment variables
mail_username = os.getenv('MAIL_USERNAME')
mail_password = os.getenv('MAIL_PASSWORD')
mail_default_sender = os.getenv('MAIL_DEFAULT_SENDER')

# Print the values to check if they are set
print(f"MAIL_USERNAME: {mail_username}")
print(f"MAIL_PASSWORD: {mail_password}")
print(f"MAIL_DEFAULT_SENDER: {mail_default_sender}")
