import sys
import yaml


def construct_tuple(loader, node):
    return tuple(yaml.SafeLoader.construct_sequence(loader, node))
yaml.SafeLoader.add_constructor(u'tag:yaml.org,2002:seq', construct_tuple)

from .nettests import FORMATS

header_fields = ('options', 'probe_asn', 'probe_cc', 'probe_ip',
                 'software_name', 'software_version', 'start_time',
                 'test_name', 'test_version', 'data_format_version')


class Report(object):

    def __init__(self, report_file):
        self._f = open(report_file)
        self._skipped_line = 0
        self.report_file = report_file
        self.report_document = yaml.safe_load_all(self._f)
        self.parse_header()
        self.detect_nettest_format()

    def close(self):
        self._f.close()

    def parse_header(self):
        """
        Parse the report header.
        """
        entry = self.report_document.next()
        for key in header_fields:
            try:
                entry_value = entry[key]
            except KeyError:
                entry_value = None
            setattr(self, key, entry_value)

    def detect_nettest_format(self):
        try:
            self.nettest_format = FORMATS[self.test_name]
        except KeyError:
            sys.stderr.write("Failed to find %s\n" % self.test_name)
            self.nettest_format = FORMATS["*"]

    def _restart_from_line(self, line_number):
        """
        This is used to skip to the specified line number in case of YAML
        parsing erorrs. We also add to self._skipped_line since the YAML parsed
        will consider the line count as relative to the start of the document.
        """
        self._skipped_line = line_number+self._skipped_line+1
        self._f.seek(0)
        for _ in xrange(self._skipped_line):
            self._f.readline()
        self.report_document = yaml.safe_load_all(self._f)

    def parse_entries(self):
        """
        This is a generator that will return a new instance of
        :class:`oonireader.data_formats.Entry`
        """
        while True:
            try:
                entry = self.report_document.next()
            except StopIteration:
                break
            except Exception as exc:
                self._restart_from_line(exc.problem_mark.line)
                continue
            yield self.parse_entry(entry)

    def parse_entry(self, entry):
        parsed_entry = self.nettest_format(entry)
        return parsed_entry
