//Import dos dtos de chamados ainda não criados
//import {CreateChamadodto} from '../chamados/chamadosdto.ts';

import { IsNotEmpty, IsString } from 'class-validator';

export class CreateChamadodto {
  //chamado : CreateChamadodto;
  @IsNotEmpty({
    message: 'Solicitante não fornecido',
  })
  solicitante: string;
  @IsNotEmpty({
    message: 'Telefone não fornecido',
  })
  telefone: string;
  @IsNotEmpty({
    message: 'Cidade não fornecido',
  })
  cidade: string;
  @IsNotEmpty({
    message: 'Posto de Trabalho não fornecido',
  })
  posto_trabalho: string;
  @IsNotEmpty({
    message: 'categoria do Problema não fornecido',
  })
  categoria_problema: string;
  @IsNotEmpty({
    message: 'Tipo do Problema não fornecido',
  })
  tipo_problema: string;
  @IsNotEmpty({
    message: 'Data não fornecido',
  })
  date: string;
  @IsNotEmpty({
    message: 'email não fornecido',
  })
  email: string;

}
