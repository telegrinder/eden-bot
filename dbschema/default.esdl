module default {
    type User {
        required property uid -> uuid {
            default := (select std::uuid_generate_v1mc());
            readonly := true;
            constraint exclusive;
        }
        required property telegram_id -> str {
            constraint exclusive;
        }
        multi link pictures := (
            select Picture filter .by_tg_id = User.telegram_id
        );
        required property name -> str;
        required property age -> int16 {
            constraint min_value(15);
            constraint max_value(100);
        }
        property description -> str;
        required property created_at -> cal::local_datetime;
        required property last_active -> cal::local_datetime;
        required property display -> bool {
            default := true;
        }
        required property interest -> str {
            default := "f";
        }
        required property gender -> int16;
        required property checked -> array<str> {
            default := <array<str>>[];
        }
        required property safe_mode -> bool {
            default := false;
        }
        required property city -> int16 {
            default := 0;
        }
        required property city_written_name -> str {
            default := "";
        }
        required property search_city -> bool {
            default := false;
        }
        required property reported -> int16 {
            default := 0;
        }
    }
    type Picture {
        required property by_tg_id -> str;
        required property file_id -> str;
        property moderated -> bool;
    }
    type `Like` {
        required link from_user -> User;
        required link to_user -> User;
        required property seen -> bool {
            default := false;
        }
    }
    type Admin {
        required property telegram_id -> str {
            constraint exclusive;
        }
        required property promoted_by -> str;
        required property promoted_at -> cal::local_datetime;
    }
}