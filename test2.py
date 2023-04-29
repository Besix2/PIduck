from readline import set_completer


s_condition = "Function hallo(123)"
i_condition = s_condition.split()[1]
i_condition = i_condition[:i_condition.find("(")] + "()"
print(i_condition)