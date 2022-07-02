CREATE MIGRATION m1rhwvyfzklroqxrpufnl2gfvsdby7xhfg3bbhly4hze7vkygptyiq
    ONTO m1gmeojbuhcbtraph2lhryhrtxud35gehipqj7l5doklns57delyqa
{
  CREATE TYPE default::Admin {
      CREATE REQUIRED PROPERTY promoted_at -> cal::local_datetime;
      CREATE REQUIRED PROPERTY promoted_by -> std::str;
      CREATE REQUIRED PROPERTY telegram_id -> std::str {
          CREATE CONSTRAINT std::exclusive;
      };
  };
};
