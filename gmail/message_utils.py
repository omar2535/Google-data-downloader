from apiclient import errors
import base64
import email
import pdb

class MessageUtils:
    def list_messages_matching_query(self, user_id, service, query=''):
        """List all Messages of the user's mailbox matching the query.

        Args:
            service: Authorized Gmail API service instance.
            user_id: User's email address. The special value "me"
            can be used to indicate the authenticated user.
            query: String used to filter messages returned.
            Eg.- 'from:user@some_domain.com' for Messages from a particular sender.

        Returns:
            List of Messages that match the criteria of the query. Note that the
            returned list contains Message IDs, you must use get with the
            appropriate ID to get the details of a Message.
        """
        try:
            response = service.users().messages().list(userId = user_id).execute()
            messages = []
            if 'messages' in response:
                messages.extend(response['messages'])

                while 'nextPageToken' in response:
                    page_token = response['nextPageToken']
                    response = service.users().messages().list(userId = user_id, q=query, pageToken=page_token).execute()
                    messages.extend(response['messages'])
            return messages
        except errors.HttpError as error:
            print('An error occured: ' + error)
        
    def list_messages_with_labels(self, user_id, service, label_ids = []):
        """List all Messages of the user's mailbox with label_ids applied.

        Args:
            service: Authorized Gmail API service instance.
            user_id: User's email address. The special value "me"
            can be used to indicate the authenticated user.
            label_ids: Only return Messages with these labelIds applied.

        Returns:
            List of Messages that have all required Labels applied. Note that the
            returned list contains Message IDs, you must use get with the
            appropriate id to get the details of a Message.
        """
        try:
            response = service.users().messages().list(user_id=user_id, labelIds=label_ids).execute()
            messages = []
            if 'messages' in response:
                messages.extend(response['messages'])

            while 'nextPageToken' in response:
                page_token = response['nextPageToken']
                response = service.users().messages().list(userId=user_id, labelIds=label_ids, pageToken=page_token).execute()
                messages.extend(response['messages'])

            return messages
        except errors.HttpError as error:
            print('An error occurred: ' + error)

    def get_message(self, service, user_id, msg_id):
        """gets message with given id
        Args:
            service: authorized gmail api service instance
            user_id: User's email address
            msg_id: message id
        
        Returns:
            A message
        """
        try:
            message = service.users().messages.get(userId=user_id, id=msg_id).execute()
            return message
        except errors.HttpError as error:
            print('An error occured: ' + error)

    def get_mime_message(self, service, user_id, msg_id):
        """Get a Message and use it to create a MIME Message.

        Args:
            service: Authorized Gmail API service instance.
            user_id: User's email address. The special value "me"
            can be used to indicate the authenticated user.
            msg_id: The ID of the Message required.

        Returns:
            A MIME Message, consisting of data from Message.
        """
        try:
            message = service.users().messages().get(userId=user_id, id=msg_id,
                                                    format='raw').execute()
            msg_str = base64.urlsafe_b64decode(message['raw'].encode('ASCII'))
            mime_msg = email.message_from_bytes(msg_str)
            return mime_msg
        except errors.HttpError as error:
            print('An error occurred: ' + error)
    
    def get_attachments_from_message(self, service, user_id, msg_id, store_dir):
        """Get and store attachment from Message with given id.

        Args:
            service: Authorized Gmail API service instance.
            user_id: User's email address. The special value "me"
            can be used to indicate the authenticated user.
            msg_id: ID of Message containing attachment.
            store_dir: The directory used to store attachments.
        """
        breakpoint()
        try:
            message = service.users().messages().get(userId=user_id, id=msg_id).execute()
            breakpoint()
            for part in message['payload']['parts']:
                if(part['filename']):

                    file_data = base64.urlsafe_b64decode(part['body']['data']
                                                        .encode('UTF-8'))

                    path = ''.join([store_dir, part['filename']])
                    breakpoint()
                    f = open(path, 'w')
                    f.write(file_data)
                    f.close()

        except errors.HttpError as error:
            print('An error occurred: ' + error)
