update User 
filter .telegram_id = <str>$telegram_id
set {checked := .checked ++ [<str>$seen_id]}