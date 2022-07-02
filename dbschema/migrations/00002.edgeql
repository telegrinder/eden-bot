CREATE MIGRATION m1gmeojbuhcbtraph2lhryhrtxud35gehipqj7l5doklns57delyqa
    ONTO m1k2colk4qvnu6kxzxmzyuctkup2p4zdshbq4rkgnej5jcdrcbfa6a
{
  ALTER TYPE default::City {
      DROP PROPERTY names;
  };
  ALTER TYPE default::User {
      DROP LINK city;
  };
  DROP TYPE default::City;
  ALTER TYPE default::User {
      CREATE REQUIRED PROPERTY city -> std::int16 {
          SET default := 0;
      };
  };
  ALTER TYPE default::User {
      CREATE REQUIRED PROPERTY city_written_name -> std::str {
          SET default := '';
      };
  };
};
