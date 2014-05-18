import ast

# Example provided in the course
from language import astpp

programm = """
x = 3
y = x+4
print(x)
"""

# parsime programmi abstraktseks süntaksipuuks:
puu = ast.parse(programm)
print("Programmi AST:\n", astpp.dump(puu))

# AST-i saab kompileerida ja seejärel käivitada
exec(compile(puu, "<katsetus>", "exec"))

# Ma võin teha puus mingi muudatuse,
# nt. muudan ära esimese omistuslause parema poole
laused = puu.body
laused[0].value = ast.Num(10)

# Python tahab, et kõikide tippude juures on viide lähtekoodile
# aga kuna meie Num(10) ei pärine lähtekoodist, siis laseme Pythonil
# leiutada talle mingi pseudo-asukoha
ast.fix_missing_locations(puu)

# Muudetud puud võin jälle kompileerida ja käivitada
exec(compile(puu, "<katsetus>", "exec"))

print(type(laused[0]))
print(type(laused[1]))
print(type(laused[2]))

