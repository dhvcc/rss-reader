import pkg_resources

# For now supporting only ujson as alternatives like rapidjson, hyperjson are not consistent in benchmarks
SUPPORTED_MODULES = ["ujson"]
DOWNLOADED = [
    pkg.key for pkg in pkg_resources.working_set if pkg.key in SUPPORTED_MODULES
]
USAGE = DOWNLOADED[-1] if DOWNLOADED else "json"

json = __import__(USAGE)
