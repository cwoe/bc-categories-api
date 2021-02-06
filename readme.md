# Local Categories API for BlueCoat/Symantec Proxies

## Description

Allows the editing of a local categories database via API calls.

This can be used to automatically resolve white-/blacklisting related tickets, if properly integrated with a ticket system.

## Allowed Methods

Path | Method | Auth | Parameters
--- | --- | --- | ---
/categories.txt | GET | None |
/add | POST | Basic | category, domain
/remove | DELETE | Basic | category, domain

## Examples

### Get current Categories Database
curl http://localhost:5000/categories.txt

### Add a domain
curl -X POST http://localhost:5000/add -F 'domain=cwoellner.com' -F 'category=HTTP_whitelist' --user admin:admin

### Remove a domain
curl -X DELETE http://localhost:5000/remove -F 'domain=cwoellner.com' -F 'category=HTTP_whitelist' --user admin:admin
