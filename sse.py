class MyServerSentEvent(object):

    def __init__(self, data):
        self.data = data
        self.event = None
        self.id = None
        self.desc_map = ["data", "event", "id"]

    def encode(self):
        if not self.data:
            return ""
        lines = ["%s: %s" % (k, self.__getattribute__(k))
                 for k in self.desc_map if self.__getattribute__(k)]

        return "%s\n\n" % "\n".join(lines)
