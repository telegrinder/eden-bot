with
    file_ids := <array<str>>$ids,
for file_id_ in array_unpack(file_ids) union (
    insert Picture {
        by_tg_id := <str>$telegram_id,
        file_id := <str>file_id_,
        moderated := <bool>false
    }
)