import { CreateProblemCategoryDto } from './dto/create-problem-category.dto';
import { ReturnProblemCategoryDto } from './dto/return-problem-category.dto';
import { UpdateProblemCategoryDto } from './dto/update-problem-category.dto';
import { Test, TestingModule } from '@nestjs/testing';
import { ProblemCategoryController } from './problem-category.controller';
import { ProblemCategoryService } from './problem-category.service';
import { ProblemCategory } from './entities/problem-category.entity';
import { v4 as uuid } from 'uuid';
import {
  CacheInterceptor,
  CacheModule,
  Header,
  NotFoundException,
} from '@nestjs/common';
import { Repository } from 'typeorm';

describe('ProblemCategoryController', () => {
  let controller: ProblemCategoryController;
  let service: ProblemCategoryService;

  const mockUuid = uuid();

  const mockCreateProblemCategoryDto: CreateProblemCategoryDto = {
    name: 'mockName',
    problem_types: 'mockProblemType1, mockProblemType2',
    description: 'mockDescription',
  };
  const mockUpdateProblemCategoryDto: UpdateProblemCategoryDto = {
    name: 'UpdateMockName',
    problem_types: 'UpdateMockProblemType1, updateMockProblemType2',
    description: 'mockDescription',
  };
  const mockProblemCategoryEntityList = [{ ...mockCreateProblemCategoryDto }];

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      controllers: [ProblemCategoryController],
      providers: [
        {
          provide: ProblemCategoryService,
          useValue: {
            createProblemCategory: jest
              .fn()
              .mockResolvedValue(mockCreateProblemCategoryDto),
            findProblemCategories: jest
              .fn()
              .mockResolvedValue(mockProblemCategoryEntityList),
            findProblemCategory: jest
              .fn()
              .mockResolvedValue(mockProblemCategoryEntityList[0]),
            updateProblemCategory: jest
              .fn()
              .mockResolvedValue(mockUpdateProblemCategoryDto),
            deleteProblemCategory: jest
              .fn()
              .mockResolvedValue('Categoria de problema excluída com sucesso'),
          },
        },
      ],
    }).compile();

    controller = module.get<ProblemCategoryController>(
      ProblemCategoryController,
    );
    service = module.get<ProblemCategoryService>(ProblemCategoryService);
  });

  it('should be defined', () => {
    expect(controller).toBeDefined();
    expect(service).toBeDefined();
  });

  describe('createProblemCategory', () => {
    it('should create a problem category entity successfully', async () => {
      const result = await controller.createProblemCategory(
        mockCreateProblemCategoryDto,
      );
      expect(result).toEqual(mockCreateProblemCategoryDto);
      expect(service.createProblemCategory).toHaveBeenCalledTimes(1);
      expect(service.createProblemCategory).toHaveBeenCalledWith(
        mockCreateProblemCategoryDto,
      );
    });
  });

  describe('updateProblemCategory', () => {
    it('should update a problem category entity successfully', async () => {
      const id = mockUuid;
      const result = await controller.updateProblemCategory(
        id,
        mockUpdateProblemCategoryDto,
      );
      expect(result).toEqual(mockUpdateProblemCategoryDto);
      expect(service.updateProblemCategory).toHaveBeenCalledTimes(1);
      expect(service.updateProblemCategory).toHaveBeenCalledWith(
        id,
        mockUpdateProblemCategoryDto,
      );
    });
  });

  describe('deleteProblemCategory', () => {
    it('should delete a problem category entity succesfully', async () => {
      const id = mockUuid;

      const result = await controller.deleteProblemCategory(id);

      expect(result).toMatch('Categoria de problema excluída com sucesso');

      expect(service.deleteProblemCategory).toHaveBeenCalledTimes(1);

      expect(service.deleteProblemCategory).toHaveBeenCalledWith(id);
    });
  });
});
