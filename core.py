from collections import defaultdict
import json
from lxml import etree
from time import time, strftime, gmtime
from random import shuffle


class Tests:
  def __init__(
    self, title: str = None, lang: str = None, lang_level: str = None
  ) -> None:
    """Create new test"""
    self._qq = defaultdict(int)
    self.qq_count = len(self._qq)
    self._title = title
    self._lang = lang
    self._lang_level = lang
    self._autor = User("Maxim", "Halyapin")
    self._autor.email = "nekokat89@gmail.com"
    self._autor.username = "elurantrop"

  @property
  def lang_level(self) -> str:
    """Retrun language level"""
    return self._lang_level

  @lang_level.setter
  def lang_level(self, level: str) -> None:
    """Retrun language level"""
    self._lang_level = level

  @property
  def title(self) -> str:
    """Retrun Test title"""
    return self._title

  @title.setter
  def title(self, title: str) -> None:
    """Set Test title"""
    self._title = title

  @property
  def lang(self) -> str:
    """Retrun Test lang"""
    return self._lang

  @lang.setter
  def lang(self, lang: str) -> None:
    """Set Test lang"""
    self._lang = lang

  def questions(self) -> str:
    """Return text, numerated list with questions"""
    temp = list(self._qq.values())
    shuffle(temp)
    return "\n".join(f"{q+1}) {temp[q]}" for q in range(len(temp)))

  def add(self, qq):
    """Add questions"""
    self._qq[qq.id] = qq
    self.qq_count += 1
    return self

  def remove(self, id: int) -> None:
    """Remove question"""
    del self.qq[id]
    self.qq_count -= 1

  def save(self):
    self.save_as_xml()
    self.save_as_json()

  def save_as_xml(self) -> etree:
    """Save Test as xmlfile"""
    root = etree.Element("Test")
    autor = etree.SubElement(root, "Autor")
    user = dict(self._autor).items()

    for field, value in user:
      etree.SubElement(autor, field).text = value

    tm = strftime("%A, %d %B %Y %H:%M:%S", gmtime(time() + 10800))
    etree.SubElement(root, "DateCreate").text = tm
    etree.SubElement(root, "Title").text = self.title
    etree.SubElement(root, "Language", langlevel=self.lang_level).text = self.lang
    body = etree.SubElement(root, "Body")
    qq = etree.SubElement(body, "Questions", count=str(self.qq_count))

    questions = list(self._qq.values())
    shuffle(questions)
    for question in questions:
      q = etree.SubElement(
        qq, "Question", id=str(question.id), type=question.type
      )
      etree.SubElement(q, "p").text = question.title

      aa = etree.SubElement(q, "Answers")
      answers = list(question._answers.values())
      shuffle(answers)
      for answer in answers:
        etree.SubElement(
          aa, "Answer", id=str(answer.id), proper=str(answer.proper)
        ).text = answer.text

    tree = etree.ElementTree(root)
    tree.write(
      "schema.xml", encoding="utf-8", pretty_print=True, xml_declaration=True
    )
    return tree

  def save_as_json(self):
    def answer(question):
      answers = list(question._answers.values())
      shuffle(answers)

      return {
        "Answer": [
          {"-id": answer.id,
           "-proper": answer.proper,
           "#text": answer.text
          }
          for answer in answers
        ]
      }

    def question():
      questions = list(self._qq.values())
      shuffle(questions)

      return [
        {
          "-id": question.id,
          "-type": question.type,
          "p": question.title,
          "Answers": answer(question),
        }
        for question in questions
      ]

    data = {
      "Test": {
        "Autor": dict(self._autor),
        "DateCreate": strftime("%A, %d %B %Y %H:%M:%S", gmtime(time() + 10800)),
        "Title": self.title,
        "Language": {"-langlevel": self.lang_level, "#text": self.lang},
        "Body": {"Questions": {"-count": self.qq_count, "Question": question()}},
      }
    }

    with open("test.json", "wb") as file:
      jsondata = json.dumps(data, indent=2, ensure_ascii=False)
      file.write(jsondata.encode("utf-8"))

  def __str__(self) -> str:
    """Printering Test with questions and answers"""
    return f"{self.lang} ({self.lang_level}): {self.title}\nNumber of questions: {self.qq_count}\n\n{self.questions()}"

  def __repr__(self):
    return f"Language: {self._lang}; {self.qq_count} questions"


