import argparse


def create_parser():
    """Create and configure the argument parser."""
    parser = argparse.ArgumentParser(
        prog="port",
        description="A CLI tool to look up TCP/UDP port numbers and their services.",
        epilog='Use "port help" for more information.',
    )

    subparsers = parser.add_subparsers(
        dest="command", help="Available commands", required=False
    )

    # Command: port get <number>
    get_parser = subparsers.add_parser(
        "get",
        help="Display info for a port number.",
    )
    get_parser.add_argument("port", help="The port number (e.g., 22, 443)")

    # Command: port edit <number> <description>
    edit_parser = subparsers.add_parser(
        "edit",
        help="Edit the description for a port.",
    )
    edit_parser.add_argument("port", help="The port number (e.g., 22, 443)")
    edit_parser.add_argument("description", help="The new description")

    # Command: port reset <number>
    reset_parser = subparsers.add_parser(
        "reset",
        help="Reset a port description to its original value.",
    )
    reset_parser.add_argument("port", nargs="?", help="The port number to reset")
    reset_parser.add_argument(
        "--all", action="store_true", help="Reset all custom descriptions"
    )
    reset_parser.add_argument(
        "--yes", "-y", action="store_true", help="Skip confirmation prompt"
    )

    # Command: port list
    subparsers.add_parser("list", help="List all known ports.")

    # Command: port search <term>
    search_parser = subparsers.add_parser(
        "search",
        help="Search ports by service name or description.",
    )
    search_parser.add_argument("term", help="Search term")

    # Command: port help
    subparsers.add_parser("help", help="Display help information.")

    # Positional argument for direct lookup (port <number>)
    parser.add_argument(
        "positional_port",
        nargs="?",
        help="The port number to look up",
    )

    return parser


def parse_arguments(args):
    """Parse command-line arguments.

    Returns:
        tuple: (command, command_args)
    """
    parser = create_parser()

    # Direct port number lookup
    if args and args[0].isdigit():
        return "get", {"port": args[0]}

    parsed_args = parser.parse_args(args)

    if parsed_args.command is None and parsed_args.positional_port:
        return "get", {"port": parsed_args.positional_port}

    if parsed_args.command is None:
        return "help", {}

    command_args = vars(parsed_args)
    command = command_args.pop("command")

    if command == "reset":
        if parsed_args.all:
            command_args.pop("port", None)
        elif not parsed_args.port:
            return "help", {"command": "reset"}

    return command, command_args
