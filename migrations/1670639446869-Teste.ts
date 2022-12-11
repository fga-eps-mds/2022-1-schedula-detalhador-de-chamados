import { MigrationInterface, QueryRunner } from "typeorm";

export class Teste1670639446869 implements MigrationInterface {
    name = 'Teste1670639446869'

    public async up(queryRunner: QueryRunner): Promise<void> {
        await queryRunner.query(`CREATE TABLE "alerta" ("id" uuid NOT NULL DEFAULT uuid_generate_v4(), "date" TIMESTAMP NOT NULL, "agendamentoId" uuid, CONSTRAINT "PK_e60bfc27e2ae1b6bbdca11ac524" PRIMARY KEY ("id"))`);
        await queryRunner.query(`CREATE TABLE "agendamento" ("id" uuid NOT NULL DEFAULT uuid_generate_v4(), "dataHora" TIMESTAMP, "descricao" character varying, "status" character varying NOT NULL, CONSTRAINT "PK_a102b15cfec9ce6d8ac6193345f" PRIMARY KEY ("id"))`);
        await queryRunner.query(`ALTER TABLE "alerta" ADD CONSTRAINT "FK_035fa764d019caba64cfd1f8e55" FOREIGN KEY ("agendamentoId") REFERENCES "agendamento"("id") ON DELETE NO ACTION ON UPDATE NO ACTION`);
    }

    public async down(queryRunner: QueryRunner): Promise<void> {
        await queryRunner.query(`ALTER TABLE "alerta" DROP CONSTRAINT "FK_035fa764d019caba64cfd1f8e55"`);
        await queryRunner.query(`DROP TABLE "agendamento"`);
        await queryRunner.query(`DROP TABLE "alerta"`);
    }

}
