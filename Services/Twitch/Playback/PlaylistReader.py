import re


class PlaylistTag:
    def __init__(self, name, data):
        self.name = name
        self.data = data

    def toString(self):
        if isinstance(self.data, dict):
            return f"#{self.name}:{','.join(f'{key}={value}' for key, value in self.data.items())}"
        elif isinstance(self.data, list):
            return f"#{self.name}:{','.join(self.data)}"
        else:
            return f"#{self.name}"


class PlaylistReader:
    TAG_WITH_DATA = re.compile("#(.*?):(.*)")
    TAG_WITHOUT_DATA = re.compile("#(.*)")

    def getTag(self, string):
        tag = re.match(self.TAG_WITH_DATA, string)
        if tag == None:
            tag = re.match(self.TAG_WITHOUT_DATA, string)
            if tag == None:
                return None
            else:
                return PlaylistTag(tag.group(1), None)
        else:
            return PlaylistTag(tag.group(1), self.getTagData(tag.group(2)))

    def getTagData(self, line):
        if "=" in line and not self.startsWithQuotation(line):
            tagData = self.parseDictString(line)
        else:
            tagData = self.parseListString(line)
        return tagData

    def startsWithQuotation(self, string):
        return string.startswith("\'") or string.startswith("\"")

    def parseListString(self, line):
        parsedLine = line.split(",")
        quotation = None
        data = []
        for string in parsedLine:
            if quotation == None:
                quotation = string[0] if self.startsWithQuotation(string) else None
                data.append(string)
                if quotation == None:
                    continue
            else:
                data[-1] = ",".join((data[-1], string))
            if string.endswith(quotation):
                data[-1] = data[-1].strip("\'\"").replace(f"\\{quotation}", quotation)
                quotation = None
        return data

    def parseDictString(self, line):
        parsedLine = line.split(",")
        quotation = None
        data = {}
        for string in parsedLine:
            if quotation == None:
                key, value = string.split("=", 1)
                quotation = value[0] if self.startsWithQuotation(value) else None
                data[key] = value
                if quotation == None:
                    continue
            else:
                value = string
                data[key] = ",".join((data[key], value))
            if value.endswith(quotation):
                data[key] = data[key].strip("\'\"")
                quotation = None
        return data