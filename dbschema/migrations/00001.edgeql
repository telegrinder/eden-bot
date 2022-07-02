CREATE MIGRATION m1k2colk4qvnu6kxzxmzyuctkup2p4zdshbq4rkgnej5jcdrcbfa6a
    ONTO initial
{
  CREATE TYPE default::Advert {
      CREATE REQUIRED PROPERTY ad_text -> std::str;
      CREATE REQUIRED PROPERTY promoted_link -> std::str;
  };
  CREATE TYPE default::City {
      CREATE REQUIRED PROPERTY names -> array<std::str>;
  };
  CREATE TYPE default::Picture {
      CREATE REQUIRED PROPERTY by_tg_id -> std::str;
      CREATE REQUIRED PROPERTY file_id -> std::str;
      CREATE PROPERTY moderated -> std::bool;
  };
  CREATE TYPE default::User {
      CREATE LINK city -> default::City {
          CREATE PROPERTY written_name -> std::str;
      };
      CREATE REQUIRED PROPERTY telegram_id -> std::str {
          CREATE CONSTRAINT std::exclusive;
      };
      CREATE MULTI LINK pictures := (SELECT
          default::Picture
      FILTER
          (.by_tg_id = default::User.telegram_id)
      );
      CREATE REQUIRED PROPERTY age -> std::int16 {
          CREATE CONSTRAINT std::max_value(100);
          CREATE CONSTRAINT std::min_value(15);
      };
      CREATE REQUIRED PROPERTY checked -> array<std::str> {
          SET default := (<array<std::str>>[]);
      };
      CREATE REQUIRED PROPERTY created_at -> cal::local_datetime;
      CREATE PROPERTY description -> std::str;
      CREATE REQUIRED PROPERTY display -> std::bool {
          SET default := true;
      };
      CREATE REQUIRED PROPERTY gender -> std::int16;
      CREATE REQUIRED PROPERTY interest -> std::str {
          SET default := 'f';
      };
      CREATE REQUIRED PROPERTY last_active -> cal::local_datetime;
      CREATE REQUIRED PROPERTY name -> std::str;
      CREATE REQUIRED PROPERTY reported -> std::int16 {
          SET default := 0;
      };
      CREATE REQUIRED PROPERTY safe_mode -> std::bool {
          SET default := false;
      };
      CREATE REQUIRED PROPERTY search_city -> std::bool {
          SET default := false;
      };
      CREATE REQUIRED PROPERTY uid -> std::uuid {
          SET default := (SELECT
              std::uuid_generate_v1mc()
          );
          SET readonly := true;
          CREATE CONSTRAINT std::exclusive;
      };
  };
  CREATE TYPE default::`Like` {
      CREATE REQUIRED LINK from_user -> default::User;
      CREATE REQUIRED LINK to_user -> default::User;
      CREATE REQUIRED PROPERTY seen -> std::bool {
          SET default := false;
      };
  };
};
