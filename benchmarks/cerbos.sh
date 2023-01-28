#!/bin/bash

cat <<EOF | curl -i --silent "localhost:3592/api/check?pretty" -d @-
{
    "requestId": "test01",
    "actions": ["read"],
    "resource": {
        "kind": "contact",
        "instances": { 
            "1": { 
                "attr":  { 
                    "id":  "1",
                    "is_active": true
                }
            }
        }
    },
    "principal": {
        "id": "john",
        "roles": ["user"],
        "attr": { 
            "department": "Sales"
        }
    }
}
EOF
