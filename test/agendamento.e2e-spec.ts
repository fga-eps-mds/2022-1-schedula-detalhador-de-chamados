import { AgendamentosService } from '../src/agendamentos/agendamentos.service';
import { CreateAgendamentodto } from '../src/agendamentos/dto/createAgendamentodto';
import { INestApplication } from '@nestjs/common';
import { Test } from '@nestjs/testing';
import * as request from 'supertest';
import { AgendamentoModule } from '../src/agendamentos/agendamento.module';

const teste: CreateAgendamentodto = {
  dataHora: new Date('2022-12-10T17:55:20.565Z'),
  alertas: [new Date('2022-12-10T17:55:20.565Z')],
  descricao: 'Teste',
  status: 'Aberto',
};

describe('Agendamentos Controller', () => {
  let app: INestApplication;
  let agendamentosService = { createAgendamento: () => teste };

  beforeAll(async () => {
    const moduleRef = await Test.createTestingModule({
      imports: [AgendamentoModule],
    })
      .overrideProvider(AgendamentosService)
      .useValue(agendamentosService)
      .compile();

    app = moduleRef.createNestApplication();
    await app.init();
  });

  it(`/POST agendamento`, () => {
    return request(app.getHttpServer())
      .post('/agendamento')
      .expect(200)
      .expect({
        data: agendamentosService.createAgendamento(),
      });
  });

  afterAll(async () => {
    await app.close();
  });
});
