CREATE TABLE "users"(
    "id" INTEGER NOT NULL,
    "name" VARCHAR(255) NOT NULL,
    "email" VARCHAR(255) NOT NULL,
    "picture" VARCHAR(255) NOT NULL,
    "password" VARCHAR(255) NOT NULL,
    "created_at" TIMESTAMP(0) WITHOUT TIME ZONE NOT NULL,
    "updated_at" TIMESTAMP(0) WITHOUT TIME ZONE NOT NULL
);
ALTER TABLE
    "users" ADD PRIMARY KEY("id");
CREATE TABLE "medicines"(
    "id" BIGINT NOT NULL,
    "name" VARCHAR(255) NOT NULL,
    "type" VARCHAR(255) NOT NULL,
    "strength" VARCHAR(255) NOT NULL,
    "brand" VARCHAR(255) NOT NULL,
    "instructions" TEXT NOT NULL
);
ALTER TABLE
    "medicines" ADD PRIMARY KEY("id");
CREATE TABLE "appointments"(
    "id" BIGINT NOT NULL,
    "user_id" BIGINT NOT NULL,
    "date" DATE NOT NULL,
    "time" TIME(0) WITHOUT TIME ZONE NOT NULL,
    "problem" VARCHAR(255) NOT NULL,
    "status" VARCHAR(255) NOT NULL,
    "created_at" TIMESTAMP(0) WITHOUT TIME ZONE NOT NULL,
    "updated_at" TIMESTAMP(0) WITHOUT TIME ZONE NOT NULL
);
ALTER TABLE
    "appointments" ADD PRIMARY KEY("id");
CREATE TABLE "prescriptions"(
    "id" BIGINT NOT NULL,
    "user_id" BIGINT NOT NULL,
    "appointment_id" BIGINT NOT NULL,
    "note" TEXT NOT NULL,
    "created_at" TIMESTAMP(0) WITHOUT TIME ZONE NOT NULL,
    "updated_at" TIMESTAMP(0) WITHOUT TIME ZONE NOT NULL
);
ALTER TABLE
    "prescriptions" ADD PRIMARY KEY("id");
CREATE TABLE "PrescriptionItems"(
    "id" BIGINT NOT NULL,
    "medicine_id" BIGINT NOT NULL,
    "prescription_id" BIGINT NOT NULL,
    "dosage" VARCHAR(255) NOT NULL,
    "duration" VARCHAR(255) NOT NULL,
    "instructions" VARCHAR(255) NOT NULL,
    "created_at" TIMESTAMP(0) WITHOUT TIME ZONE NOT NULL,
    "updated_at" TIMESTAMP(0) WITHOUT TIME ZONE NOT NULL
);
ALTER TABLE
    "PrescriptionItems" ADD PRIMARY KEY("id");
CREATE TABLE "documents"(
    "id" BIGINT NOT NULL,
    "user_id" BIGINT NOT NULL,
    "title" VARCHAR(255) NOT NULL,
    "file" VARCHAR(255) NOT NULL,
    "created_at" TIMESTAMP(0) WITHOUT TIME ZONE NOT NULL,
    "updated_at" TIMESTAMP(0) WITHOUT TIME ZONE NOT NULL
);
ALTER TABLE
    "documents" ADD PRIMARY KEY("id");
CREATE TABLE "payments"(
    "id" BIGINT NOT NULL,
    "user_id" BIGINT NOT NULL,
    "method" VARCHAR(255) NOT NULL,
    "amount" DECIMAL(8, 2) NOT NULL,
    "type" VARCHAR(255) NOT NULL DEFAULT 'paid',
    "transactionID" VARCHAR(255) NOT NULL,
    "status" VARCHAR(255) NOT NULL DEFAULT 'successful',
    "created_at" TIMESTAMP(0) WITHOUT TIME ZONE NOT NULL,
    "updated_at" TIMESTAMP(0) WITHOUT TIME ZONE NOT NULL
);
ALTER TABLE
    "payments" ADD PRIMARY KEY("id");
CREATE TABLE "patient"(
    "id" BIGINT NOT NULL,
    "user_id" BIGINT NOT NULL,
    "phone" VARCHAR(255) NOT NULL,
    "date_of_birth" DATE NOT NULL,
    "gender" VARCHAR(255) NOT NULL DEFAULT 'male',
    "blood_group" VARCHAR(255) NOT NULL,
    "address" TEXT NOT NULL
);
ALTER TABLE
    "patient" ADD PRIMARY KEY("id");
ALTER TABLE
    "PrescriptionItems" ADD CONSTRAINT "prescriptionitems_medicine_id_foreign" FOREIGN KEY("medicine_id") REFERENCES "medicines"("id");
ALTER TABLE
    "payments" ADD CONSTRAINT "payments_user_id_foreign" FOREIGN KEY("user_id") REFERENCES "users"("id");
ALTER TABLE
    "appointments" ADD CONSTRAINT "appointments_user_id_foreign" FOREIGN KEY("user_id") REFERENCES "users"("id");
ALTER TABLE
    "prescriptions" ADD CONSTRAINT "prescriptions_appointment_id_foreign" FOREIGN KEY("appointment_id") REFERENCES "appointments"("id");
ALTER TABLE
    "patient" ADD CONSTRAINT "patient_user_id_foreign" FOREIGN KEY("user_id") REFERENCES "users"("id");
ALTER TABLE
    "documents" ADD CONSTRAINT "documents_user_id_foreign" FOREIGN KEY("user_id") REFERENCES "users"("id");
ALTER TABLE
    "prescriptions" ADD CONSTRAINT "prescriptions_user_id_foreign" FOREIGN KEY("user_id") REFERENCES "users"("id");
ALTER TABLE
    "PrescriptionItems" ADD CONSTRAINT "prescriptionitems_prescription_id_foreign" FOREIGN KEY("prescription_id") REFERENCES "prescriptions"("id");