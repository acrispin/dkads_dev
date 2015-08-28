BEGIN;

ALTER TABLE "public"."art" ADD CONSTRAINT "uk_artl_code" UNIQUE ("code");
ALTER TABLE "public"."sy_user" ADD CONSTRAINT "uk_user_email" UNIQUE ("email");
ALTER TABLE "public"."sy_user" ADD CONSTRAINT "uk_user_username" UNIQUE ("username");

ALTER TABLE "public"."whs_art" ADD CONSTRAINT "whs_art_whs_fk" FOREIGN KEY ("whs_id") REFERENCES "public"."whs" ( "_id");
ALTER TABLE "public"."whs_art" ADD CONSTRAINT "whs_art_art_fk" FOREIGN KEY ("art_id") REFERENCES "public"."art" ( "_id");
ALTER TABLE "public"."whs_tran" ADD CONSTRAINT "whs_tran_whs_fk" FOREIGN KEY ("whs_id") REFERENCES "public"."whs" ( "_id");
ALTER TABLE "public"."whs_tran" ADD CONSTRAINT "whs_tran_art_fk" FOREIGN KEY ("art_id") REFERENCES "public"."art" ( "_id");
ALTER TABLE "public"."whs_tran" ADD CONSTRAINT "whs_tran_rsn_fk" FOREIGN KEY ("rsn_id") REFERENCES "public"."rsn" ( "_id");
ALTER TABLE "public"."sy_user_role" ADD CONSTRAINT "sy_user_role_role_fk" FOREIGN KEY ("sy_role_id") REFERENCES "public"."sy_role" ( "_id");
ALTER TABLE "public"."sy_user_role" ADD CONSTRAINT "sy_user_role_user_fk" FOREIGN KEY ("sy_user_id") REFERENCES "public"."sy_user" ( "_id");

ALTER TABLE "public"."sy_user" ALTER COLUMN "active" SET DEFAULT TRUE;
ALTER TABLE "public"."sy_user" ALTER COLUMN "reg_date" SET DEFAULT CURRENT_TIMESTAMP;
ALTER TABLE "public"."sy_user" ALTER COLUMN "reg_user" SET DEFAULT CURRENT_USER;
ALTER TABLE "public"."sy_role" ALTER COLUMN "active" SET DEFAULT TRUE;
ALTER TABLE "public"."sy_role" ALTER COLUMN "reg_date" SET DEFAULT CURRENT_TIMESTAMP;
ALTER TABLE "public"."sy_role" ALTER COLUMN "reg_user" SET DEFAULT CURRENT_USER;
ALTER TABLE "public"."art" ALTER COLUMN "active" SET DEFAULT TRUE;
ALTER TABLE "public"."art" ALTER COLUMN "reg_date" SET DEFAULT CURRENT_TIMESTAMP;
ALTER TABLE "public"."art" ALTER COLUMN "reg_user" SET DEFAULT CURRENT_USER;
ALTER TABLE "public"."rsn" ALTER COLUMN "active" SET DEFAULT TRUE;
ALTER TABLE "public"."rsn" ALTER COLUMN "reg_date" SET DEFAULT CURRENT_TIMESTAMP;
ALTER TABLE "public"."rsn" ALTER COLUMN "reg_user" SET DEFAULT CURRENT_USER;
ALTER TABLE "public"."whs" ALTER COLUMN "active" SET DEFAULT TRUE;
ALTER TABLE "public"."whs" ALTER COLUMN "reg_date" SET DEFAULT CURRENT_TIMESTAMP;
ALTER TABLE "public"."whs" ALTER COLUMN "reg_user" SET DEFAULT CURRENT_USER;
ALTER TABLE "public"."whs_tran" ALTER COLUMN "active" SET DEFAULT TRUE;
ALTER TABLE "public"."whs_tran" ALTER COLUMN "reg_date" SET DEFAULT CURRENT_TIMESTAMP;
ALTER TABLE "public"."whs_tran" ALTER COLUMN "reg_user" SET DEFAULT CURRENT_USER;

COMMIT;
