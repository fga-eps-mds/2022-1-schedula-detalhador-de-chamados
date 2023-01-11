import { PartialType } from '@nestjs/mapped-types';
import { CreateProblemCategoryDto } from './create-problem-category.dto';

export class UpdateProblemCategoryDto extends PartialType(
  CreateProblemCategoryDto,
) {
  name: string;
  problem_types: string;
}
