#!/usr/bin/env python3

# Dependencies:
# python3-dnspython

import dns.zone as dz
import dns.query as dq
import dns.resolver as dr
import argparse


NS = dr.Resolver()
Subdomains = []


# Define the AXFR Function
def AXFR(domain, nameserver):

    # Try zone transfer for given domain and namerserver
    try:
        # Perform the zone transfer
        # print("NS: " + nameserver + " - Domain: " + domain)
        axfr = dz.from_xfr(dq.xfr(nameserver, domain), check_origin=False)
        # print(axfr)

        # If zone transfer was successful
        if axfr:
            print("\n[*] Successful Zone Transfer from {}".format(nameserver))

            # Add found subdomains to global 'Subdomain' list
            for record in axfr:
                Subdomains.append("{}.{}".format(record.to_text(), domain))

    # If zone transfer fails
    except Exception as error:

        print(error)
        pass


if __name__ == "__main__":

    # ArgParser - Declare & define arguments

    parser = argparse.ArgumentParser(
        prog="dns-axfr.py",
        epilog="DNS ZT script",
        usage="dns-axfr.py [options] -d <DOMAIN>",
        prefix_chars="-",
        add_help=True,
    )

    parser.add_argument(
        "-d",
        action="store",
        metavar="Domain",
        type=str,
        help="Your target domain. \t(Example: tylerptl.com)",
        required=True,
    )
    parser.add_argument(
        "-n",
        action="store",
        metavar="Nameserver",
        type=str,
        help="Comma seperated list of nameserver(s). \t(Example: ns1.tylerptl.com, ns2.tylerptl.com)",
    )
    parser.add_argument(
        "-v",
        action="version",
        version="DNS-AXFR - v0.1.0",
        help="Displays version info.",
    )

    # Set the vars
    args = parser.parse_args()
    Domain = args.d
    NS.nameservers = list(args.n.split(","))

    if not args.d:
        print("[!!!] Add a target domain...... [!!!] \n")
        print(parser.print_help())
        exit()

    if not args.n:
        print("[!!!] Add a target nameserver...... [!!!]")
        print(parser.print_help())
        exit()

    for nameserver in NS.nameservers:

        # Try AXFR
        AXFR(Domain, nameserver)

    # Print the results
    if Subdomains is not None:
        print("---------- Found Subdomains -----------")

        for subdomain in Subdomains:
            print("{}".format(subdomain))

        print("-------- End of Subdomain List --------")
        print("\n Number of subdomains: ", len(Subdomains))
    else:
        print("No subdomains found.")
        exit()
