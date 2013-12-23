import boto

import urllib2


def main(access_key, secret_key, zone, record):
    route = boto.connect_route53(
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key
    )
    try:
        zone = route.get_zone(zone)
    except boto.route53.exception.DNSServerError:
        print 'Invalid security tokens'
    else:
        if zone is None:
            print 'Zone %s not found!' % zone
        else:
            current_record = zone.get_a(record)
            if current_record is None:
                print 'Record %s not found!' % record
            else:
                external_ip = urllib2.urlopen('http://ipecho.net/plain').read()
                if current_record.to_print() != external_ip:
                    print 'Update needed. New IP: %s' % external_ip
                    zone.update_a(record, external_ip)
                    print 'Record updated'
                else:
                    print 'No update needed'


if __name__ == '__main__':
    import sys

    import gflags

    gflags.DEFINE_string('aws_access_key_id', None, 'Amazon Access Key')
    gflags.DEFINE_string('aws_secret_access_key', None, 'Amazon Secret Key')
    gflags.DEFINE_string('zone', None, 'Route53 zone name')
    gflags.DEFINE_string('record', None, 'Route53 A record name')
    gflags.MarkFlagAsRequired('aws_access_key_id')
    gflags.MarkFlagAsRequired('aws_secret_access_key')
    gflags.MarkFlagAsRequired('zone')
    gflags.MarkFlagAsRequired('record')

    try:
        gflags.FLAGS(sys.argv)
    except gflags.FlagsError, e:
        print '%s\\nUsage: %s ARGS\\n%s' % (e, sys.argv[0], gflags.FLAGS)
        sys.exit(1)

    main(
        gflags.FLAGS.aws_access_key_id,
        gflags.FLAGS.aws_secret_access_key,
        gflags.FLAGS.zone,
        gflags.FLAGS.record
    )
