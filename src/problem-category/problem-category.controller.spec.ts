import { CreateProblemCategoryDto } from './dto/create-problem-category.dto';
import { UpdateProblemCategoryDto } from './dto/update-problem-category.dto';
import { Test, TestingModule } from '@nestjs/testing';
import { ProblemCategoryController } from './problem-category.controller';
import { ProblemCategoryService } from './problem-category.service';
import { v4 as uuid } from 'uuid';

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
            findProblemCategoryById: jest
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

  describe('findProblemCategories', () => {
    it('should return an array of problem category entities succesfully', async () => {
      const result = await controller.findProblemCategories();
      expect(result).toEqual(mockProblemCategoryEntityList);
      expect(service.findProblemCategories).toHaveBeenCalledTimes(1);
    });
  });

  describe('findProblemCategory', () => {
    it('should return a problem category entity succesfully', async () => {
      const id = mockUuid;
      const message = 'Categoria de problema encontrada';
      const result = await controller.findProblemCategory(id);
      expect(result).toMatchObject({
        problemCategory: mockProblemCategoryEntityList[0],
        message: message,
      });
      expect(service.findProblemCategoryById).toHaveBeenCalledTimes(1);
      expect(service.findProblemCategoryById).toHaveBeenCalledWith(id);
    });
  });

  describe('updateProblemCategory', () => {
    it('should update a problem category entity with new data successfully', async () => {
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
      const message = 'Categoria de problema excluída com sucesso';
      const result = await controller.deleteProblemCategory(id);
      expect(result).toMatchObject({ message: message });
      expect(service.deleteProblemCategory).toHaveBeenCalledTimes(1);
      expect(service.deleteProblemCategory).toHaveBeenCalledWith(id);
    });
  });
});
