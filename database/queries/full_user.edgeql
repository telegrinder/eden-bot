select User {
    uid, 
    telegram_id,
    gender, 
    interest, 
    created_at, 
    last_active,
    description,
    age, 
    name, 
    display, 
    city,
    city_written_name,
    pictures: {file_id},
    safe_mode, 
    search_city
} filter .telegram_id = <str>$telegram_id