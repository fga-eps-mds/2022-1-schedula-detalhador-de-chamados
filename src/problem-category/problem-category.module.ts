import { Module } from '@nestjs/common';
import { ProblemCategoryService } from './problem-category.service';
import { ProblemCategoryController } from './problem-category.controller';
import { ProblemCategory } from './entities/problem-category.entity';
import { TypeOrmModule } from '@nestjs/typeorm';

@Module({
  imports: [TypeOrmModule.forFeature([ProblemCategory])],
  controllers: [ProblemCategoryController],
  providers: [ProblemCategoryService],
})
export class ProblemCategoryModule {}
