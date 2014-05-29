import os
import sys
import csv
import argparse
import cStringIO

from .report import Report, header_fields


class IncompatibleReportFile(Exception):
    pass


class ReportReader(object):

    def __init__(self, report_files, output_file):
        self.report_files = report_files
        self.output_file = output_file
        self._header_written = False
        if self.output_file:
            self.same_output_format()

    def same_output_format(self):
        previous_keys = None
        entry_keys = None
        for report_file in self.report_files:
            if entry_keys:
                previous_keys = entry_keys
            report = Report(report_file)
            try:
                entry = report.parse_entries().next()
            except:
                sys.stderr.write("%s is not a valid report\n" % report_file)
                self.report_files.remove(report_file)
                continue
            entry_keys = entry.output_fields().keys()
            if not previous_keys:
                previous_keys = entry_keys
            elif set(previous_keys) != set(entry_keys):
                raise IncompatibleReportFile(report_file)

            report.close()

    def process_reports(self):
        for report_file in self.report_files:
            report = Report(report_file)
            print "Inspecting at %s" % report_file
            self.process_entries(report)
            report.close()

    def process_entries(self, report):
        for entry in report.parse_entries():
            self.process_entry(entry, report)

    def process_entry(self, entry, report):
        if entry.interesting:
            print "# %s/%s" % (report.probe_cc,
                               os.path.basename(report.report_file))
            print "input: %s" % entry.input
            print str(entry)
            print "---"
        self.process_fields(entry, report)

    def process_fields(self, entry, report):
        if not self._header_written and self.output_file:
            with open(self.output_file, 'a+') as f:
                f.write(self.csv_header_row(entry))
            self._header_written = True

        field_content = str(self.csv_entry_row(report,
                                               entry.output_fields().values()))
        if self.output_file:
            with open(self.output_file, 'a+') as f:
                f.write(field_content)
        else:
            sys.stdout.write(field_content)

    def csv_entry_row(self, report, row):
        row = [report.probe_asn,
               report.probe_cc,
               report.probe_ip,
               report.software_name,
               report.software_version,
               report.start_time,
               report.test_name,
               report.test_version,
               report.data_format_version] + row

        return self.csv_row(row)

    def csv_header_row(self, entry):
        row = list(header_fields) + entry.output_fields().keys()
        row.remove('options')

        return self.csv_row(row)

    def csv_row(self, row):
        output = cStringIO.StringIO()
        writer = csv.writer(output)
        writer.writerow(row)
        output.seek(0)

        return output.read()


def run():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i",
        "--input",
        help="Apply transformations from given file")
    parser.add_argument("-o", "--output", help="Output filename")
    parser.add_argument(
        "-f",
        "--filter-interesting",
        help="Filter the most interesting report entries")
    parser.add_argument("-t", "--format", help="The output format")
    parser.add_argument("reports", help="The report file to parse",
                        nargs='+')
    args = parser.parse_args()

    report_reader = ReportReader(args.reports, args.output)
    report_reader.process_reports()
