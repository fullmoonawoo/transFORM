from transFORM import Transform



perform = Transform("source.txt", "Data-Result", separator=":", position=3, jump=2)
#perform.transform()
print(perform.show_data())