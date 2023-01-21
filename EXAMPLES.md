```sh
curl -s -XPUT -H 'Content-Type: application/json'  -H 'accept: application/json' -d '{
    "first_name": "Simon",
    "last_name": "Jaff",
    "is_active": false,
    "marketing_opt_in": true,
    "owner_id": 1,
    "company_id": 2
}' http://john@localhost:8000/contacts/2 | jq .
```
