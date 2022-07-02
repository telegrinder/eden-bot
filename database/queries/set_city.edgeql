update User {city, search_city, safe_mode}
filter .telegram_id = <str>$telegram_id
set {
    city := <int16>$city_id,
    city_written_name := <str>$written_name
}