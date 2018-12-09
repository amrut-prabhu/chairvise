import csv
import codecs
from collections import Counter

from ..utils import parseCSVFile


def getAuthorAndSubmissionInfo(authorFile, submissionFile, authorMapping, subMapping):
	"""
	author.csv: header row, author names with affiliations, countries, emails
	data format:
	submission ID | f name | s name | email | country | affiliation | page | person ID | corresponding?

	submission.csv
	data format:
	submission ID | track ID | track name | title | authors | submit time | last update time | form fields | keywords | decision | notified | reviews sent | abstract
	File has header
	"""

	a_paperIdx = authorMapping['SubmissionID'] if 'SubmissionID' in authorMapping else -1
	a_firstNameIdx = authorMapping['FirstName'] if 'FirstName' in authorMapping else -1
	a_lastNameIdx = authorMapping['LastName'] if 'LastName' in authorMapping else -1
	a_emailIdx = authorMapping['Email'] if 'Email' in authorMapping else -1
	a_countryIdx = authorMapping['Country'] if 'Country' in authorMapping else -1
	a_orgIdx = authorMapping['Organization'] if 'Organization' in authorMapping else -1
	a_webIdx = authorMapping['Webpage'] if 'Webpage' in authorMapping else -1
	a_personIdIdx = authorMapping['PersonID'] if 'PersonID' in authorMapping else -1

	s_paperIdx = subMapping['SubmissionID'] if 'SubmissionID' in subMapping else -1
	s_trackIdx = subMapping['TrackId'] if 'TrackId' in subMapping else -1
	s_trackNameIdx = subMapping['TrackName'] if 'TrackName' in subMapping else -1
	s_titleIdx = subMapping['Title'] if 'Title' in subMapping else -1
	s_authorsIdx = subMapping['Authors'] if 'Authors' in subMapping else -1
	s_timeIdx = subMapping['Time'] if 'Time' in subMapping else -1
	s_updateIdx = subMapping['Update'] if 'Update' in subMapping else -1
	s_keywordsIdx = subMapping['KeyWords'] if 'KeyWords' in subMapping else -1
	s_decisionIdx = subMapping['Decision'] if 'Decision' in subMapping else -1
	s_mailIdx = subMapping['Mail'] if 'Mail' in subMapping else -1
	s_reviewIdx = subMapping['Review'] if 'Review' in subMapping else -1
	s_abstractIdx = subMapping['Abstract'] if 'Abstract' in subMapping else -1

	parsedResult = {}

	# ------------- Parse author.csv -------------
	authorLines = parseCSVFile(authorFile)[1:]
	authorLines = [ele for ele in authorLines if ele]

	authorAffiliation = {(ele[a_firstNameIdx] + " " + ele[a_lastNameIdx]).strip(): ele[a_orgIdx] for ele in authorLines if ele}

	# {organisation: {'accepted': {}, 'rejected': {}}}
	organisationPapers = {ele[a_orgIdx].strip(): {'accepted': set(), 'rejected': set()}for ele in authorLines if ele}

	authorCountry = {(ele[a_firstNameIdx] + " " + ele[a_lastNameIdx]).strip(): ele[a_countryIdx] for ele in authorLines if ele}

	# {country: {'accepted': {}, 'rejected': {}}}
	countryPapers = {ele[a_countryIdx].strip(): {'accepted': set(), 'rejected': set()} for ele in authorLines if ele}

	# ------------- Parse submission.csv -------------
	submissionLines = parseCSVFile(submissionFile)[1:]
	submissionLines = [ele for ele in submissionLines if ele]

	# ------------- Generate insights -------------
	for ele in submissionLines:
		# Authors of this submission
		authors = map(str.strip, str(ele[s_authorsIdx]).replace(" and ", ", ").split(","))

		for author in authors:
			if author not in authorAffiliation or authorAffiliation[author] not in organisationPapers:
				continue

			# Add submission id to organisation's and country's set
			org = organisationPapers[authorAffiliation[author]]
			country = countryPapers[authorCountry[author]]

			if ele[s_decisionIdx] == 'accept':
				org['accepted'].add(ele[s_paperIdx])
				country['accepted'].add(ele[s_paperIdx])
			elif ele[s_decisionIdx] == 'reject':
				org['rejected'].add(ele[s_paperIdx])
				country['rejected'].add(ele[s_paperIdx])

			organisationPapers[authorAffiliation[author]] = org
			countryPapers[authorCountry[author]] = country

	acceptedOrg = getSortedByValue(organisationPapers, 'accepted')
	rejectedOrg = getSortedByValue(organisationPapers, 'rejected')

	acceptedCountry = getSortedByValue(countryPapers, 'accepted')
	rejectedCountry = getSortedByValue(countryPapers, 'rejected')

	# ------------- Combination insights -------------
	parsedResult['topAcceptedOrganisations'] = acceptedOrg
	parsedResult['topRejectedOrganisations'] = rejectedOrg

	parsedResult['topAcceptedCountries'] = acceptedCountry
	parsedResult['topRejectedCountries'] = rejectedCountry

	return {'infoType': 'author&submission', 'infoData': parsedResult}

def getSortedByValue(papers, key):
	sortedRes = sorted(papers.iteritems(), key=lambda (k, v): k)  # Sort alphabetically first
	sortedRes = sorted(sortedRes, key=lambda x: len(x[1][key]), reverse=True)
	sortedRes = [(ele[0], len(ele[1][key])) for ele in sortedRes if len(ele[1][key]) > 0]
	return sortedRes
