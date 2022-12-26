import { Module } from '@nestjs/common';
import { ProblemCategoryService } from './problem-category.service';
import { ProblemCategoryController } from './problem-category.controller';

@Module({
  controllers: [ProblemCategoryController],
  providers: [ProblemCategoryService]
})
export class ProblemCategoryModule {}
