import {
  Injectable,
  InternalServerErrorException,
  NotFoundException,
} from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository, DataSource } from 'typeorm';
import { Chamado } from './chamado.entity';
import { CreateChamadodto } from './dto/createChamadodto';

@Injectable()
export class ChamadosService {
  constructor(
    @InjectRepository(Chamado)
    private ChamadoRepo: Repository<Chamado>,
  ) {}

  async createChamado(
    createChamadodto: CreateChamadodto,
  ): Promise<Chamado> {
    const {solicitante,telefone,cidade,posto_trabalho,categoria_problema,tipo_problema,email} = createChamadodto;
    const chamado = this.ChamadoRepo.create();
    chamado.solicitante = solicitante;
    chamado.telefone = telefone;
    chamado.cidade = cidade;
    chamado.posto_trabalho  = posto_trabalho;
    chamado.categoria_problema  = categoria_problema;
    chamado.tipo_problema = tipo_problema;
    chamado.email = email;
    try {
      await chamado.save();
      return chamado;
    } catch (error) {
      throw new InternalServerErrorException(error.message);
    }
  }

  async findChamados(): Promise<Chamado[]> {
    const chamados = this.ChamadoRepo.find({ relations: ['alertas'] });
    if (!chamados)
      throw new NotFoundException('Não existem chamados cadastrados');
    return chamados;
  }

  async findChamadoById(chamadoId: string): Promise<Chamado> {
    const agendamento = await this.ChamadoRepo.findOne({
      where: { id: chamadoId },
    });
    if (!agendamento) throw new NotFoundException('Agendamento não encontrado');
    return agendamento;
  }

  async updateChamado(
    createChamdodto: CreateChamadodto,
    chamadoId: string,
  ): Promise<Chamado> {
    const chamado = await this.ChamadoRepo.findOneBy({
      id: chamadoId,
    });
    const {solicitante,telefone,cidade,posto_trabalho,categoria_problema,tipo_problema,email} = createChamadodto;

    chamado.solicitante = solicitante;
    chamado.telefone = telefone;
    chamado.cidade = cidade;
    chamado.posto_trabalho  = posto_trabalho;
    chamado.categoria_problema  = categoria_problema;
    chamado.tipo_problema = tipo_problema;
    chamado.email = email;

    try {
      await this.ChamadoRepo.save(chamado);
      return chamado;
    } catch (error) {
      throw new InternalServerErrorException(error.message);
    }
  }

  async deleteAgendamento(chamadoId: string) {
    const result = await this.ChamadoRepo.delete({ id: chamadoId });
    if (result.affected === 0) {
      throw new NotFoundException(
        'Nao foi encontrado um chamado com este id',
      );
    }
  }

}
