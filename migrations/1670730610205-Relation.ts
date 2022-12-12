import { MigrationInterface, QueryRunner } from "typeorm";

export class Relation1670730610205 implements MigrationInterface {
    name = 'Relation1670730610205'

    public async up(queryRunner: QueryRunner): Promise<void> {
        await queryRunner.query(`ALTER TABLE "alerta" DROP CONSTRAINT "FK_035fa764d019caba64cfd1f8e55"`);
        await queryRunner.query(`ALTER TABLE "alerta" ADD CONSTRAINT "FK_035fa764d019caba64cfd1f8e55" FOREIGN KEY ("agendamentoId") REFERENCES "agendamento"("id") ON DELETE CASCADE ON UPDATE NO ACTION`);
    }

    public async down(queryRunner: QueryRunner): Promise<void> {
        await queryRunner.query(`ALTER TABLE "alerta" DROP CONSTRAINT "FK_035fa764d019caba64cfd1f8e55"`);
        await queryRunner.query(`ALTER TABLE "alerta" ADD CONSTRAINT "FK_035fa764d019caba64cfd1f8e55" FOREIGN KEY ("agendamentoId") REFERENCES "agendamento"("id") ON DELETE NO ACTION ON UPDATE NO ACTION`);
    }

}
