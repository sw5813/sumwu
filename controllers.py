import gspread

def overall():
	# Login with your Google account
	gc = gspread.login('summer.wu@yale.edu', '1sum$soc13')

	# Open the first worksheet
	standings = gc.open_by_url("https://docs.google.com/a/yale.edu/spreadsheets/d/1fJ-bIkjFERyPApaGtUb3cvom7rO1bQYrig7Ly0Hy0jM/edit#gid=477165936").sheet1

	# Fetch overall rankings
	overall = standings.range('B3:D15')
	table = []

	for cell in overall:
		val = cell.value
		table.append(val)

	return table