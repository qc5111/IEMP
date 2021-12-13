import os


class Mutilang:
    def GetLang(self, lang):
        if lang in self.LangDict:
            return self.LangDict[lang]
        lang = lang.split("-")[0]
        for key in self.LangDict:
            key1 = key.split("-")[0]
            if lang == key1:
                return self.LangDict[key]
        return self.LangDict["en-us"]  # 无匹配返回英语

    def __init__(self):
        self.LangDict = {}
        LangROotPath = r"IEMP_Satellite/lang"
        for files in os.walk(LangROotPath):
            for file in files[2]:
                LangName = file[:file.rfind(".")]
                fr = open(LangROotPath + "/" + file, "r", encoding="UTF-8")
                self.LangDict[LangName] = {}
                data = fr.read()
                data = data.split("\n")
                for i in data:
                    LangArr = i.split("=")
                    if len(LangArr) == 2:
                        self.LangDict[LangName][LangArr[0]] = LangArr[1]
