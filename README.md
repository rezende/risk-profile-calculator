## Set up

`pipenv shell`
`pipenv install --dev`

## Running the server

`gunicorn risk_api:app`

## Calling the endpoint

Using HTTPie:

`http POST localhost:8000/calculator age:=90 dependents:=2 risk_questions:='[1,1,1]' income:=150000 marital_status=single vehicle:='{"year": 2010}' house:='{"ownership_status": "mortgaged"}'`

## Running Tests

`pytest`
