update User {search_city, city, safe_mode}
filter .telegram_id = <str>$telegram_id
set {
    search_city := not .search_city
}