# port

A CLI tool to look up TCP/UDP port numbers and their services.

```
$ port 22
22/TCP  SSH - Secure Shell for logins and file transfers

$ port 443
443/TCP/UDP  HTTPS - Hypertext Transfer Protocol Secure

$ port search database
  1433           TCP        MSSQL                Microsoft SQL Server database
  3306           TCP/UDP    MySQL                MySQL database system
  5432           TCP        PostgreSQL           PostgreSQL database
  27017          TCP        MongoDB              MongoDB
```

## Install

Requires [uv](https://docs.astral.sh/uv/).

```bash
git clone https://github.com/friedrichtroescher/port-info-cli.git ~/scripts/port
chmod +x ~/scripts/port/port
# Add to your shell profile:
export PATH="$HOME/scripts/port:$PATH"
```

## Usage

```
port <number>                Look up a port number
port search <term>           Search by service name or description
port list                    List all known ports
port edit <number> <desc>    Override a port's description
port reset <number>          Reset to original description
port help                    Show help
```

## Data

Port data sourced from [Wikipedia's list of TCP and UDP port numbers](https://en.wikipedia.org/wiki/List_of_TCP_and_UDP_port_numbers). Custom descriptions are stored in `~/.config/port-info-cli/`.
