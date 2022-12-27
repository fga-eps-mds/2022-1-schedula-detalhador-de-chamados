import { InjectRepository } from '@nestjs/typeorm';
import {
  Injectable,
  InternalServerErrorException,
  NotFoundException,
} from '@nestjs/common';
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

  async createProblemCategory(
    createProblemCategoryDto: CreateProblemCategoryDto,
  ): Promise<ProblemCategory> {
    const { name, problem_types } = createProblemCategoryDto;
    return this.problemCategoryRepository.save(createProblemCategoryDto);
    const problemCategory = this.problemCategoryRepository.create();
    problemCategory.name = name;
    problemCategory.problem_types = problem_types;
    try {
      await problemCategory.save();
      return problemCategory;
    } catch (error) {
      throw new InternalServerErrorException(
        'Erro ao salvar o usuário no banco de dados',
      );
    }
  }

  async findProblemCategories(): Promise<ProblemCategory[]> {
    const problemCategories = this.problemCategoryRepository.find();
    if (!problemCategories)
      throw new NotFoundException('Categoria de problema não encontrada');

    return problemCategories;
  }

  async findProblemCategoryById(id: number): Promise<ProblemCategory> {
    const problemCategory = await this.problemCategoryRepository.findOne({
      select: ['id', 'name', 'problem_types'],
    });
    if (!problemCategory)
      throw new NotFoundException('Categoria de problema não encontrada');

    return problemCategory;
  }

  async updateProblemCategory(
    id: number,
    updateProblemCategoryDto: UpdateProblemCategoryDto,
  ): Promise<ProblemCategory> {
    const problemCategory = await this.problemCategoryRepository.findOneBy({
      id: id,
    });
    const { name, problem_types } = updateProblemCategoryDto;
    problemCategory.name = name ? name : problemCategory.name;
    problemCategory.problem_types = problem_types
      ? problem_types
      : problemCategory.problem_types;
    try {
      await problemCategory.save();
      return problemCategory;
    } catch (error) {
      throw new InternalServerErrorException(
        'Erro ao salvar os dados no banco de dados',
      );
    }
  }

  async deleteProblemCategory(id: number) {
    const result = await this.problemCategoryRepository.delete({ id: id });
    if (result.affected === 0) {
      throw new NotFoundException(
        'Não foi encontrada uma categoria de problema com o ID informado',
      );
    }
  }
}
