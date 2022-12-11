import {
  Injectable,
  InternalServerErrorException,
  NotFoundException,
} from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository, DataSource } from 'typeorm';
import { Call } from './calls.entity';
import { CreateCalldto } from './dto/createCalldto';

@Injectable()
export class CallsService {
  constructor(
    @InjectRepository(Call)
    private CallRepo: Repository<Call>,
  ) {}

  async createCall(
    createCalldto: CreateCalldto,
  ): Promise<Call> {
    const {requester,phone,city,workstation,problem_category,problem_type,email} = createCalldto;
    const call = this.CallRepo.create();
    call.requester = requester;
    call.phone = phone;
    call.city = city;
    call.workstation  = workstation;
    call.problem_category  = problem_category;
    call.problem_type = problem_type;
    call.email = email;
    try {
      await call.save();
      return call;
    } catch (error) {
      throw new InternalServerErrorException(error.message);
    }
  }

  async findCalls(): Promise<Call[]> {
    const calls = this.CallRepo.find({});
    if (!calls)
      throw new NotFoundException('Não existem chamado cadastrados');
    return calls;
  }

  async findCallById(callId: string): Promise<Call> {
    const Call = await this.CallRepo.findOne({
      where: { id: callId },
    });
    if (!Call) throw new NotFoundException('Chamado não encontrado');
    return Call;
  }

  async updateCall(
    createCalldto: CreateCalldto,
    callId: string,
  ): Promise<Call> {
    const call = await this.CallRepo.findOneBy({
      id: callId,
    });
    const {requester,phone,city,workstation,problem_category,problem_type,email} = createCalldto;

    call.requester = requester;
    call.phone = phone;
    call.city = city;
    call.workstation  = workstation;
    call.problem_category  = problem_category;
    call.problem_type = problem_type;
    call.email = email;
    call.date = new Date();
    
    try {
      await this.CallRepo.save(call);
      return call;
    } catch (error) {
      throw new InternalServerErrorException(error.message);
    }
  }

  async deleteCall(callId: string) {
    const result = await this.CallRepo.delete({ id: callId });
    if (result.affected === 0) {
      throw new NotFoundException(
        'Nao foi encontrado um chamado com este id',
      );
    }
  }

}
