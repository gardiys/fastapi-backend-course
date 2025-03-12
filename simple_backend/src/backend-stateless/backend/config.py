import os
import dotenv

dotenv.load_dotenv()


class Configs:
    __x_key = os.getenv('X_MASTER_KEY')


    @property
    def get_secret(self):
        return self.__x_key
