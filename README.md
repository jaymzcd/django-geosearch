# Django-Geosearch

This provides a generic model you can use to hook in latitude/longitude info to
your current models. You can then make queries based on a radius and have a list
of objects returned in order of increasing distance from the center point. A
sample view called **lookup** returns a JSON array of data.

## Example

To make a request you can either use POST or GET, an example GET url is:

    http://localhost:8000/geosearch/?latitude=51.5&longitude=0&radius=500

The radius parameter is optional and is in *miles*. The current lookup view returns
JSON formatted like this:

    [
        {
            "distance": 0.0,
            "object_data": [
                null
            ],
            "object_id": 1,
            "content_type": 10
        },
        {
            "distance": 342.1842550215147,
            "object_data": [
                null
            ],
            "object_id": 2,
            "content_type": 10
        }
    ]

You can customise the fields returned by providing a *fields* parameter, comma separated:

    http://localhost:8000/geosearch/?latitude=51.5&longitude=0&radius=500&fields=pk,name

Would return:

    [
        {
            "distance": 0.0,
            "object_data": {
                "pk": 1,
                "name": "London"
            },
            "object_id": 1,
            "content_type": 10
        },
        {
            "distance": 342.1842550215147,
            "object_data": {
                "pk": 2,
                "name": "Glasgow"
            },
            "object_id": 2,
            "content_type": 10
        }
    ]

For that to work the fields must be a callable (via getattr) on the content_object
model.

