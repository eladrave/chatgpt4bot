import dbhandler

def clear_replit_db():
    if dbhandler.db_type == 'replit':
        keys_to_delete = []

        # Collect all the keys to delete
        for key in dbhandler.db.keys():
            keys_to_delete.append(key)

        # Delete keys
        for key in keys_to_delete:
            del dbhandler.db[key]

        print("Replit DB has been cleared.")
    else:
        print("Database type is not Replit, aborting operation.")

def display_db():
    if dbhandler.db_type == 'replit':
        print("Replit DB contents:")
        for key in dbhandler.db.keys():
            print(f"{key}: {dbhandler.db[key]}")
    else:
        print("Database type is not Replit, aborting operation.")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Replit DB Manager")
    parser.add_argument('--clear', action='store_true', help="Clear the Replit DB")
    parser.add_argument('--display', action='store_true', help="Display the Replit DB contents")

    args = parser.parse_args()

    if args.clear:
        clear_replit_db()
    elif args.display:
        display_db()
    else:
        parser.print_help()
