import sys


def handle_get(data_manager, port):
    """Display info for a port number."""
    info = data_manager.get_info(port)

    if info is None:
        if not port.isdigit() or int(port) > 65535:
            print(f"Error: Invalid port '{port}'. Valid range is 0-65535.")
        else:
            print(f"Error: Port {port} not found.")
        sys.exit(1)

    protocol = info["protocol"]
    service = info["service"]
    description = info["description"]
    print(f"{port}/{protocol}  {service} - {description}")


def handle_edit(data_manager, port, description):
    """Edit the description for a port."""
    if not port.isdigit():
        print(f"Error: Invalid port '{port}'. Must be a number 0-65535.")
        sys.exit(1)

    info = data_manager.get_info(port)
    if info is None:
        print(f"Error: Port '{port}' not found in the original data.")
        sys.exit(1)

    if data_manager.set_custom_description(port, description):
        print(f"Description for port {port} has been updated.")
    else:
        print(f"Error: Failed to update description for port {port}.")
        sys.exit(1)


def handle_reset(data_manager, port=None, all=False, yes=False):
    """Reset port descriptions."""
    if all:
        if not data_manager.custom_data:
            print("No custom descriptions to reset.")
            return

        if not yes:
            print("Reset all custom descriptions? (yes/NO)")
            confirmation = input().strip().lower()
            if confirmation != "yes":
                print("Operation cancelled.")
                return

        if data_manager.reset_all_custom_descriptions():
            print("All custom descriptions have been reset.")
        else:
            print("Error: Failed to reset custom descriptions.")
            sys.exit(1)
    elif port:
        if not data_manager.has_custom_description(port):
            print(f"Port {port} has no custom description to reset.")
            return

        if data_manager.reset_custom_description(port):
            print(f"Description for port {port} has been reset.")
        else:
            print(f"Error: Failed to reset description for port {port}.")
            sys.exit(1)
    else:
        print("Error: Specify a port number or use --all.")
        sys.exit(1)


def handle_list(data_manager):
    """List all known ports."""
    for key in data_manager.get_all_ports():
        info = data_manager.original_data[key]
        print(f"  {key:<14} {info['protocol']:<10} {info['service']:<20} {info['description']}")


def handle_search(data_manager, term):
    """Search ports by service name or description."""
    term_lower = term.lower()
    results = []

    for key, info in data_manager.original_data.items():
        if (
            term_lower in info["service"].lower()
            or term_lower in info["description"].lower()
        ):
            results.append((key, info))

    if not results:
        print(f"No ports found matching '{term}'.")
        return

    results.sort(key=lambda r: int(r[0].split("-")[0]))
    for key, info in results:
        print(f"  {key:<14} {info['protocol']:<10} {info['service']:<20} {info['description']}")


def handle_help(data_manager=None, command=None):
    """Display help information."""
    if command == "reset":
        print("Usage: port reset <port>")
        print("       port reset --all [--yes]")
        print()
        print("Reset a port description to its original value.")
        print()
        print("Arguments:")
        print("  <port>          The port number to reset")
        print()
        print("Options:")
        print("  --all           Reset all custom descriptions")
        print("  --yes, -y       Skip confirmation prompt")
        return

    print("Port Lookup CLI Tool")
    print()
    print("Usage:")
    print("  port <number>                Look up a port number")
    print("  port edit <number> <desc>    Edit the description for a port")
    print("  port reset <number>          Reset a port description")
    print("  port reset --all [--yes]     Reset all custom descriptions")
    print("  port list                    List all known ports")
    print("  port search <term>           Search by service name or description")
    print("  port help                    Display this help message")
    print()
    print("Examples:")
    print("  port 22                      Look up port 22 (SSH)")
    print("  port 443                     Look up port 443 (HTTPS)")
    print("  port search database         Find database-related ports")
    print("  port list                    Show all known ports")
