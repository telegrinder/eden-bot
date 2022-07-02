update User {city, city_written_name, safe_mode}
filter .telegram_id = <str>$telegram_id
set {safe_mode := not .safe_mode}