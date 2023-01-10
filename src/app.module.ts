import { Module } from '@nestjs/common';
import { ProblemCategoryModule } from './problem-category/problem-category.module';
import { config } from '../typeOrm.config';
import { TypeOrmModule } from '@nestjs/typeorm';

@Module({
  imports: [ProblemCategoryModule, TypeOrmModule.forRoot(config)],
  controllers: [],
  providers: [],
})
export class AppModule {}
