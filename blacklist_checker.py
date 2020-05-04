import dns.resolver
import sys

site = "zen.spamhaus.org"

#function to check whether ip is in the blacklist
def get_info(myIp):
    try:
        my_resolver = dns.resolver.Resolver()
        #we need to reverse the ip address's octets in order to search the ip address in the blacklist
        query = '.'.join(reversed(str(myIp).split("."))) + "." + site
        #find whether the ip address is in the blacklist
        answers = my_resolver.query(query, "A")
        info = getDescriptionOfQuery(answers[0])
        print('The IP address : %s IS found in the following  %s (%s: %s)' % (myIp, site, answers[0], info))
    except dns.resolver.NXDOMAIN: #NXDOMAIN says the query name doesn't exist
        print('The IP address : %s is NOT found in %s' % (myIp, site))

#function to find the ip zone
def getDescriptionOfQuery(resIp):
    temp = str(resIp)
    if temp[-2:-1] != '.' and temp[-2:] == '10':
        return ' - PBL - ISP Maintained'
    elif temp[-2:-1] != '.' and temp[-2:] == '11':
        return ' - PBL - Spamhaus Maintained'
    elif temp[-1] == '2':
        return ' - SBL - Spamhaus SBL Data'
    elif temp[-1] == '3':
        return ' - SBL - Spamhaus SBL CSS Data'
    elif temp[-1] == '4':
        return ' - XBL - CBL Data'
    else:
        return ' - SBL - Spamhaus DROP/EDROP Data'

def main():
    if len(sys.argv) >= 2:
        for i in range(1, len(sys.argv)):
            myIp = sys.argv[i]
            get_info(myIp)
    else:
        print('Next time, please enter ip address. :)')


if __name__ == "__main__":
    main()

