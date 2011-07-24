#!/usr/bin/python
"""
Launch new cloud workers

Cloudtask can launch and destroy cloud workers automatically when needed, but
sometimes it can be desirable to launch a persistent pool of workers and manage
it by hand.

Options:

    --apikey      Hub APIKEY
                  Environment: HUB_APIKEY

    --region      Region for instance launch (default: us-east-1)
                  Regions:

                    us-east-1 (Virginia, USA)
                    us-west-1 (California, USA)
                    eu-west-1 (Ireland, Europe)
                    ap-southeast-1 (Singapore, Asia)

    --size        Instance size (default: m1.small)
                  Sizes:

                    t1.micro (1 CPU core, 613M RAM, no tmp storage)
                    m1.small (1 CPU core, 1.7G RAM, 160G tmp storage)
                    c1.medium (2 CPU cores, 1.7G RAM, 350G tmp storage)

    --type        Instance type <s3|ebs> (default: s3)
    --label       Hub description label for all launched servers

Usage example:

    cloudtask-launch-workers 10 workers.txt

"""

import os
import sys
import getopt

from cloudtask import hub

def usage(e=None):
    if e:
        print >> sys.stderr, "error: " + str(e)

    print >> sys.stderr, "Usage: %s [ -opts ] howmany ( path/to/file | - )" % sys.argv[0]
    print >> sys.stderr, __doc__.strip()
    sys.exit(1)

def fatal(e):
    print >> sys.stderr, "error: " + str(e)
    sys.exit(1)

def main():
    kwargs = {
        'region': "us-east-1",
        'size': "m1.small",
        'type': "s3",
        'label': "",
    }

    opt_apikey = os.environ.get('HUB_APIKEY', os.environ.get('CLOUDTASK_APIKEY'))
    
    try:
        opts, args = getopt.getopt(sys.argv[1:], 
                                   'h', [ 'help',
                                          'apikey=' ] + 
                                        [ key + '=' for key in kwargs ])
    except getopt.GetoptError, e:
        usage(e)

    for opt, val in opts:
        if opt in ('-h', '--help'):
            usage()

        if opt == '--apikey':
            opt_apikey = val

        for key in kwargs:
            if opt == '--' + key:
                kwargs[key] = val
                break

    if not opt_apikey:
        fatal("missing required APIKEY")

    if len(args) < 2:
        usage()

    howmany = args[1]

    print `opt_apikey`
    print `kwargs`

if __name__ == "__main__":
    main()
