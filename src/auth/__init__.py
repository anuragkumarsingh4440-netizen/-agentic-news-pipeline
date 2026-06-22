"""Identity / authorization boundary.

Face auth is a SECURITY gate, not a feature: sensitive tools must not run
unless the operator is verified. Behind an interface so 'verified' can be a
real face match in production and a stub in tests.
"""
