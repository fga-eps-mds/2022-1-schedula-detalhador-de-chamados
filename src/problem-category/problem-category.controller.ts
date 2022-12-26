import {
  Controller,
  Get,
  Post,
  Body,
  Patch,
  Param,
  Delete,
} from '@nestjs/common';
import { ProblemCategoryService } from './problem-category.service';
import { CreateProblemCategoryDto } from './dto/create-problem-category.dto';
import { UpdateProblemCategoryDto } from './dto/update-problem-category.dto';

@Controller('problem-category')
export class ProblemCategoryController {
  constructor(
    private readonly problemCategoryService: ProblemCategoryService,
  ) {}

  @Post()
  create(@Body() createProblemCategoryDto: CreateProblemCategoryDto) {
    return this.problemCategoryService.create(createProblemCategoryDto);
  }

  @Get()
  findAll() {
    return this.problemCategoryService.findAll();
  }

  @Get(':id')
  findOne(@Param('id') id: string) {
    return this.problemCategoryService.findOne(+id);
  }

  @Patch(':id')
  update(
    @Param('id') id: string,
    @Body() updateProblemCategoryDto: UpdateProblemCategoryDto,
  ) {
    return this.problemCategoryService.update(+id, updateProblemCategoryDto);
  }

  @Delete(':id')
  remove(@Param('id') id: string) {
    return this.problemCategoryService.remove(+id);
  }
}
