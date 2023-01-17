import { CreateProblemCategoryDto } from './dto/create-problem-category.dto';
import { UpdateProblemCategoryDto } from './dto/update-problem-category.dto';
import { Test, TestingModule } from '@nestjs/testing';
import { ProblemCategoryService } from './problem-category.service';
import { ProblemCategory } from './entities/problem-category.entity';
import { v4 as uuid } from 'uuid';
import { Repository } from 'typeorm';
import { getRepositoryToken } from '@nestjs/typeorm';
import {
  InternalServerErrorException,
  NotFoundException,
} from '@nestjs/common';

describe('ProblemCategoryService', () => {
  let service: ProblemCategoryService;
  let repo: Repository<ProblemCategory>;

  const mockUuid = uuid();

  const mockCreateProblemCategoryDto: CreateProblemCategoryDto = {
    name: 'mockName',
    description: 'mockDescription',
    problem_types: 'mockProblemType1, mockProblemType2',
  };

  const mockUpdateProblemCategoryDto: UpdateProblemCategoryDto = {
    name: 'UpdateMockName',
    description: 'mockDescription',
    problem_types: 'UpdateMockProblemType1, updateMockProblemType2',
  };

  const mockProblemCategoryEntityList = [{ ...mockCreateProblemCategoryDto }];

  const mockCreateProblemCategoryEntity = {
    name: 'mockName',
    description: 'mockDescription',
    problem_types: 'mockProblemType1, mockProblemType2',
  };

  const mockUpdateProblemCategoryEntity = {
    name: 'UpdateMockName',
    description: 'mockDescription',
    problem_types: 'UpdateMockProblemType1, updateMockProblemType2',
  };

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      providers: [
        ProblemCategoryService,
        {
          provide: getRepositoryToken(ProblemCategory),
          useValue: {
            create: jest
              .fn()
              .mockResolvedValue(mockCreateProblemCategoryEntity),
            find: jest.fn().mockResolvedValue(mockProblemCategoryEntityList),
            findOne: jest
              .fn()
              .mockResolvedValue(mockProblemCategoryEntityList[0]),
            findOneBy: jest
              .fn()
              .mockResolvedValue(mockProblemCategoryEntityList[0]),
            update: jest
              .fn()
              .mockResolvedValue(mockUpdateProblemCategoryEntity),
            delete: jest
              .fn()
              .mockResolvedValue('Categoria de problema excluída com sucesso'),
            save: jest.fn(),
          },
        },
      ],
    }).compile();

    service = module.get<ProblemCategoryService>(ProblemCategoryService);
    repo = module.get<Repository<ProblemCategory>>(
      getRepositoryToken(ProblemCategory),
    );
  });

  it('should be defined', () => {
    expect(repo).toBeDefined();
    expect(service).toBeDefined();
  });

  describe('CreateProblemCategory', () => {
    it('should return a problem category entity succesfully', async () => {
      const result = await service.createProblemCategory(
        mockCreateProblemCategoryDto,
      );
      expect(result).toEqual(mockCreateProblemCategoryEntity);
      expect(repo.save).toHaveBeenCalledTimes(1);
    });

    it('should throw an internal server error', async () => {
      jest.spyOn(repo, 'save').mockRejectedValueOnce(new Error());
      expect(service.createProblemCategory).rejects.toThrowError(
        InternalServerErrorException,
      );
    });
  });

  describe('findProblemCategories', () => {
    it('should return an array of problem category entities succesfully', async () => {
      const result = await service.findProblemCategories();
      expect(result).toEqual(mockProblemCategoryEntityList);
      expect(repo.find).toHaveBeenCalledTimes(1);
    });

    it('should throw an internal server error', async () => {
      jest.spyOn(repo, 'find').mockRejectedValueOnce(new Error());
      expect(service.findProblemCategories).rejects.toThrowError(
        InternalServerErrorException,
      );
    });
  });

  describe('findProblemCategoryById', () => {
    it('should return a problem category entity succesfully', async () => {
      const id = mockUuid;
      const result = await service.findProblemCategoryById(id);
      expect(result).toEqual(mockProblemCategoryEntityList[0]);
      expect(repo.findOne).toHaveBeenCalledTimes(1);
    });

    it('should throw an internal server error', async () => {
      jest.spyOn(repo, 'findOne').mockRejectedValueOnce(new Error());
      expect(service.findProblemCategoryById(mockUuid)).rejects.toThrowError(
        InternalServerErrorException,
      );
    });
  });

  describe('updateProblemCategory', () => {
    it('should update a problem category entity with new data succesfully', async () => {
      const id = mockUuid;
      const result = await service.updateProblemCategory(
        id,
        mockUpdateProblemCategoryDto,
      );
      expect(result).toEqual(mockUpdateProblemCategoryEntity);
      expect(repo.findOneBy).toHaveBeenCalledTimes(1);
      expect(repo.save).toHaveBeenCalledTimes(1);
    });

    it('should throw an internal server error', async () => {
      jest.spyOn(repo, 'save').mockRejectedValueOnce(new Error());
      expect(
        service.updateProblemCategory(mockUuid, mockUpdateProblemCategoryDto),
      ).rejects.toThrowError(InternalServerErrorException);
    });
  });

  describe('deleteProblemCategory', () => {
    it('should delete a problem category entity succesfully', async () => {
      const id = mockUuid;
      //const message = '';
      const result = await service.deleteProblemCategory(id);
      expect(result).toEqual('Categoria de problema excluída com sucesso');
      expect(repo.delete).toHaveBeenCalledTimes(1);
    });

    it('should throw an internal server error', async () => {
      jest.spyOn(repo, 'delete').mockRejectedValueOnce(new Error());
      expect(service.deleteProblemCategory(mockUuid)).rejects.toThrowError(
        InternalServerErrorException,
      );
    });

    it('should throw a not found error', async () => {
      jest.spyOn(repo, 'findOneBy').mockResolvedValueOnce(null);
      expect(service.deleteProblemCategory(mockUuid)).rejects.toThrowError(
        NotFoundException,
      );
    });
  });
});
