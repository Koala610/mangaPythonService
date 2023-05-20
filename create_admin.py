import sys

from src.repository.mysql import admin_repository


def main():
    if len(sys.argv) < 3:
        print("Usage: python create_admin.py [username] [password]")
        return

    # Get the argument value
    username = sys.argv[1]
    password = sys.argv[2]
    admin_repository.create(username=username, password=password)

if __name__ == "__main__":
    main()