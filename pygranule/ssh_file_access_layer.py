from pygranule.file_access_layer import FileAccessLayer, FileAccessLayerError
import paramiko
import stat

class SSHFileAccessLayer(FileAccessLayer):
    
    __implements__ = (FileAccessLayer,)

    def __init__(self, hostname, username, password=None, port=22):
        FileAccessLayer.__init__(self)
        self.hostname = hostname
        self.username = username
        self.port = port
        self.password = password

    def list_source_directory(self, directory):
        directory = directory.rstrip("/")
        files = []
        try:
            t = paramiko.Transport((self.hostname, self.port))
            try:
                t.connect(username=self.username, password=self.password)
                sftp = paramiko.SFTPClient.from_transport(t)
                
                for x in sftp.listdir_attr(directory):
                    if stat.S_IFMT(x.st_mode) != stat.S_IFDIR:
                        files.append(directory + "/" + x.filename)
            finally:
                t.close()
        except:
            raise FileAccessLayerError("Failed to list source")

        return files

    def copy_file(self, source, destination):
        pass

    def remove_source_file(self, filename):
        pass

    def check_for_source_file(self, filename):
        pass
