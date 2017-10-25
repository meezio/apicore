import yaml
import re
from .logger import Logger


class OpenAPI:
    def __init__(self, appname, endpoint="/openapi.json", openApiFile="conf/openapi.yaml"):
        self.endpoint = endpoint
        self._pattern = re.compile(r"<([^<]*:)?([^<]*)>")
        self._replace = r"{\2}"
        self._doc = dict()

        self.spec = dict()
        self.spec["info"] = dict()
        self.spec["info"]["title"] = "{} API Specifications".format(appname)
        self.spec["info"]["version"] = "1.0.0"
        self.spec["paths"] = dict()

        try:
            with open(openApiFile) as f:
                data = yaml.load(f)
                if data:
                    self.spec.update(data)
                Logger.info("'{}' loaded".format(openApiFile))
        except FileNotFoundError:
            pass

        self.spec["openapi"] = "3.0.0"

    def addEndpoint(self, rule, methods, docstring, funcName):
        if docstring:
            clean = re.sub(self._pattern, self._replace, rule)
            self.spec["paths"][clean] = dict()
            common_responses = dict()
            docs = docstring.split("---")

            try:
                once = True
                idx = 0
                for doc in docs:
                    yl = yaml.load(doc)
                    if "responses" in yl:
                        yl["responses"].update(common_responses)
                        self.spec["paths"][clean][methods[idx].lower()] = yl
                        if idx < len(methods) - 1:
                            idx += 1
                    elif once:
                        common_responses = yl.pop('common_responses', dict())
                        self.spec["paths"][clean] = yl
                    once = False
                self._doc[funcName] = self.spec["paths"][clean]
            except:
                Logger.error('"Invalide OpenAPI Spec for endpoint "{}" {}'.format(rule, methods))

    def check(self, function, method):
        try:
            # TODO parcourir la doc pour trouver parameters ou bodydata à valider
            print(self._doc[funcName][method.lower()])
            if "parameters" in self._doc[funcName][method.lower()]:
                pass
            return str(self._doc[funcName][method.lower()])
        except:
            # TODO raise error 500 : OpenAPI Specifications not found
            return "ERROR"

    def fake(self, funcName, method):
        try:
            # TODO parcourir la doc pour trouver une request valide (reponse 200 ou < 300)
            return str(self._doc[funcName][method.lower()]["responses"])
        except:
            # TODO raise error 500 : OpenAPI Specifications not found
            return "Fake data"
