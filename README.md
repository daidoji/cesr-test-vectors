# cesr-test-vectors
CESR Test Vectors

**Note: Neither the sizeify property based testing nor (for a lot of reasons)
are the sizeified keripy vectors.  They are not idempotent between testing
runs.  We tried to use libraries like freezegun and time_machine with our
monkeypatching code but due to a variety of choices in the keripy test
implementations these dates aren't always adhered to. **

We mangled the date to one specific date but the "n" fields in the KERI events
use next key digests that aren't idempotent either so we'd have to monkeypatch
that too.

SIZEIFY
	KERIPY
		VERSION1
			MGPK
			CBOR
			JSON
		VERSION2
			MGPK
			CBOR
			JSON
	PROPERTY_BASED_TESTING
		VERSION1
			MGPK
			CBOR
			JSON
		VERSION2
			MGPK
			CBOR
			JSON
PRIMITIVES
INDEXES
COUNT\_CODES
	VERSION1
	VERSION2
STREAMS (TBD)
	VERSION1
	VESRION2

Utils
	commands that generate the above
	commands that take above and put it into a DB for transporting/archiving
