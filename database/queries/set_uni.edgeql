update User
filter .telegram_id = <str>$telegram_id
set {
    university := (select Uni filter .id = <uuid>$uni_id limit 1)
}