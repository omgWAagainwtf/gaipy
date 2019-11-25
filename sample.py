import gaipy

# Create
DB = 'classify'
create_arg = {
        'title': 'text',
        'content': 'text',
        'post_time': 'time',
        'post_date': 'date',
        'likes': 'num'
    }
weighted_col = [
        'title',
        'content'
    ]
status = Create(DB, create_arg, weighted_col)
print("---Create---")
print(status)
print("------")
print()

# Insert
db = 'test'
record = {
        'title': '好麻煩',
        'content': '好不想寫Usage喔',
        'likes': 1
    }
Insert(db, record, 'json')
Insert(db, record, 'json')
status = Insert(db, record, 'json')
print("---Insert---")
print(status)
print("------")
print()

# Update
db = 'test'
new_record = "@title:啊呀不小心打錯"
status = Update(db, 4, new_record, False)
print("---Update---")
print(status)
print("------")
print()

# Show
print("---Show---")
Show('test')
print("------")
print()

# Select
status = Select('test', {'val': ['好麻煩'], 'col': ['title']})
print("---Select---")
print(status)
print("------")
print()

# Search
db = "test"
keyword = "好,不想"
status = Search(db, keyword, filter_args={'val': ['>0'], 'col': ['likes']})
print("---Search---")
print(status)
print("------")
print()

# Del
status = Del('test', [1, 2, 3])
print("---Del---")
print(status)
print("------")
print()

Drop
status = Drop('test')
print("---Drop---")
print(status)
print("------")
print()

# ExactSearch
status = ExactSearch(DB='classify',pattern="季戰績",col='content')
print("---ExactSearch---")
print(status)
print("------")
print()
