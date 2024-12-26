import smtplib

def test_smtp_connection():
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login('your-email@example.com', 'your-password')
        print("SMTP server connection successful.")
        server.quit()
    except Exception as e:
        print(f"Failed to connect to SMTP server: {e}")

if __name__ == '__main__':
    test_smtp_connection()
