# Flask Code Challenge - Sweets Vendors

For this assessment, you'll be working with a vendors and sweets domain.

In this repo:

- There is a Flask application with some features built out.
- There is a fully built React frontend application.
- There are tests included which you can run using `pytest -x`.
- There is a file `challenge-3-sweets.postman_collection.json` that contains a
  Postman collection of requests for testing each route you will implement.

Depending on your preference, you can either check your API by:

- Using Postman to make requests
- Running `pytest -x` and seeing if your code passes the tests
- Running the React application in the browser and interacting with the API via
  the frontend

You can import `challenge-3-sweets.postman_collection.json` into Postman by
pressing the `Import` button.

![import postman](https://curriculum-content.s3.amazonaws.com/6130/phase-4-code-challenge-instructions/import_collection.png)

Select `Upload Files`, navigate to this repo folder, and select
`challenge-3-sweets.postman_collection.json` as the file to import.

## Setup

The instructions assume you changed into the `code-challenge` folder **prior**
to opening the code editor.

To download the dependencies for the frontend and backend, run:

```console
pipenv install
pipenv shell
npm install --prefix client
```

You can run your Flask API on [`localhost:5555`](http://localhost:5555) by
running:

```console
python server/app.py
```

You can run your React app on [`localhost:4000`](http://localhost:4000) by
running:

```sh
npm start --prefix client
```

You are not being assessed on React, and you don't have to update any of the
React code; the frontend code is available just so that you can test out the
behavior of your API in a realistic setting.

Your job is to build out the Flask API to add the functionality described in the
deliverables below.

## Models

You will implement an API for the following data model:

![domain diagram](https://curriculum-content.s3.amazonaws.com/6130/challenge-3-sweets/domain.png)

The file `server/models.py` defines the model classes **without relationships**.
Use the following commands to create the initial database `app.db`:

```console
export FLASK_APP=server/app.py
flask db init
flask db upgrade head
```

Now you can implement the relationships as shown in the ER Diagram:

- A `Sweet` has many `Vendor`s through `VendorSweet`
- A `Vendor` has many `Sweet`s through `VendorSweet`
- A `VendorSweet` belongs to a `Sweet` and belongs to a `Vendor`

Update `server/models.py` to establish the model relationships. Since a
`VendorSweet` belongs to a `Vendor` and a `Sweet`, configure the model to
cascade deletes.

Set serialization rules to limit the recursion depth.

Run the migrations and seed the database:

```console
flask db revision --autogenerate -m 'message'
flask db upgrade head
python server/seed.py
```

> If you aren't able to get the provided seed file working, you are welcome to
> generate your own seed data to test the application.

## Validations

Add validations to the `VendorSweet` model:

- `price` must have a value (i.e. can't be None)
- `price` cannot be a negative number

## Routes

Set up the following routes. Make sure to return JSON data in the format
specified along with the appropriate HTTP verb.

### GET /vendors

Return JSON data in the format below:

```json
[
  { "id": 1, "name": "Insomnia Cookies" },
  { "id": 2, "name": "Cookies Cream" }
]
```

### GET /vendors/:id

If the `Vendor` exists, return JSON data in the format below:

```json
{
  "id": 1,
  "name": "Insomnia Cookies",
  "vendor_sweets": [
    {
      "id": 2,
      "price": 45,
      "sweet": {
        "id": 2,
        "name": "Chocolate Chunk Cookie"
      },
      "sweet_id": 2,
      "vendor_id": 1
    }
  ]
}
```

If the `Vendor` does not exist, return the following JSON data, along with the
appropriate HTTP status code:

```json
{
  "error": "Vendor not found"
}
```

### GET /sweets

Return JSON data in the format below:

```json
[
  {
    "id": 1,
    "name": "Chocolate Chip Cookie"
  },
  {
    "id": 2,
    "name": "Brownie"
  }
]
```

### GET /sweets/<int:id>

If the `Sweet` exists, return JSON data in the format below:

```json
{
  "id": 1,
  "name": "Chocolate Chip Cookie"
}
```

If the `Sweet` does not exist, return the following JSON data, along with the
appropriate HTTP status code:

```json
{
  "error": "Sweet not found"
}
```

### POST /vendor_sweets

This route should create a new `VendorSweet` that is associated with an existing
`Vendor` and `Sweet`. It should accept an object with the following properties
in the body of the request:

```json
{
  "price": 300,
  "vendor_id": 1,
  "sweet_id": 3
}
```

If the `VendorSweet` is created successfully, send back a response with the
following data:

```json
{
  "id": 7,
  "price": 300,
  "sweet": {
    "id": 3,
    "name": "M&Ms Cookie"
  },
  "sweet_id": 3,
  "vendor": {
    "id": 1,
    "name": "Insomnia Cookies"
  },
  "vendor_id": 1
}
```

If the `VendorSweet` is **not** created successfully, return the following JSON
data, along with the appropriate HTTP status code:

```json
{ "errors": ["validation errors"] }
```

### DELETE /vendor_sweets/<int:id>

This route should delete an existing `VendorSweet`. If the `VendorSweet` exists
and is deleted successfully, return an empty object as a response:

```json
{}
```

If the `VendorSweet` does not exist, return the following JSON data, along with
the appropriate HTTP status code:

```json
{
  "error": "VendorSweet not found"
}
```
