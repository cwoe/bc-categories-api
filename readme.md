# Local Categories API for BlueCoat/Symantec Proxies

## Description

Allows the editing of a local categories database via API calls.

This can be used to automatically resolve white-/blacklisting related tickets, if properly integrated with a ticket system.

## Allowed Methods

Path | Method | Auth | Parameters
--- | --- | --- | ---
/categories.txt | GET | None | 
/add | POST | Basic | category, domain
/remove | DELETE | Basic | category. domainw
