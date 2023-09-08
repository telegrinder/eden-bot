CREATE MIGRATION m1vr3wtls2qh7tyqqvahak6li6q6l2x6rtqhhrnbcn3zrlggckil6a
    ONTO m13w2k2mkxxm2peswdnh2ljklq2r7ruy6xo4tkdroj7eraa3r4sqfa
{
  CREATE TYPE default::Uni {
      CREATE REQUIRED PROPERTY city -> std::int16;
      CREATE REQUIRED PROPERTY name -> std::str;
  };
  ALTER TYPE default::User {
      CREATE LINK university -> default::Uni;
  };
};
