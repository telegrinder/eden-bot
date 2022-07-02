select `Like` {from_user: {telegram_id, name, age, description, pictures: {file_id}}}
filter .to_user.telegram_id = <str>$telegram_id
and .seen = false