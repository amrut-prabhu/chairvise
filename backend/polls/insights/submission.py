import csv
import codecs
from collections import Counter

from ..utils import parseCSVFile, parseSubmissionTime


def getSubmissionInfo(inputFile, mapping):
	"""
	submission.csv
	data format: 
	submission ID | track ID | track name | title | authors | submit time | last update time | form fields | keywords | decision | notified | reviews sent | abstract
	File has header
	"""

	paperIdx = mapping['SubmissionID'] if 'SubmissionID' in mapping else -1
	trackIdx = mapping['TrackId'] if 'TrackId' in mapping else -1
	trackNameIdx = mapping['TrackName'] if 'TrackName' in mapping else -1
	titleIdx = mapping['Title'] if 'Title' in mapping else -1
	authorsIdx = mapping['Authors'] if 'Authors' in mapping else -1
	timeIdx = mapping['Time'] if 'Time' in mapping else -1
	updateIdx = mapping['Update'] if 'Update' in mapping else -1
	keywordsIdx = mapping['KeyWords'] if 'KeyWords' in mapping else -1
	decisionIdx = mapping['Decision'] if 'Decision' in mapping else -1
	mailIdx = mapping['Mail'] if 'Mail' in mapping else -1
	reviewIdx = mapping['Review'] if 'Review' in mapping else -1
	abstractIdx = mapping['Abstract'] if 'Abstract' in mapping else -1

	parsedResult = {}
	lines = parseCSVFile(inputFile)[1:]
	lines = [ele for ele in lines if ele]
	acceptedSubmission = [line for line in lines if str(line[decisionIdx]) == 'accept']
	rejectedSubmission = [line for line in lines if str(line[decisionIdx]) == 'reject']

	acceptanceRate = float(len(acceptedSubmission)) / len(lines)

	submissionTimes = [parseSubmissionTime(str(ele[timeIdx])) for ele in lines]
	lastEditTimes = [parseSubmissionTime(str(ele[updateIdx])) for ele in lines]
	submissionTimes = Counter(submissionTimes)
	lastEditTimes = Counter(lastEditTimes)
	timeStamps = sorted([k for k in submissionTimes])
	lastEditStamps = sorted([k for k in lastEditTimes])
	submittedNumber = [0 for n in range(len(timeStamps))]
	lastEditNumber = [0 for n in range(len(lastEditStamps))]
	timeSeries = []
	lastEditSeries = []
	for index, timeStamp in enumerate(timeStamps):
		if index == 0:
			submittedNumber[index] = submissionTimes[timeStamp]
		else:
			submittedNumber[index] = submissionTimes[timeStamp] + submittedNumber[index - 1]

		timeSeries.append({'x': timeStamp, 'y': submittedNumber[index]})

	for index, lastEditStamp in enumerate(lastEditStamps):
		if index == 0:
			lastEditNumber[index] = lastEditTimes[lastEditStamp]
		else:
			lastEditNumber[index] = lastEditTimes[lastEditStamp] + lastEditNumber[index - 1]

		lastEditSeries.append({'x': lastEditStamp, 'y': lastEditNumber[index]})

	# timeSeries = {'time': timeStamps, 'number': submittedNumber}
	# lastEditSeries = {'time': lastEditStamps, 'number': lastEditNumber}

	acceptedKeywordList, acceptedKeywordMap = getKeywords(acceptedSubmission, keywordsIdx)
	rejectedKeywordList, rejectedKeywordMap = getKeywords(rejectedSubmission, keywordsIdx)
	allKeywordList, allKeywordMap = getKeywords(lines, keywordsIdx)

	tracks = set([str(ele[trackNameIdx]) for ele in lines])
	paperGroupsByTrack = {track : [line for line in lines if str(line[trackNameIdx]) == track] for track in tracks}
	keywordsGroupByTrack = {}
	acceptanceRateByTrack = {}
	comparableAcceptanceRate = {}
	topAuthorsByTrack = {}

	# Obtained from the JCDL.org website: past conferences
	comparableAcceptanceRate['year'] = [2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018]
	comparableAcceptanceRate['Full Papers'] = [0.29, 0.28, 0.27, 0.29, 0.29, 0.30, 0.29, 0.30]
	comparableAcceptanceRate['Short Papers'] = [0.29, 0.37, 0.31, 0.31, 0.32, 0.50, 0.35, 0.32]
	for track, papers in paperGroupsByTrack.iteritems():
		keywords = [str(ele[8]).lower().replace("\r", "").split("\n") for ele in papers]
		keywords = [ele for item in keywords for ele in item]
		# keywordMap = {k : v for k, v in Counter(keywords).iteritems()}
		keywordMap = [[ele[0], ele[1]] for ele in Counter(keywords).most_common(20)]
		keywordsGroupByTrack[track] = keywordMap

		acceptedPapersPerTrack = [ele for ele in papers if str(ele[decisionIdx]) == 'accept']
		acceptanceRateByTrack[track] = float(len(acceptedPapersPerTrack)) / len(papers)

		acceptedPapersThisTrack = [paper for paper in papers if str(paper[decisionIdx]) == 'accept']
		acceptedAuthorsThisTrack = [str(ele[authorsIdx]).replace(" and ", ", ").split(", ") for ele in acceptedPapersThisTrack]
		acceptedAuthorsThisTrack = [ele for item in acceptedAuthorsThisTrack for ele in item]
		topAcceptedAuthorsThisTrack = Counter(acceptedAuthorsThisTrack).most_common(10)
		topAuthorsByTrack[track] = {'names': [ele[0] for ele in topAcceptedAuthorsThisTrack], 'counts': [ele[1] for ele in topAcceptedAuthorsThisTrack]}

		if track == "Full Papers" or track == "Short Papers":
			comparableAcceptanceRate[track].append(float(len(acceptedPapersPerTrack)) / len(papers))

	acceptedAuthors = [str(ele[authorsIdx]).replace(" and ", ", ").split(", ") for ele in acceptedSubmission]
	acceptedAuthors = [ele for item in acceptedAuthors for ele in item]
	topAcceptedAuthors = Counter(acceptedAuthors).most_common(10)
	topAcceptedAuthorsMap = {'names': [ele[0] for ele in topAcceptedAuthors], 'counts': [ele[1] for ele in topAcceptedAuthors]}
	# topAcceptedAuthors = {ele[0] : ele[1] for ele in Counter(acceptedAuthors).most_common(10)}

	# ------------- submission.csv insights -------------
	parsedResult['acceptanceRate'] = acceptanceRate
	parsedResult['overallKeywordMap'] = allKeywordMap
	parsedResult['overallKeywordList'] = allKeywordList
	parsedResult['acceptedKeywordMap'] = acceptedKeywordMap
	parsedResult['acceptedKeywordList'] = acceptedKeywordList
	parsedResult['rejectedKeywordMap'] = rejectedKeywordMap
	parsedResult['rejectedKeywordList'] = rejectedKeywordList
	parsedResult['keywordsByTrack'] = keywordsGroupByTrack
	parsedResult['acceptanceRateByTrack'] = acceptanceRateByTrack
	parsedResult['topAcceptedAuthors'] = topAcceptedAuthorsMap
	parsedResult['topAuthorsByTrack'] = topAuthorsByTrack
	parsedResult['timeSeries'] = timeSeries
	parsedResult['lastEditSeries'] = lastEditSeries
	parsedResult['comparableAcceptanceRate'] = comparableAcceptanceRate

	return {'infoType': 'submission', 'infoData': parsedResult}


def getKeywords(submission, keywordsIdx):
	'''
	:param submission: List of entries from submission.csv
	:return:
	'''
	keywords = [str(ele[keywordsIdx]).lower().replace("\r", "").split("\n") for ele in submission]
	keywords = [ele for item in keywords for ele in item]
	keywordMap = {k: v for k, v in Counter(keywords).iteritems()}
	keywordList = [[ele[0], ele[1]] for ele in Counter(keywords).most_common(20)]
	return keywordList, keywordMap