class Questions:
  count = 0

  def __init__(self, title: str = None, type: str = None) -> None:
    """Create Questions"""
    Answers.count = 0
    self.__class__.count += 1
    self._answers = defaultdict(int)
    self._type = type
    self._title = title
    self._id = self.__class__.count

  def add(self, a):
    """Add Answer"""
    self._answers[a.id] = a
    return self

  def answers(self):
    """Retrun numerated list with answers"""
    temp = list(self._answers.values())
    shuffle(temp)
    return "\n".join(f"\t{chr(q+97)}) {temp[q]}" for q in range(len(temp)))

  @property
  def title(self) -> str:
    """Return Questions's title"""
    return self._title

  @property
  def id(self) -> int:
    """Return Questions's id"""
    return self._id

  @property
  def type(self) -> str:
    """Return Questions's type"""
    return self._type

  @type.setter
  def type(self, type: str) -> None:
    """Set Questions's id"""
    self._type = type

  @title.setter
  def title(self, title: str) -> None:
    """Set Questions's title"""
    self._title = title

  @id.setter
  def id(self, id: int) -> None:
    """Set Questions's id"""
    self._id = id

  def proper(self, id: int) -> None:
    self._answers[id].change_proper()

  def copy(self) -> None:
    """Copy Question"""
    temp = Questions(self.title, self.type)
    temp._answers = self._answers
    return temp

  def __str__(self):
    """Printering question with answers"""
    return f"{self.title} ({self.type})\n{self.answers()}\n"

  def __repr__(self):
    """Representation question with answers"""
    return f"{self.title}({self.type})"


class Answers:
  count = 0

  def __init__(self, text: str = None):
    self.__class__.count += 1
    self._text = text
    self._id = self.__class__.count
    self._proper = False

  @property
  def id(self):
    """Return Answers's id"""
    return self._id
    
  @id.setter
  def id(self, id: int):
    """Set Answers's id"""
    self._id = id
    
  @property
  def text(self):
    """Return Answers's text"""
    return self._text

  @text.setter
  def text(self, text: str):
    """Set Answers's text"""
    self._text = text

  @property
  def proper(self):
    """Return proper"""
    return self._proper

  @proper.setter
  def proper(self, proper: str):
    """Set proper as [True, False]"""
    self._proper = proper

  def change_proper(self):
    """Change proper"""
    self._proper = not self._proper
    return self

  def __str__(self):
    """Printering answer"""
    return f"{self._text}"

  def __repr__(self):
    """Representation answer"""
    return f"Ansvers(id {self._id})"


class User:
  def __init__(self, name: str = None, last_name: str = None) -> None:
    self._name = name
    self._last_name = last_name
    self._email = None
    self._username = None

  @property
  def email(self) -> str:
    return self._email

  @email.setter
  def email(self, email: str) -> None:
    self._email = email

  @property
  def username(self) -> str:
    return self._username

  @username.setter
  def username(self, username: str) -> None:
    self._username = username

  def __iter__(self) -> None:
    self_iter = (
      ("FirstName", self._name),
      ("LastName", self._last_name),
      ("Username", self._username),
      ("Email", self._email),
    )
    return iter(self_iter)

  def from_dict(self, data) -> None:
    self._name, self._last_name, self._usernam,self._email = dict(data).values()

  def __str__(self) -> str:
    return "{} {}, {} <{}>".format(*dict(self).values())

  def __repr__(self) -> str:
    return str(dict(self))
