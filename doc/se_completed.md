# Sweden - completed

| Final columns     | Source column(s)                      | Remarks       |
|-------------------|---------------------------------------|---------------|
| name              | Name of cohouse                       |               |
| development_stage |                                       | "functioning" |
| completion_year   | started living                        |               |
| address           | Address, City/municipality, *country* |               |
| dwellings_number  | Number of flats                       |               |
| housing_tenure    | Tenure today, Type of house owner     | *see below*   |
| legal_form        | Tenure today, Type of house owner     | *see below*   |

## housing_tenure

| Source: Tenure Today | Logic. op. | Source: Type of house owner               | housing_tenure           | Remarks |
|----------------------|:----------:|-------------------------------------------|--------------------------|---------|
| tenancy              |    AND     | municipality owned public housing company | rental_public            |         |
| tenancy              |    AND     | private housing company                   | rental_private_regulated |         |
| tenancy              |    AND     | foundation or trust                       | rental_private_regulated |         |
| tenancy              |    AND     | private person                            | rental_private_regulated |         |
| cooperative tenancy  |            |                                           | rental_cooperative       |         |
| condominium          |            |                                           | ownership_co             |         |

## legal_form

| Source: Tenure today | Source: Type of house owner | legal_form  | Remarks |
|----------------------|-----------------------------|-------------|---------|
| cooperative tenancy  |                             | cooperative |         |
|                      | foundation or trust         | foundation  |         |
