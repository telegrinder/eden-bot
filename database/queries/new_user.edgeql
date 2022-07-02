insert User {
    telegram_id := <str>$telegram_id, 
    name := <str>$name, 
    age := <int16>$age, 
    created_at := <cal::local_datetime>$time_now, 
    last_active := <cal::local_datetime>$time_now, 
    gender := <int16>$gender, 
    interest := <str>$interest, 
    description := <str>$description
}