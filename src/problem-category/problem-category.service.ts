import { InjectRepository } from '@nestjs/typeorm';
import { Injectable } from '@nestjs/common';
import { Repository } from 'typeorm';
import { CreateProblemCategoryDto } from './dto/create-problem-category.dto';
import { UpdateProblemCategoryDto } from './dto/update-problem-category.dto';
import { ProblemCategory } from '../problem-category/entities/problem-category.entity';

@Injectable()
export class ProblemCategoryService {
  constructor(
    @InjectRepository(ProblemCategory)
    private problemCategoryRepository: Repository<ProblemCategory>,
  ) {}

  create(createProblemCategoryDto: CreateProblemCategoryDto) {
    return this.problemCategoryRepository.save(createProblemCategoryDto);
  }

  findAll() {
    return `This action returns all problemCategory`;
  }

  findOne(id: number) {
    return `This action returns a #${id} problemCategory`;
  }

  update(id: number, updateProblemCategoryDto: UpdateProblemCategoryDto) {
    return `This action updates a #${id} problemCategory`;
  }

  remove(id: number) {
    return `This action removes a #${id} problemCategory`;
  }
}
