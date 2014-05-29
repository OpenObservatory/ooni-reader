# ooni-reader

The purpose of this tool is to process and convert ooni-probe YAML formatted
reports into other data formats.

The tool is particularly useful to identify significant reports that could be a
symptom of internet censorship.

## Usage

To convert a set of ooni-probe reports from `.yamloo` format to `.csv` you can run:

```
./bin/oonireader -t csv -o my_report.csv /path/to/report-something.yamloo
```

You can also specify multiple reports like so:

```
./bin/oonireader -t csv -o my_report.csv /path/to/report-http_requests*
```

When running the tool on multiple reports they must all be of the same format.

## Output format

All of the generated output data will always have some data inside of them and that is:

```
probe_asn,probe_cc,probe_ip,software_name,software_version,start_time,test_name,test_version,data_format_version,input,interesting
```

Most of these values are self explanatory, if their meaning is not clear to
you, you should check out the [ooni data format specification](https://github.com/TheTorProject/ooni-spec/tree/master/data-formats).

The perhaps most interesting value that is added is called `interesting`. This
indicates that ooni-reader has flagged that particular report entry as one of
particular significance. This means that such report entry could be a symptom
of internet censorship and special attention should be placed to it.

The rest of the entries depend on the test specific data format.
