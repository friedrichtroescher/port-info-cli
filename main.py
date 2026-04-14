#!/usr/bin/env python3
import sys
import os

from data_manager import DataManager
from argument_parser import parse_arguments
from command_handlers import handle_get, handle_edit, handle_reset, handle_help, handle_list, handle_search


def main():
    """Main entry point for the port CLI tool."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    json_file_path = os.path.join(script_dir, "ports.json")

    if not os.path.exists(json_file_path):
        print("Error: ports.json not found in the script directory.")
        sys.exit(1)

    try:
        data_manager = DataManager(json_file_path)
    except Exception as e:
        print(f"Error initializing data manager: {e}")
        sys.exit(1)

    try:
        command, args = parse_arguments(sys.argv[1:])
    except SystemExit:
        sys.exit(1)

    try:
        if command == "get":
            handle_get(data_manager, args["port"])
        elif command == "edit":
            handle_edit(data_manager, args["port"], args["description"])
        elif command == "reset":
            handle_reset(
                data_manager,
                port=args.get("port"),
                all=args.get("all", False),
                yes=args.get("yes", False),
            )
        elif command == "list":
            handle_list(data_manager)
        elif command == "search":
            handle_search(data_manager, args["term"])
        elif command == "help":
            handle_help(data_manager, args.get("command"))
        else:
            print("Error: Unknown command.")
            handle_help()
            sys.exit(1)
    except KeyboardInterrupt:
        print("\nOperation cancelled.")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
