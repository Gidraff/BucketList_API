"""Module that contains custom errors."""
from flask import jsonify


def bad_request(e):
    """Check for error 400 and returns a custom error."""
    return jsonify({
        "error": "{} Bad request. Check your inputs and try again".format(
            e.code)}), 400


def page_not_found(e):
    """Check for a 404 error and returns a custom error."""
    return jsonify({
        "error": "{} page request not found.Check url".format(e.code)}), 404


def internal_server_error(e):
    """Check for a 500 error and returns a custom error."""
    return jsonify({
        "error": "{} Oops! Internal server error.".format(500)}), 500
