select User {last_active, telegram_id} filter
exists (select `Like` {to_user, seen} filter .seen = false and .to_user = User)
and User.last_active > <cal::local_datetime>$min_online