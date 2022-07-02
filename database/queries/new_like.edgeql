insert `Like` {
    from_user := (select User filter .telegram_id = <str>$from_user_id),
    to_user := (select User filter .telegram_id = <str>$to_user_id)
}