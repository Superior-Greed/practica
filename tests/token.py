import json
class tokenJson():
    def token_save(user_parse):
        json_object = json.dumps({"Authorization": "Bearer {0}".format(user_parse.token)}, indent=4)
        with open("tests/token.json", "w") as outfile:
            outfile.write(json_object)
    
    def token_read():
        with open("tests/token.json", "r") as openfile:
            return json.load(openfile)

