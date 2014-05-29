import pprint


class Entry(object):
    def __init__(self, entry):
        self.entry = entry

    def output_fields(self):
        try:
            test_input = self.entry['input']
        except KeyError:
            test_input = None
        return {
            'input': test_input,
            'interesting': self.entry_filter()
        }

    def entry_filter(self):
        return False

    @property
    def interesting(self):
        return self.entry_filter()

    def __getattr__(self, attr):
        try:
            v = self.entry[attr]
            return v
        except KeyError:
            return None

    def __str__(self):
        return pprint.pformat(self.entry)

    def get_fields(self):
        return self.output_fields().values()


class HTTPT(Entry):

    def __str__(self):
        data = self.entry.copy()
        data['requests'] = []
        for request in self.entry['requests']:
            if 'response' not in request:
                continue
            request['response']['body'] = request['response']['body'][:50]
            data['requests'].append(request)
        return pprint.pformat(data)


class DNST(Entry):
    pass


class TCPT(Entry):
    pass


class Scapy(Entry):
    pass
