import urllib.parse


def generate_issue_link(title, body,owner='slimeless', repo='zipper', labels=None, assignee=None, milestone=None):
	base_url = f"https://github.com/{owner}/{repo}/issues/new"
	params = {
		"title": title,
		"body": body
	}
	if labels:
		params["labels"] = labels
	if assignee:
		params["assignee"] = assignee
	if milestone:
		params["milestone"] = milestone
	query_string = urllib.parse.urlencode(params, quote_via=urllib.parse.quote)
	return f"{base_url}?{query_string}"
