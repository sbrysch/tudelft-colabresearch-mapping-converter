# Denemark

| Final columns     | Source column(s)                  | Remarks                                      |
|-------------------|-----------------------------------|----------------------------------------------|
| name              | Name                              | years are removed from the names             |
| development_stage | year                              | deduced from source year and completion_year |
| completion_year   | Established                       | only when lower or equal to source year      |
| address           | Address, Postal number, *country* |                                              |
| dwellings_number  | Number of housing units           |                                              |
| housing_tenure    | Type of ownership                 | *see below*                                  |
| legal_form        | Type of ownership                 | *see below*                                  |

## housing_tenure

| Source: Type of ownership | housing_tenure               | Remarks |
|---------------------------|------------------------------|---------|
| Andelsboliger             | ownership_shares             |         |
| Almene boliger            | rental_public, rental_social |         |
| Ejerboliger               | ownership_full               |         |
| Lejeboliger               | rental_private_regulated     |         |
| Medejerboliger            | ownership_co                 |         |

## legal_form

| Source: Type of ownership | legal_form  | Remarks |
|---------------------------|-------------|---------|
| Andelsboliger             | cooperative |         |
