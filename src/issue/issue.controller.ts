import {
    Body,
    Controller,
    Delete,
    Get,
    Param,
    Post,
    Put,
} from '@nestjs/common';
import { Issue } from './issue.entity';
import { IssuesService } from './issue.service';
import { CreateIssuedto } from './dto/createIssuedto';

  @Controller('issues')
  export class IssuesController {
    constructor(private issuesService: IssuesService) {}
  
    @Post()
    async createIssue(
      @Body() createIssuedto: CreateIssuedto,
    ): Promise<Issue> {
      const issue = await this.issuesService.createIssue(
        createIssuedto,
      );
      return issue;
    }
  
    @Get()
    async getIssues(): Promise<Issue[]> {
      const issues = await this.issuesService.findIssues();
      return issues;
    }
  
    @Get(':id')
    async getIssue(@Param('id') id: string): Promise<Issue> {
      const issue = await this.issuesService.findIssueById(id);
      return issue;
    }
  
    @Put(':id')
    async updateIssue(
      @Param('id') id: string,
      @Body() updateIssuedto: CreateIssuedto,
    ): Promise<Issue> {
      const issue = await this.issuesService.updateIssue(
        updateIssuedto,
        id,
      );
      return issue;
    }
  
    @Delete(':id')
    async deleteIssue(@Param('id') id: string) {
      const issue = await this.issuesService.deleteIssue(id);
      return {
        message: 'Chamado removido com sucesso',
      };
    }
  }
  