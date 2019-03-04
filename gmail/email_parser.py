import email

class EmailParser:
    def get_subject(self, msg):
        return msg['subject']

    def get_from(self, msg):
        return msg['from']

    def get_to(self, msg):
        return msg['to']

    def get_body(self, msg):
        total_payload = ""
        if msg.is_multipart():
            for load in msg.get_payload():
                total_payload += load
        else:
            total_payload += msg.get_payload()
        return total_payload