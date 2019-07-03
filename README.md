# manytables

## install

:warning: not uploaded yet (TODO task)

```console
$ pip install manytables
```

## how to use

```console
$ manytables init
INFO:manytables.configuration:create manytables.toml, as config file.

$ manytables clone --type spreadsheet https://docs.google.com/spreadsheets/d/xxxXXXXxxxxxXxXxxXxXXXxxxXxXXxxxxXxXXXxXxXxx/edit
INFO:manytables.csvdb:database: manytables
INFO:manytables.csvdb:table: manytables/Group
INFO:manytables.csvdb:table: manytables/Member

$ manytables show manytables
INFO:manytables.cli:database: manytables
INFO:manytables.cli:table: Group
"id"	"name"
"1"	"A"
"2"	"B"
"3"	"C"
"4"	"D"

INFO:manytables.cli:table: Member
"id"	"name"	"group_id"
"1"	"x"	"1"
"2"	"y"	"2"
"3"	"z"	"1"
"4"	"i"	"1"
"5"	"j"	"2"

$ manytables pull manytables
INFO:manytables.csvdb:database: manytables
INFO:manytables.csvdb:table: manytables/Group
INFO:manytables.csvdb:table: manytables/Member

$ manytables push --type spreadsheet manytables
INFO:manytables.cli:push database: manytables
INFO:manytables.spreadsheetdb:save_db, update spreadsheet 'manytables', url=https://docs.google.com/spreadsheets/d/xxxXXXXxxxxxXxXxxXxXXXxxxXxXXxxxxXxXXXxXxXxx/edit
INFO:manytables.spreadsheetdb:update cells len=10, in <Spreadsheet 'manytables' id:xxxXXXXxxxxxXxXxxXxXXXxxxXxXXxxxxXxXXXxXxXxx>
INFO:manytables.spreadsheetdb:update cells len=21, in <Spreadsheet 'manytables' id:xxxXXXXxxxxxXxXxxXxXXXxxxXxXXxxxxXxXXXxXxXxx>
INFO:manytables.csvdb:save metadata: 'manytables/metadata.toml'

# save as other sheet (make a copy)
$ manytables push --type spreadsheet --name=manytables2
```
