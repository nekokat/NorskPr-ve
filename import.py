from core import Tests, Questions, Answers, User
import json
import xmltodict
import re

def from_json(filename: str) -> dict:
  with open(filename, "r", encoding = "utf-8") as file:
    return json.loads(file.read())


def from_xml(filename: str) -> dict:
  with open(filename, "r", encoding = "utf-8") as file:
    return xmltodict.parse(file.read())


def from_text(filename: str) -> dict:
  with open(filename, "r", encoding = "utf-8") as file:
    s = file.read()

  def header():
    return re.search(r"(?P<text>.+) \((?P<langlevel>.+)\): (?P<Title>.+)\nNumber of questions: (?P<count>\d+)\n\nCreate: (?P<DateCreate>.+)\n\n(?P<FirstName>.+) (?P<LastName>.+), (?P<Username>.+) <(?P<Email>.+)>", s).groupdict()

  def answers(data: dict) -> list:
    return data["Answers"].strip().split("\n\t")
 
  def questions() -> list:      
    data = list(i.groupdict() for i in re.finditer(r"(?P<id>\d+)\) (?P<p>.+)\n(?P<Answers>(?:\t.+\n)+)", s))
    
    return [{
      "-id": question["id"],
      "-type": ["M", "S"][question["Answers"].count("+") == 1],
      "p": question["p"],
      "Answers": {
        "Answer": [
          { 
            "id": answers(question).index(answer),
            "-proper": [False, True][answer[0] == "+"],
            "#text": answer.replace("+", ""),
          } for answer in answers(question)
        ]
      }
    } for question in data
    ]  
    
  data = header()
  return {"Test": {
    "Autor": {attr: data[attr] for attr in ['FirstName', 'LastName', 'Username', 'Email']},
    "DateCreate": data["DateCreate"],
    "Title": data["Title"],
    "Language":{
      '-langlevel': data["langlevel"],
      '#text':data["text"]
    },
    "Body": {
      "Questions": {
        "-count": data["count"],
        "Question": questions()
      }
    }
  }
         }


def import_test(data: dict) -> None:
  attrname = lambda data, attr: [i for i in data.keys() if i.endswith(attr)][0]
  
  test = Tests()
  test.title = data["Test"]["Title"]
  lang = data["Test"]["Language"]
  test.lang = lang["#text"]
  test.lang_level = lang[attrname(lang, "langlevel")]
  
  user = User()
  user.from_dict(data["Test"]["Autor"])
  test.autor = user
  
  questions = data["Test"]["Body"]["Questions"]
  for question in questions["Question"]:
    q = Questions()
    q.id = question[attrname(question, "id")]
    q.title = question["p"]
    q.type = question[attrname(question, "type")]
    answers = question['Answers']
    for answer in answers['Answer']:
      a = Answers()
      a.id = answer[attrname(answer, "id")]
      a.proper = answer[attrname(answer, "proper")]
      a.text = answer["#text"]
      q.add(a)
    test.add(q)
  print(test)


import_test(from_text("test.txt"))