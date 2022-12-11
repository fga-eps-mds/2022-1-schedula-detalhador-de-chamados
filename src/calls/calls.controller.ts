import {
    Body,
    Controller,
    Delete,
    Get,
    Param,
    Post,
    Put,
} from '@nestjs/common';
import { Call } from './calls.entity';
import { CallsService } from './calls.service';
import { CreateCalldto } from './dto/createCalldto';

  @Controller('calls')
  export class CallsController {
    constructor(private callsService: CallsService) {}
  
    @Post()
    async createCall(
      @Body() createCalldto: CreateCalldto,
    ): Promise<Call> {
      const call = await this.callsService.createCall(
        createCalldto,
      );
      return call;
    }
  
    @Get()
    async getCalls(): Promise<Call[]> {
      const calls = await this.callsService.findCalls();
      return calls;
    }
  
    @Get(':id')
    async getCall(@Param('id') id: string): Promise<Call> {
      const call = await this.callsService.findCallById(id);
      return call;
    }
  
    @Put(':id')
    async updateCall(
      @Param('id') id: string,
      @Body() updateCalldto: CreateCalldto,
    ): Promise<Call> {
      const call = await this.callsService.updateCall(
        updateCalldto,
        id,
      );
      return call;
    }
  
    @Delete(':id')
    async deleteCall(@Param('id') id: string) {
      const call = await this.callsService.deleteCall(id);
      return {
        message: 'Chamado removido com sucesso',
      };
    }
  }
  