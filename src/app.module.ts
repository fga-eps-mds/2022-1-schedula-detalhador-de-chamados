import { ProblemCategoryModule } from './problem-category/problem-category.module';
import { config } from '../typeOrm.config';
//import { IssueModule } from './issue/issue.module';
import { AppService } from './app.service';
import { AppController } from './app.controller';
import { Module } from '@nestjs/common';
import configuration from './configs/configuration';
import { ConfigModule } from '@nestjs/config';
//import { ScheduleModule } from './schedules/schedules.module';
import { TypeOrmModule } from '@nestjs/typeorm';

const configService = configuration();

@Module({
  imports: [
    //TypeOrmModule.forRoot(config),
    ConfigModule.forRoot({ load: [configuration] }),
    TypeOrmModule.forRoot({
      type: 'postgres',
      host: configService.database.host,
      port: 5432,
      username: configService.database.user,
      password: configService.database.pass,
      database: configService.database.db,
      entities: [__dirname + '/../**/*.entity.{js,ts}'],
      synchronize: true,
    }),
    ProblemCategoryModule,
  ],
  controllers: [AppController],
  providers: [AppService],
})
export class AppModule {}
