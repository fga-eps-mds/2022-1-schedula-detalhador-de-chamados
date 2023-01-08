import { IsNotEmpty, IsString } from 'class-validator';
export class CreateProblemCategoryDto {
  @IsString({ message: 'Informe um nome válido' })
  name: string;
  @IsString({ message: 'Informe um tipo válido' })
  problem_types: string;
}
