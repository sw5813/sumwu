from keyczar import keyczar
import gspread

def decrypt(ciphertext):
    location = './keys'
    crypter = keyczar.Crypter.Read(location)
    plaintext = crypter.Decrypt(ciphertext)

    return plaintext

def overall():
	# Login with your Google account
	gc = gspread.login(decrypt('AKEQNEBAIOxdrZIPdML6l0bu4Wt6jPKG88td--0KVA5xXluxBSPUlJuIwfvhZzuMKcf3GW1-KUmPyfcWizhQsXzMs8rGZ5zUiQ'), decrypt('AKEQNECl_fi8axz0d1i3t_Z-YmqRowycteVXl3bJGIshMiEcFcB7JaO-gcI6QSRtuvDuP91H2h3t'))

	# Open the first worksheet
	standings = gc.open_by_url("https://docs.google.com/a/yale.edu/spreadsheets/d/1fJ-bIkjFERyPApaGtUb3cvom7rO1bQYrig7Ly0Hy0jM/edit#gid=477165936").sheet1

	# Fetch overall rankings
	overall = standings.range('B3:D15')
	table = []

	for cell in overall:
		val = cell.value
		table.append(val)

	return table