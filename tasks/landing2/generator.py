from kyzylborda_lib.secrets import get_secret


def generate():
	return {
		"flags": [get_secret("editor_password")]
	}
