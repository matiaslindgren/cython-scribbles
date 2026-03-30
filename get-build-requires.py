from tomllib import load

assert __name__ == "__main__", "wtf u doin"

with open("pyproject.toml", "rb") as f:
    pyproject = load(f)

build_requires = pyproject["build-system"]["requires"]
assert build_requires

print(" ".join(map(repr, build_requires)))
