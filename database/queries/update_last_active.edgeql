update User
filter .telegram_id = <str>$telegram_id
set {
    last_active := <cal::local_datetime>$time_now
}