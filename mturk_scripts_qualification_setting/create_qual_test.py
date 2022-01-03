"""Create qualifications test and HITs."""

import argparse
import boto3
import json

config_json = json.load(open("../config.json", "r"))
MTURK_SANDBOX = 'https://mturk-requester-sandbox.us-east-1.amazonaws.com'
MTURK_PROD = 'https://mturk-requester.us-east-1.amazonaws.com'
REGARD_REWARD = '0.04'
REGARD = 'regard'
SANDBOX = 'sandbox'
PROD = 'prod'
SANDBOX_REGARD_QUAL_ID = ''
PROD_REGARD_QUAL_ID = ''
SANDBOX_WORKER_URL = 'https://workersandbox.mturk.com/mturk/preview?'
PROD_WORKER_URL = 'https://worker.mturk.com/mturk/preview?'

# Variables to alter in main fn.
REWARD = '0'
QUAL_ID = -1


def make_regard_qual_test(mturk):
	# Set up qualification pre-test.
	questions = open('regard_question_template.xml', mode='r').read()
	answers = open('regard_answer_template.xml', mode='r').read()
	qual_response = mturk.create_qualification_type(
		Name='Vision test',
		Keywords='animal knowledge, cat and dog, visual perception',
		Description='This is a pre-test for identifying cats and dogs.',
		QualificationTypeStatus='Active',
		Test=questions,
		AnswerKey=answers,
		TestDurationInSeconds=1800)  # 30 minutes.
	qual_id = qual_response['QualificationType']['QualificationTypeId']
	print('REGARD PRETEST qual ID:', qual_id)
	return qual_id


def main():
	global QUAL_ID, REWARD
	AWS_ACCESS_KEY_ID = config_json['AWS_ACCESS_ID']
	AWS_SECRET_ACCESS_KEY = config_json['AWS_ACCESS_SECRET']

	parser = argparse.ArgumentParser()
	parser.add_argument(
		'--test_type',
		default='regard',
		type=str,
		required=False,
		help='`regard`.'
	)
	parser.add_argument(
		'--version',
		default='sandbox',
		type=str,
		required=False,
		help='Either `sandbox` or `prod`.'
	)
	parser.add_argument(
		'--make_pretest',
		required=False,
		action='store_true',
		help='Whether to make a pretest.'
	)

	args = parser.parse_args()
	print('args', args)

	# Set global variables.
	if args.test_type == REGARD:
		REWARD = REGARD_REWARD
		if args.version == PROD:
			QUAL_ID = PROD_REGARD_QUAL_ID
		elif args.version == SANDBOX:
			QUAL_ID = SANDBOX_REGARD_QUAL_ID
	if args.version == PROD:
		endpoint_url = MTURK_PROD
	elif args.version == SANDBOX:
		endpoint_url = MTURK_SANDBOX

	# Set up mturk client.

	mturk = boto3.client('mturk',
	                     region_name='us-east-1',
	                     endpoint_url=endpoint_url,
	                     aws_access_key_id=AWS_ACCESS_KEY_ID,
						 aws_secret_access_key=AWS_SECRET_ACCESS_KEY
	)
	print("I have $" + mturk.get_account_balance()['AvailableBalance'] + " in my account")

	# Make pretest.
	if args.test_type == REGARD:
		if args.make_pretest:
			QUAL_ID = make_regard_qual_test(mturk)
		else:
			if args.version == SANDBOX:
				QUAL_ID = SANDBOX_REGARD_QUAL_ID
			elif args.version == PROD:
				QUAL_ID = PROD_REGARD_QUAL_ID


if __name__ == '__main__':
	main()
