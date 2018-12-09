import csv
import codecs
import operator
from collections import Counter

from ..utils import parseCSVFile
from review import getEvaluation
from submission import getKeywords


def getSubmissionAndReviewInfo(submissionFile, reviewFile, subMapping, reviewMapping):
	"""
	submission.csv
	data format:
	submission ID | track ID | track name | title | authors | submit time | last update time | form fields | keywords | decision | notified | reviews sent | abstract
	File has header

	review.csv
	data format:
	review ID | paper ID | reviewer ID | reviewer name | unknown | text | scores | overall score | unknown | unknown | unknown | unknown | date | time | recommend?
	File has NO header
	"""

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

	# ------------- Parse submission.csv -------------
	submissionLines = parseCSVFile(submissionFile)[1:]
	submissionLines = [ele for ele in submissionLines if ele]

	# Dictionary of submission ID to the submission- {submissionID: submission}
	submissions = {line[s_paperIdx]: line for line in submissionLines}

	# Dictionary of submission ID to list of authors for that submission- {submissionID: [authors of submission]}
	submissionAuthors = {row[s_paperIdx]: map(str.strip, str(row[s_authorsIdx]).replace(" and ", ", ").split(",")) for row in submissionLines}

	# Dictionary of author to scores and confidences given to their submissions- {author: {scores: [], confidences: []}}
	authorScoreDict = {author: {'scores': [], 'confidences': []} for authors in submissionAuthors.itervalues() for author in authors}

	# Dictionary of author to number of their recommended papers- {author: numRecommended}
	recommendedAuthors = {author: 0 for authors in submissionAuthors.itervalues() for author in authors}

	# ------------- Parse review.csv -------------
	reviewLines = parseCSVFile(reviewFile)[0:]
	reviewLines = [ele for ele in reviewLines if ele]
	evaluation = [str(line[r_evaluationIdx]).replace("\r", "") for line in reviewLines]
	submissionIDs = set([str(line[r_paperId]) for line in reviewLines])

	# ------------- Generate insights -------------

	# Idea: from -3 to 3 (min to max scores possible), every 0.25 will be a gap
	scoreDistributionCounts = [0] * int((3 + 3) / 0.25)
	recommendDistributionCounts = [0] * int((1 - 0) / 0.1)

	scoreDistributionLabels = [" ~ "] * len(scoreDistributionCounts)
	recommendDistributionLabels = [" ~ "] * len(recommendDistributionCounts)

	for index, col in enumerate(scoreDistributionCounts):
		scoreDistributionLabels[index] = str(-3 + 0.25 * index) + " ~ " + str(-3 + 0.25 * index + 0.25)

	for index, col in enumerate(recommendDistributionCounts):
		recommendDistributionLabels[index] = str(0 + 0.1 * index) + " ~ " + str(0 + 0.1 * index + 0.1)

	recommendedSubmissions = []
	scoreList = []
	recommendList = []
	confidenceList = []
	submissionIDReviewMap = {}

	for submissionID in submissionIDs:
		# List of Review Scores (overall, confidence, recommend) for the current submission ID
		reviews = [str(line[r_evaluationIdx]).replace("\r", "") for line in reviewLines if str(line[r_paperId]) == submissionID]

		# Authors of this submission
		authors = submissionAuthors[submissionID]

		for review in reviews:
			score, confidence, isRecommended = getEvaluation(review)

			if isRecommended:
				recommendedSubmissions.append(submissions[submissionID])

			for author in authors:
				# Add score and confidence to each author of this submission
				result = authorScoreDict[author]
				result['scores'].append(score)
				result['confidences'].append(confidence)
				authorScoreDict[author] = result

				# Update author's count if the paper was recommended
				if isRecommended:
					recommendedAuthors[author] = recommendedAuthors[author] + 1

		# print reviews
		confidences = [float(review.split("\n")[1].split(": ")[1]) for review in reviews]
		scores = [float(review.split("\n")[0].split(": ")[1]) for review in reviews]

		confidenceList.append(sum(confidences) / len(confidences))
		# recommends = [1.0 for review in reviews if review.split("\n")[2].split(": ")[1] == "yes" else 0.0]
		try:
			recommends = map(lambda review: 1.0 if review.split("\n")[2].split(": ")[1] == "yes" else 0.0, reviews)
		except:
			recommends = [0.0 for n in range(len(reviews))]
		weightedScore = sum(x * y for x, y in zip(scores, confidences)) / sum(confidences)
		weightedRecommend = sum(x * y for x, y in zip(recommends, confidences)) / sum(confidences)

		scoreColumn = min(int((weightedScore + 3) / 0.25), 23)
		recommendColumn = min(int(weightedRecommend / 0.1), 9)
		scoreDistributionCounts[scoreColumn] += 1
		recommendDistributionCounts[recommendColumn] += 1
		submissionIDReviewMap[submissionID] = {'score': weightedScore, 'recommend': weightedRecommend}
		scoreList.append(weightedScore)
		recommendList.append(weightedRecommend)

	# List of tuples sorted by decreasing average score- [(author, weighted score)]
	authorScores = []
	for author, v in authorScoreDict.iteritems():
		score = sum(x * y for x, y in zip(v['scores'], v['confidences'])) / max(1, sum(v['confidences']))
		authorScores.append((author, score))

	authorScores = sorted(authorScores, key=lambda x: x[0])  # Sort alphabetically first
	authorScores = sorted(authorScores, key=lambda x: x[1], reverse=True)

	# List of tuples of authors and number of recommended for best paper sorted in alphabetical and decreasing order- [(author, numRecommended)]
	recommendedAuthors = [(k, v) for (k, v) in recommendedAuthors.iteritems() if v != 0]
	recommendedAuthors = sorted(recommendedAuthors, key=lambda x: x[0])  # Sort alphabetically first
	recommendedAuthors = sorted(recommendedAuthors, key=lambda x: x[1], reverse=True)

	recommendedKeywordList, recommendedKeywordMap = getKeywords(recommendedSubmissions, s_keywordsIdx)

	# ------------- Combination insights -------------
	# TODO: only send back top 10, 20?
	parsedResult['authorScores'] = authorScores

	parsedResult['bestPaperAuthors'] = recommendedAuthors

	parsedResult['recommendedKeywordList'] = recommendedKeywordList
	parsedResult['recommendedKeywordMap'] = recommendedKeywordMap

	return {'infoType': 'submission&Review', 'infoData': parsedResult}

