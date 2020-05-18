from docx import Document


class HebrewDictionary:
    dictionary = None

    @classmethod
    def get_dict(cls):
        if cls.dictionary is None:
            cls.load_dict()
        return cls.dictionary

    @classmethod
    def load_dict(cls):
        cls.dictionary = {}
        with open('hebrew.txt', 'rb') as file:
            is_vowel = False
            for line in file.read().split(b'\r\n'):
                if line == b'vowels:':
                    is_vowel = True
                elif is_vowel:
                    cls.dictionary[chr(line[0])] = line[2:]
                else:
                    cls.dictionary[chr(line[0])] = line[1:]


# read line
def read_line(doc_path):
    document = Document(doc_path)
    dictionary = HebrewDictionary.get_dict()
    for content in document.paragraphs:
        result = ''
        for character in content.text:
            if character in dictionary:
                result += dictionary[character].decode('utf-8')
            else:
                result += character
        print(result)


if __name__ == '__main__':
    filename = 'HelloWorld.docx'
    read_line(filename)
