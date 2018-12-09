import csv
import codecs
from collections import Counter

from ..utils import parseCSVFile
from review import getEvaluation


def getAuthorAndReviewInfo(authorFile, reviewFile, authorMapping, reviewMapping):
	"""
	author.csv: header ele, author names with affiliations, countries, emails
	data format:
	submission ID | f name | s name | email | country | affiliation | page | person ID | corresponding?

	review.csv
	data format:
	review ID | paper ID | reviewer ID | reviewer name | unknown | text | scores | overall score | unknown | unknown | unknown | unknown | date | time | recommend
	File has NO header
	"""

	a_paperIdx = authorMapping['SubmissionID'] if 'SubmissionID' in authorMapping else -1
	a_firstNameIdx = authorMapping['FirstName'] if 'FirstName' in authorMapping else -1
	a_lastNameIdx = authorMapping['LastName'] if 'LastName' in authorMapping else -1
	a_emailIdx = authorMapping['Email'] if 'Email' in authorMapping else -1
	a_countryIdx = authorMapping['Country'] if 'Country' in authorMapping else -1
	a_orgIdx = authorMapping['Organization'] if 'Organization' in authorMapping else -1
	a_webIdx = authorMapping['Webpage'] if 'Webpage' in authorMapping else -1
	a_personIdIdx = authorMapping['PersonID'] if 'PersonID' in authorMapping else -1

	r_revId = reviewMapping['ReviewID'] if 'ReviewID' in reviewMapping else -1
	r_paperId = reviewMapping['SubmissionID'] if 'SubmissionID' in reviewMapping else -1
	r_reviewerId = reviewMapping['ReviewAssignID'] if 'ReviewAssignID' in reviewMapping else -1
	r_reviewerName = reviewMapping['Name'] if 'Name' in reviewMapping else -1
	r_fieldId = reviewMapping['FieldID'] if 'FieldID' in reviewMapping else -1
	r_comment = reviewMapping['Comments'] if 'Comments' in reviewMapping else -1
	r_evaluationIdx = reviewMapping['Evaluation'] if 'Evaluation' in reviewMapping else -1
	r_date = reviewMapping['Date'] if 'Date' in reviewMapping else -1
	r_time = reviewMapping['Time'] if 'Time' in reviewMapping else -1
	r_recommend = reviewMapping['Recommendation'] if 'Recommendation' in reviewMapping else -1

	parsedResult = {}

	# ------------- Parse author.csv -------------
	authorLines = parseCSVFile(authorFile)[1:]
	authorLines = [ele for ele in authorLines if ele]

	authorCountry = {(ele[a_firstNameIdx] + " " + ele[a_lastNameIdx]).strip(): ele[a_countryIdx].strip() for ele in authorLines if ele}
	authorOrganisation = {(ele[a_firstNameIdx] + " " + ele[a_lastNameIdx]).strip(): ele[a_orgIdx].strip() for ele in authorLines if ele}

	# {paperId: [list of authors]}
	paperAuthors = {}
	for ele in authorLines:
		paperId = ele[a_paperIdx]
		author = ele[a_firstNameIdx].strip() + " " + ele[a_lastNameIdx].strip()
		if paperId in paperAuthors:
			paperAuthors[paperId].append(author)
		else:
			paperAuthors[paperId] = [author]

	# {country: {'scores': [], 'confidences': []}}
	countryReviews = {ele[a_countryIdx].strip(): {'scores': [], 'confidences': []}for ele in authorLines if ele}

	# {organisation: {'scores': [], 'confidences': []}}
	organisationReviews = {ele[a_orgIdx].strip(): {'scores': [], 'confidences': []}for ele in authorLines if ele}
  
	# ------------- Parse review.csv -------------
	reviewLines = parseCSVFile(reviewFile)[0:]
	reviewLines = [ele for ele in reviewLines if ele]

	# ------------- Generate insights -------------
	for ele in reviewLines:
		# Authors of this submission
		authors = paperAuthors[ele[r_paperId]]

		score, confidence, isRecommended = getEvaluation(str(ele[r_evaluationIdx]).replace("\r", ""))

		for author in authors:
			if author not in authorCountry or authorCountry[author] not in countryReviews:
				continue
			else:
				# Append score and confidence to list
				countryReviews[authorCountry[author]]['scores'].append(score)
				countryReviews[authorCountry[author]]['confidences'].append(confidence)

			if author not in authorOrganisation or authorOrganisation[author] not in organisationReviews:
				continue
			else:
				# Append score and confidence to list
				organisationReviews[authorOrganisation[author]]['scores'].append(score)
				organisationReviews[authorOrganisation[author]]['confidences'].append(confidence)

	# List of tuples sorted by decreasing average score- [(author, weighted score)]
	countryScores = getSortedByScore(countryReviews)
	organisationScores = getSortedByScore(organisationReviews)

	# ------------- Combination insights -------------
	parsedResult['countryScores'] = countryScores
	parsedResult['organisationScores'] = organisationScores

	return {'infoType': 'author&review', 'infoData': parsedResult}


def getSortedByScore(reviewsDict):
	sortedRes = sorted(reviewsDict.iteritems(), key=lambda (k, v): k)  # Sort alphabetically first

	scores = []
	for x in sortedRes:
		score = sum(x * y for x, y in zip(x[1]['scores'], x[1]['confidences'])) / max(1, sum(x[1]['confidences']))
		scores.append((x[0], score))
	scores = sorted(scores, key=lambda x: x[1], reverse=True)
	return scores
