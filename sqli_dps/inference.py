import joblib
import pkg_resources


def get_package_file(filename: str) -> str:
    return pkg_resources.resource_filename("sqli_dps", filename)


model_path = get_package_file("model.pkl")
pipeline = joblib.load(model_path)


class PotentialSQLiPayload(Exception):
    def __init__(self, message="You have a Potential SQL payload in your data"):
        self.message = message
        super().__init__(self.message)


class SQLi:
    @staticmethod
    def _classify(text):
        prediction = pipeline.predict([text])
        if prediction[0] == 1:
            raise PotentialSQLiPayload(f"{text} is a potential payload.")
        else:
            return prediction[0]

    @staticmethod
    def check(data):
        if isinstance(data, str):
            SQLi._classify(data)
        elif isinstance(data, list):
            for value in data:
                SQLi._classify(value)
        elif isinstance(data, dict):
            for value in data.values():
                SQLi._classify(value)

    @staticmethod
    def parse(data, error="potential payload"):
        assert isinstance(data, dict), "Dictionary expected"
        cleaned = {}
        for key, value in data.items():
            try:
                SQLi._classify(value)
                cleaned[key] = value
            except PotentialSQLiPayload:
                cleaned[key] = error
        return cleaned


SQLi.check(" or pg_sleep ( __TIME__ ) --")
