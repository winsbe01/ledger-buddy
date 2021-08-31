import imaplib


class IMAPClient:

    def __init__(self, username, password, server, source_folder):
        self.username = username
        self.password = password
        self.server = server
        self.source_folder = source_folder

    def __open(self):
        M = imaplib.IMAP4_SSL(self.server)
        M.login(self.username, self.password)
        M.select(mailbox=self.source_folder)
        return M

    def __close(self, M):
        M.close()
        M.logout()

    def get_all_message_ids(self):
        M = self.__open()
        typ, data = M.search(None, "ALL")
        self.__close(M)
        return data[0].split()

    def get_message(self, message_id):
        M = self.__open()
        typ, data = M.fetch(message_id, "(BODY[HEADER] BODY[1])")
        header = data[0][1]
        body = data[1][1]
        self.__close(M)
        return header, body
