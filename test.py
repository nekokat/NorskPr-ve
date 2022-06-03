from core import Tests, Questions, Answers

# Create new test
t = Tests()
t.title = "Norskprøven - Kompetanse Norge"
t.lang = "Norwegian"
t.lang_level = "B1"
q = Questions()
q.title = "Hvilken måned er det nå?"
q.type = "S"
ans = ["Januar", "Mandag", "Uke 13", "Det er jul"]
for a in ans:
  q.add(Answers(a))
q.proper(3)
t.add(q)
q = Questions()
q.title = "Skal vi gå____ og spise på restaurant?"
q.type = "S"
ans = ["inn", "til", "ut", "reise"]
for a in ans:
  q.add(Answers(a))
q.proper(2)
t.add(q)
q = Questions()
q.title = "Hvilken av disse er IKKE en farge?"
q.type = "S"
ans = ["Rosa", "Rød", "Båt", "Gul"]
for a in ans:
  q.add(Answers(a))
q.proper(1)
t.add(q)
#print(t._autor)
print(t._autor)
#print([str(t._autor)])
t.save()