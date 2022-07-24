CREATE DATABASE detalhador_de_chamados;

\c detalhador_de_chamados

CREATE SCHEMA IF NOT EXISTS "public";

CREATE TABLE "public"."category" (
    id INTEGER NOT NULL GENERATED ALWAYS AS IDENTITY(start 1),
    name VARCHAR(250) NOT NULL,
    description TEXT,
    active BOOLEAN NOT NULL DEFAULT TRUE,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT "PK_id_category" PRIMARY KEY ("id")
);

CREATE TABLE "public"."problem" (
    id INTEGER NOT NULL GENERATED ALWAYS AS IDENTITY(start 1),
    name VARCHAR(250),
    description TEXT,
    active BOOLEAN,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    category_id INTEGER,

    CONSTRAINT "PK_id_problem" PRIMARY KEY ("id"),
    CONSTRAINT "FK_category_id" FOREIGN KEY ("category_id")
        REFERENCES "public"."category" ("id")
        ON DELETE RESTRICT

);