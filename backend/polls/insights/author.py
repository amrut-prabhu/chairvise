import csv
import codecs
import pycountry
from collections import Counter
import pycountry

from ..utils import parseCSVFile

def parseAuthorCSVFile(inputFile, mapping):

	csvFile = inputFile
	dialect = csv.Sniffer().sniff(codecs.EncodedFile(csvFile, "utf-8").read(1024))
	csvFile.open()
	# reader = csv.reader(codecs.EncodedFile(csvFile, "utf-8"), delimiter=',', dialect=dialect)
	reader = csv.reader(codecs.EncodedFile(csvFile, "utf-8"), delimiter=',', dialect='excel')

	rowResults = []
	for index, row in enumerate(reader):
		rowResults.append(row)
		print row
		print type(row)
		if index == 5:
			break

	parsedResult = {}

	return parsedResult


def getAuthorInfo(inputFile, mapping):
	"""
	author.csv: header row, author names with affiliations, countries, emails
	data format:
	submission ID | f name | s name | email | country | affiliation | page | person ID | corresponding?
	"""
	paperIdx = mapping['SubmissionID'] if 'SubmissionID' in mapping else -1
	firstNameIdx = mapping['FirstName'] if 'FirstName' in mapping else -1
	lastNameIdx = mapping['LastName'] if 'LastName' in mapping else -1
	emailIdx = mapping['Email'] if 'Email' in mapping else -1
	countryIdx = mapping['Country'] if 'Country' in mapping else -1
	orgIdx = mapping['Organization'] if 'Organization' in mapping else -1
	webIdx = mapping['Webpage'] if 'Webpage' in mapping else -1
	personIdIdx = mapping['PersonID'] if 'PersonID' in mapping else -1

	parsedResult = {}

	lines = parseCSVFile(inputFile)[1:]
	lines = [ele for ele in lines if ele]

	authorList = []
	for authorInfo in lines:
		# authorInfo = line.replace("\"", "").split(",")
		# print authorInfo
		authorList.append(
			{'name': authorInfo[firstNameIdx] + " " + authorInfo[lastNameIdx], 'country': authorInfo[countryIdx], 'affiliation': authorInfo[orgIdx]})

	authors = [ele['name'] for ele in authorList if
	           ele]  # adding in the if ele in case of empty strings; same applies below

	topAuthors = Counter(authors).most_common(10)
	parsedResult['topAuthors'] = {'labels': [ele[0] for ele in topAuthors], 'data': [ele[1] for ele in topAuthors]}

	countries = [ele['country'] for ele in authorList if ele]
	countryCount = Counter(countries)
	countryCountLabel = []
	countryCountData = []
	for country in countryCount:
		countryCode = ''
		try:
			countryCode = pycountry.countries.get(name=country).alpha_2
		except KeyError:
			continue
		countryCountLabel.append(countryCode)
		countryCountData.append(countryCount[country])

	parsedResult['countryCount'] = {'labels': countryCountLabel, 'data': countryCountData}

	topCountries = countryCount.most_common(10)
	parsedResult['topCountries'] = {'labels': [ele[0] for ele in topCountries],
	                                'data': [ele[1] for ele in topCountries]}

	affiliations = [ele['affiliation'] for ele in authorList if ele]
	topAffiliations = Counter(affiliations).most_common(10)
	parsedResult['topAffiliations'] = {'labels': [ele[0] for ele in topAffiliations],
	                                   'data': [ele[1] for ele in topAffiliations]}
	return {'infoType': 'author', 'infoData': parsedResult}