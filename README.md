Dictionary app. An API, which uses wamerican, more specifically american-english-huge (link to download below) to service POST endpoints.
These endpoints send back information about request text, like what words are not defined in the wamerican, their count and pairs of defined and undefined words.

Not deployed, runs on waitress. Local host set to port 50100

Endpoints:

/filter_words - Response: Undefined words in request body
/filter_pairs - Response: Pairs of undefined a defined words from request body
/filter_count - Response: Count of undefined and defined words in request body

The app treats request body like raw text.

Link to the used version of wamerican: https://ftp.zcu.cz/mirrors/debian/pool/main/s/scowl/wamerican-huge_2020.12.07-2_all.deb

Disclaimer: For the app to work properly refactor_wamerican.py needs to be run because wamerican-huge is not sorted.
