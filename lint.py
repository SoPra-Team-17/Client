# siehe https://medium.com/analytics-vidhya/pylint-static-code-analysis-github-action-to-fail-below-a-score-threshold-58a124aafaa0
import logging
from pylint.lint import Run
import sys

logging.getLogger().setLevel(logging.INFO)

path = ["view", "model", "controller", "test"]
threshold = 5

results = Run(path, do_exit=False)

final_score = results.linter.stats['global_note']

if final_score < threshold:
    message = ('PyLint Failed | '
               'Score: {} | '
               'Threshold: {} '.format(final_score, threshold))
    logging.error(message)
    raise Exception(message)

else:
    message = ('PyLint Passed | '
               'Score: {} | '
               'Threshold: {} '.format(final_score, threshold))
    logging.info(message)
    sys.exit(0)