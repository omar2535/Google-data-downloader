import email

class EmailParser:
    def get_subject(self, msg):
        return msg['subject']

    def get_from(self, msg):
        return msg['from']

    def get_to(self, msg):
        return msg['to']

    # TODO: get body contents
    def get_body(self, msg):
        if msg.is_multipart():
            for load in msg.get_payload():
                pass
        else:
            return msg.get_payload()