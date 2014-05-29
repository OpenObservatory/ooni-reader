from .data_formats import HTTPT, DNST, TCPT, Scapy, Entry


class HTTPRequests(HTTPT):
    def output_fields(self):
        of = HTTPT.output_fields(self)
        ks = ('experiment_failure', 'control_failure',
              'body_length_match', 'factor', 'headers_match')
        for k in ks:
            try:
                of[k] = self.entry[k]
            except:
                of[k] = None
        return of

    def entry_filter(self):
        if self.experiment_failure is not None and \
                self.control_failure is None:
            return True
        return False


class DNSConsistency(DNST):
    def output_fields(self):
        of = DNST.output_fields(self)
        ks = ('control_resolver',)
        for k in ks:
            of[k] = self.entry[k]
        return of

    def entry_filter(self):
        if any(t is True
               for t in self.tampering.values()):
            return True
        return False


class HTTPHeaderFieldManipulation(HTTPT):
    def output_fields(self):
        of = HTTPT.output_fields(self)
        ks = ('header_field_name',
              'header_field_number',
              'header_field_value',
              'header_name_capitalization',
              'request_line_capitalization',
              'total')
        for k in ks:
            of['tampering_'+k] = self.entry['tampering'][k]
        return of

    def entry_filter(self):
        if self.tampering['header_field_name'] is not False:
            return True
        if self.tampering['header_field_number'] is not False:
            return True
        if self.tampering['header_field_value'] is not False:
            return True
        if self.tampering['header_name_capitalization'] is not False:
            return True
        if self.tampering['request_line_capitalization'] is not False:
            return True
        if self.tampering['total'] is not False:
            return True
        return False


class HTTPInvalidRequestLine(TCPT):
    def output_fields(self):
        of = TCPT.output_fields(self)
        ks = ('tampering',)
        for k in ks:
            of[k] = self.entry[k]
        return of

    def entry_filter(self):
        return not self.tampering


class TCPConnect(TCPT):
    def output_fields(self):
        of = TCPT.output_fields(self)
        ks = ('connection',)
        for k in ks:
            of[k] = self.entry[k]
        return of

    def entry_filter(self):
        if self.connection != 'success':
            return True
        return False


class CaptivePortal(DNST, HTTPT):
    pass

FORMATS = {
    'captivep': CaptivePortal,
    'captiveportal': CaptivePortal,
    'http_requests_test': HTTPRequests,
    'http_requests': HTTPRequests,
    'dns_consistency': DNSConsistency,
    'httphost': HTTPT,
    'dnsspoof': Scapy,
    'http_header_field_manipulation': HTTPHeaderFieldManipulation,
    'http_invalid_request_line': HTTPInvalidRequestLine,
    'tcp_connect': TCPConnect,
    'multi_protocol_traceroute': Scapy,
    'squid_test': TCPT,
    '*': Entry
}
