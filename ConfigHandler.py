class ConfigHandler:
    @staticmethod
    def read_file(filename):
        try:
            with open(filename, 'r') as file:
                return file.readlines()
        except Exception as e:
            print(e)
            exit(11)