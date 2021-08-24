# United-Kingdom - England

| Final columns     | Source column(s)                   | Remarks                                 |
|-------------------|------------------------------------|-----------------------------------------|
| name              | Group Id, Project ID               | only an ID                              |
| development_stage | Current stage                      | Live = "functioning" (otherwise "wip")  |
| completion_year   | Target overall year for completion | only when completion_year="functioning" |
| address           | Project Postcode Area, *country*   |                                         |
| dwellings_number  | Total number of homes              |                                         |
| housing_tenure    | from columns                       |                                         |
| legal_form        | Legal form                         |                                         |

## housing_tenure

| Source: *mutliple columns*                  | housing_tenure           | Remarks |
|---------------------------------------------|--------------------------|---------|
| Affordable Rent Homes > 0                   | rental_private_regulated |         |
| Living Rent Homes > 0                       | rental_private_regulated |         |
| Social Rent Homes > 0                       | rental_social            |         |
| Market Sale Homes > 0                       | ownership_full           |         |
| Discounted Market Sale Homes (% income) > 0 | ownership_full           |         |
| Discounted Market Sale Homes (% market) > 0 | ownership_full           |         |
| Market Rent Homes > 0                       | rental_private           |         |
| Shared Ownership Homes > 0                  | ownership_co             |         |
| Shared Equity Homes > 0                     | ownership_shares         |         |
| Mutual Home Ownership Homes > 0             | ownership_shares         |         |

## legal_form

| Source: Legal form           | housing_tenure | Remarks |
|------------------------------|----------------|---------|
| Registered Society           | clt, rs        |         |
| Community Benefit Society    | clt, cbs       |         |
| Company Limited by Guarantee | clt, clg       |         |