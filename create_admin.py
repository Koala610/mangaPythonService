import sys

from src.repository.mysql import admin_repository


def main():
    if len(sys.argv) < 4:
        print("Usage: python create_admin.py [username] [password] [user_id]")
        return

    # Get the argument value
    username = sys.argv[1]
    password = sys.argv[2]
    user_id = sys.argv[3]
    admin_repository.create(user_id=user_id, username=username, password=password)

if __name__ == "__main__":
    main()