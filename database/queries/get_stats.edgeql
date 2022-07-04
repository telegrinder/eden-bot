select (
    (select count((select User)))
    union
    (select count((select User filter .gender = 0)))
    union
    (select count((select `Like`)))
    union
    (select count((select Picture)))
)