import csv
import codecs
from collections import Counter

from utils import parseCSVFile, testCSVFileFormatMatching, isNumber, parseSubmissionTime
from insights.author import parseAuthorCSVFile, getAuthorInfo
from insights.review import getReviewInfo
from insights.submission import getSubmissionInfo
from insights.review_score import getReviewScoreInfo
from insights.watchlist import getWatchlistInfo

# Multiple file combinations
from insights.authorAndReview import getAuthorAndReviewInfo
from insights.authorAndSubmission import getAuthorAndSubmissionInfo
from insights.submissionAndReview import getSubmissionAndReviewInfo


def getMappingDict(mappings):
	mappingDict = {}

	for infoType, cols in mappings.iteritems():
		colMappings = {}
		for colData in cols:
			if 'Mapping' in colData:
				colMappings[colData['Mapping']] = colData['column_number']

		mappingDict[infoType] = colMappings

	return mappingDict



def getSingleFileInsights(csvFile, mappings):
	fileName = str(csvFile.name)

	mappingDict = getMappingDict(mappings)

	rowContent = ""
	print "Getting insights for file: ", fileName


	if "Author" in fileName:
		rowContent = getAuthorInfo(csvFile, mappingDict['Author'])
	elif "Review" in fileName:
		rowContent = getReviewInfo(csvFile, mappingDict['Review'])
	elif "Submission" in fileName:
		rowContent = getSubmissionInfo(csvFile, mappingDict['Submission'])
	elif "Review_score" in fileName:
		rowContent = getReviewScoreInfo(csvFile, mappingDict['Review_score'])
	elif "Watchlist" in fileName:
		rowContent = getWatchlistInfo(csvFile, mappingDict['Watchlist'])
	else:
		raise Exception('File uploaded is not supported for insights')
	return rowContent


def getMultipleFileInsights(csvFiles, mappings):
	filesDict = {}
	for csvFile in csvFiles:
		filesDict[csvFile.name] = csvFile

	mappingDict = getMappingDict(mappings)

	rowContent = ""

	if {'Author', 'Review'} <= set(filesDict):
		rowContent = getAuthorAndReviewInfo(filesDict['Author'], filesDict['Review'], mappingDict['Author'], mappingDict['Review'])
	elif {'Author', 'Submission'} <= set(filesDict):
		rowContent = getAuthorAndSubmissionInfo(filesDict['Author'], filesDict['Submission'], mappingDict['Author'], mappingDict['Submission'])
	elif {'Submission', 'Review'} <= set(filesDict):
		rowContent = getSubmissionAndReviewInfo(filesDict['Submission'], filesDict['Review'], mappingDict['Submission'], mappingDict['Review'])
	else:
		raise Exception('File combination uploaded is not supported for insights')

	return rowContent


if __name__ == "__main__":
	parseCSVFile(fileName)
